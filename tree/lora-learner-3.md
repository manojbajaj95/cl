# LoRA Learner 3: Rejoin the Answers, Keep the Directions

Child of [LoRA Learner 2](lora-learner-2.md) ([PR #346](https://github.com/manojbajaj95/cl/pull/346), depth 2) · 27 candidate primitives · 4 ranked questions · Ideas only; no experiments run

**Thesis.** When two groups are climbing different hills, let each branch optimize for its own users rather than training one max-min compromise. But a permanent copy is not the only way to remember a direction. If both branches can serve the same answer today, discard the duplicate serving weights while retaining what each group can independently teach tomorrow. Conversely, while answers are still shared, reserve one bounded write slot that can realize two incompatible corrections when fresh feedback licenses one. The durable object should be a *way to learn a correction*, not a cached answer or a preauthorized update.

**Why this node exists.** The [review of #346, row 473][triage] kept L2-19 (rejoin serving while keeping independently teachable amendment coordinates) and L2-16 (reserve opposite edits in one slot) at score 3; no score 4. It made L2-08's common-proposal rule mandatory, not a new primitive. Following the [idea ledger][ledger], these cards don't revive a split-only library, a Gramian readiness proxy, or a checkpoint scheme. Related [#340 DS12][ds12] keeps an option for a previously rejected direction; here a LoRA write must realize the option from fresh feedback without storing two serving children.

## Shared repeated-revision protocol

- **Stream.** Freeze a linear or small ReLU Executor; the Learner writes actual LoRA factors. Begin with routine old tasks A/B (B rare). Give both groups the same initial alternative pairs, then alternate shared revisions, real conflicts, temporary agreement, and fresh amendments C/D/E. Include permanent divergence, durable convergence, agreement on present actions but different later corrections, a shift toward neither reserved direction, and an unseen order of changes. Treat a *teachable direction* as the effect of authorized feedback under a specified write budget, not a gradient cosine. Use simulator utilities only for evaluation.
- **Mandatory same-item gate.** For every candidate fork, reopening, or branch selection that is scored as a split, both cohorts must actually have seen and rated **the same request and the same candidate output pair** under a matched presentation. Randomize pair order, repeat enough to distinguish reliable directional disagreement from flips, and pay for the elicitation. Compute disagreement on that intersection, not on marginals or imputed counterfactual ratings. Include an exposure-only decoy with disjoint pairs and matching pooled discordance: it must yield **zero credited splits**. A prospective learning fork during agreement is provisional state, not a counted split; a simulated or unilateral amendment alone cannot validate one. Common-item disagreement is necessary, not sufficient: for a serving split also beat the strongest legal shared edit at the same budget and demonstrate a pre-action cue rather than an oracle group ID.
- **Baseline on every card (“Stack”).** Use the stronger matched static [Text-to-LoRA][t2l] or [Drag-and-Drop][dnd] writer, rerun on fresh descriptions or prompt evidence at each revision, followed by **per-skill distillation** (including an [on-policy][opcd] arm where relevant) and a **routed LoRA library** ([Arrow][arrow]-style). Allow a cue-conditioned single adapter, the optimized shared-plus-residual implementation, and cached source if paid for. Give all arms the same feedback, proposal exposure, runtime cues, adaptation deadlines and budgets. Bill retained and peak bytes (including parent and reserved directions), peak live rank, inference compute, proofs, state decoders and failed writes. Compare total labels/writes or memory at matched retention and new cohort gain, not comparisons to a frozen zero-updater.
- **Close controls.** For rejoin: merge both serving and amendment, keep both children, [GLAM][glam]/[Compress-then-Merge][ctm], one meta-updater, and an equal-byte explicit symbolic amendment table. Include a held-out intervention that *should collapse* the remaining routes. For reserve: matched [InfLoRA][inf] and [OML][oml], ordinary signed coefficients, an empty spare coordinate, random directions, and two paid child adapters. Include a no-fit (“neither”) outcome and check actual future correction cost. In a linear scalar slot with effects (+u) and (-u), a signed scalar over one fixed basis is already sufficient; the proposal must beat that control in an identified regime, not discover the sign bit.
- **Retention.** Every first test below adds a specific slice to normal hidden A/B returns after rejoin, immediately after each accepted or refused write, and after E. Run old requests through the production route, not a rescued old checkpoint. Report per-cohort and worst-case scores, especially rare B, along with adaptation latency and new performance. Refusing everything does not pass. No runs are proposed outside CPU-scale fixtures; no experiments were performed.

## Literature check

Hugging Face Papers discovery was followed by checks of original arXiv abstracts. The comparisons below describe mechanisms, not a claim of priority or full-paper coverage.

| Prior mechanism | What remains to test |
|---|---|
| [MaxMin-RLHF][maxmin] fits a mixture of preferences and learns a max-min policy objective. [VPL][vpl] already conditions rewards and policies on user latents and can actively elicit preferences. [MiCRo][micro] models preference mixtures and adapts their weights with context-aware online routing. [Personalized Soups][soups] combines preference-aligned models for user control. | Branching is an alternative to a single compromise, not new personalization by itself. Measure whether cohort-specific gains persist over revisions and whether keeping separate amendment state after a *true shared serving solution* is cheaper than keeping separately routed policies. [Partial reward identifiability][ident] cautions that identical observations can fit different rewards. |
| [InfLoRA][inf] defines update subspaces to reduce interference; [O-LoRA][olora] assigns task updates to orthogonal subspaces; [OGD][ogd] projects updates away from old-output interference; [OML][oml] learns representations for future online updates. | A protected, learnable direction is established prior art. A candidate reserve must preserve a pair of feedback-linked outcomes at an actual bounded write interface, and compete with an equally sized low-rank subspace and an ordinary signed basis. |
| [GLAM][glam] groups and merges adapters and [Compress-then-Merge][ctm] projects adapters into shared low-rank coordinates before merging. [C-LoRA][clora] uses a shared adapter with stability and plasticity components. [FedRep][fedrep] shares a representation while keeping local heads. | Neither a single serving LoRA nor local/shared factorization is itself new. Test an operation that can remove local serving weights **without** losing a learned, separately exercisable amendment. |
| [LoRA-XS][xs] learns a small inner matrix between frozen factors; [VeRA][vera] shares fixed low-rank matrices and learns scaling vectors; [ACL][acl] meta-learns continual-learning algorithms. | One cheap slot is not enough. Look for a portable or composable operation at the amendment interface, priced against a symbolic updater and equivalent factorizations. |

## A · Rejoin what serves, not what can be taught

### L3-01 · Factor a correction contrast out of the children
- **Mechanism:** Before deleting the children, record a small mapping from authorized feedback to the difference between their intended amendments. Keep one shared response rule and this contrast, not the two local serving deltas.
- **Novelty vs nearest prior art:** [GLAM][glam] and [CtM][ctm] compress serving adapters. This object is derived from the *response to a write*, not from tensor similarity or current outputs.
- **Cheapest first test:** Enumerate two 8-state policies that converge on actions but interpret the same next correction as “only this case” versus “all cases in this class.” Swap labels of later corrections to check causal dependence on the saved contrast.
- **Old-task retention:** Check both old audiences' neighboring cases where the broad correction must not spill, including rare B.
- **Beat the Stack on revisions:** Recover both independently licensed edits at E with fewer active bytes than keeping adapters and fewer fresh labels than rebuild-on-demand; include an equal-byte contrast table.

### L3-02 · Delete serving weights under a reconstruction embargo
- **Mechanism:** Erase both children, prevent saving any lossless per-child serving code, and retain only bounded edit semantics. Ask whether a later correction can build children for *new* targets that the erased children would get wrong.
- **Novelty vs nearest prior art:** [FedRep][fedrep] retains client heads; [CtM][ctm] keeps a single serving LoRA. The proposed operation keeps only how to take a step from the new shared policy, neither client outputs nor an exact restoration route.
- **Cheapest first test:** Randomize discarded child behaviors independently of the upcoming correction. Test an explicit table of permitted rules, replay-free re-fit, and a retained child compressed to the same bytes.
- **Old-task retention:** Revisit ordinary older workloads during the embargo and after applying feedback that changes only one requested behavior.
- **Beat the Stack on revisions:** Reduce retained bytes and fresh examples jointly; if equally sized compressed children score the same after E, the embargo buys nothing.

### L3-03 · Transport amendment meaning through a shared rewrite
- **Mechanism:** When an unrelated revision changes the shared adapter, transport each dormant amendment by what it must do on paired behavior probes, not by copying its old factor coordinates.
- **Novelty vs nearest prior art:** [LoRA-XS][xs] compresses writes in a frozen coordinate frame and [InfLoRA][inf] chooses a protected subspace. The candidate retargets independent *future feedback effects* when the current shared map changes, not active adapter transfer across bases.
- **Cheapest first test:** Change the hidden activation frame of a two-layer toy and leave the Executor base fixed. Give the old port a now-wrong effect; compare analytic transport, a frozen port, and equal-evidence re-fit.
- **Old-task retention:** Check untouched old coalition and non-coalition behavior after transport and after either port is exercised.
- **Beat the Stack on revisions:** Do less redistillation over D and E than updating and recaching each library member; charge probe fitting and include an analytic tie.

### L3-04 · One serving rule, two independent amendment deadlines
- **Mechanism:** Rejoin serving while retaining a bounded write route that can honor an early amendment for one cohort without forcing a premature change for the cohort awaiting its own evidence.
- **Novelty vs nearest prior art:** [C-LoRA][clora] explicitly separates stability and plasticity; [MiCRo][micro] adapts preference mixtures online. This isolates a scheduling consequence of separately teachable edits even when current answers match.
- **Cheapest first test:** In a toy scheduling skill, alternate feedback arriving before and after a commitment boundary. Compare explicit deadline queues plus one meta-updater and trial-only child weights.
- **Old-task retention:** Check old requests already in flight across each deadline and clients whose answers should not change before confirmation.
- **Beat the Stack on revisions:** Meet both revision deadlines with fewer charged serving writes or fewer late responses at matched accuracy; do not count a unilateral write as a fork.

### L3-05 · Rejoin against a third, previously shared intervention
- **Mechanism:** Use two probes that separate the private amendments and a third that they must still share. Keep independent coordinates only if one shared action can propagate the third correction while each private action leaves the other untouched.
- **Novelty vs nearest prior art:** [FedRep][fedrep] has shared representations and private heads; [OML][oml] optimizes future learnability. This object is a three-way intervention contract for deleting local serving weights, not static multitask sharing.
- **Cheapest first test:** Enumerate a shared default correction and one authorized exception per cohort. Test all three orderings of what comes last; compare a blocked explicit sidecar and naïve merged distillation.
- **Old-task retention:** Check old shared defaults and private exception boundaries after every order, especially rare overlap requests.
- **Beat the Stack on revisions:** Pay for the shared D correction once and still resolve E independently without maintaining the two live child weights.

### L3-06 · Rejoin one observable service slice at a time
- **Mechanism:** Delete the child code for only the common service slice, but keep amendment coordinates that can later teach different rules at its boundary. Do not let a temporary unobserved cohort stand in for agreement.
- **Novelty vs nearest prior art:** [CtM][ctm] captures common parameter structure; [Arrow][arrow] routes modules. The candidate reclaims *a service slice* with a separate test of how any future authorized edit crosses its boundary.
- **Cheapest first test:** Use three intervals of toy input space: true agreement, visible disagreement, and missing overlap. Compare shared trunk/heads and input-region distillation; include an exposure-only decoy on the third.
- **Old-task retention:** Score hidden old requests on either side of each boundary and old clients with no cue.
- **Beat the Stack on revisions:** Cut live bytes before whole-skill agreement, then edit the boundary after E without more wrong-route calls or distillation work.

### L3-07 · Preserve correction scope under feedback paraphrase
- **Mechanism:** Retain a private amendment only if a change in how feedback is phrased leaves its affected cases unchanged while swapping scope changes them. Store the retained intervention relation, rather than each cohort's feedback wording.
- **Novelty vs nearest prior art:** [VPL][vpl] learns calibrated user-conditioned preferences; [OPCD][opcd] distills trajectory behavior. The target is invariant *feedback scope* after serving is merged, not response personalization or wording robustness alone.
- **Cheapest first test:** Cross two meanings with two short feedback grammars on a finite policy. Hold out one grammar for each cohort and swap the meaning with the text fixed.
- **Old-task retention:** Check ordinary old revisions in the original grammar and held-out routine requests whose answers should remain unchanged.
- **Beat the Stack on revisions:** At D/E need fewer restated examples to recover correct scope than re-running either static writer and refining both adapters.

### L3-08 · Collapse a route, not all the routes that look like it
- **Mechanism:** Use an intervention that should make two amendment routes equivalent within a declared horizon; free the route's bytes only if the forecast matches held-out feedback. Leave another equally quiet but still distinct route live.
- **Novelty vs nearest prior art:** [ACL][acl] meta-learns update dynamics and [GLAM][glam] groups adapters. The reusable operation is a targeted retirement of teachability state after serving has already merged.
- **Cheapest first test:** Model three authorized senders with the same action policy: two become amendment-equivalent; the third diverges only after a second correction. Compare a single updater, learned merge heuristic, and finite bisimulation check.
- **Old-task retention:** Check all three senders on normal old tasks before route retirement and on sequences that require their earlier distinctions.
- **Beat the Stack on revisions:** Reclaim the one route without an E reconstruction penalty or a false rejoin of the third, charging the intervention used to collapse it.

### L3-09 · Give rejoin a bound on how long evidence remains useful
- **Mechanism:** Store for each retained amendment the observable conditions under which its feedback-to-effect map remains usable. When a later revision violates a condition, invalidate only that coordinate and solicit new feedback.
- **Novelty vs nearest prior art:** [VPL][vpl] models uncertainty and [OML][oml] optimizes adaptation to later learning. This is an explicit validity boundary on a dormant amendment, not a confidence-driven serving router.
- **Cheapest first test:** Construct one condition that remains valid through D yet one that E replaces. Compare fixed expiration, full refresh, and an equally sized cache invalidation table.
- **Old-task retention:** Check requests depending on the surviving route and routine old cases in the invalidated scope where no unconfirmed edit should occur.
- **Beat the Stack on revisions:** Refresh just one teachable direction following E instead of recompiling both skills; retained-byte savings must exceed the charged validity map.

## B · Reserve two edits in one bounded write slot

### L3-10 · Certify the two ends and the neutral middle
- **Mechanism:** Reserve one neutral slot with two signed write options; each must pass the old floors on its own. Store the feedback condition selecting each endpoint and a third outcome that leaves the slot unchanged and requests new evidence.
- **Novelty vs nearest prior art:** [InfLoRA][inf] protects a subspace and [VeRA][vera] learns small scaling vectors. The candidate is a tested three-outcome *write contract*; in the linear symmetric case it reduces to a signed scalar and has no rank advantage.
- **Cheapest first test:** Enumerate slots with two legal endpoints, only one legal endpoint, and neither. Match an empty coordinate, signed coefficients, InfLoRA subspaces, and random reserved directions.
- **Old-task retention:** Check old behavior at neutral and under both authorized endpoint writes, including rare examples at the validity margin.
- **Beat the Stack on revisions:** Use fewer stored weights and reach either justified E correction in one write, but beat the signed basis at matched cost or concede the simpler mechanism.

### L3-11 · Keep opposite behavior with unequal write lengths
- **Mechanism:** Allow two opposite effects on a target comparison to use asymmetric edit magnitudes; bind them to measured coalition utility and cap each with different protected-read margins. The reserved slot keeps the legal interval, not a pair of serving checkpoints.
- **Novelty vs nearest prior art:** [OGD][ogd] constrains update directions and [LoRA-XS][xs] permits a compact core. The proposed object is a feedback-indexed pair of legal endpoints robust to asymmetric step costs, not ordinary line search.
- **Cheapest first test:** Use a clipped two-output head where the long end clears one floor and the short end preserves a rare old read. Compare symmetric reserve, learned signed steps, and separately distilled children.
- **Old-task retention:** Check the old read most sensitive to the long step and the old output most sensitive to the short step.
- **Beat the Stack on revisions:** Make both E revisions feasible under the same slot without extra fitting; a tuned one-coordinate line search should eliminate the advantage if it finds both endpoints at equal cost.

### L3-12 · Keep semantic opposition across a nonmonotone slot
- **Mechanism:** Treat a reserve as two validated target effects, not two raw tensor signs. Choose an address where the allowed changes still induce opposite behavior after an unrelated nonlinear rewrite; discard a sign if it ceases to do so.
- **Novelty vs nearest prior art:** [InfLoRA][inf] and [O-LoRA][olora] constrain subspaces, not feedback-defined effects after a change of activation region. Piecewise-affine checking is a control, not the novelty.
- **Cheapest first test:** Enumerate a frozen ReLU head where positive and negative perturbations initially have the same effect at one site but two other amplitudes straddling an activation boundary have opposite effects. Require both reachable from the neutral serving value.
- **Old-task retention:** Test old inputs near the changed activation threshold at neutral and at both reachable options.
- **Beat the Stack on revisions:** Reuse a verified address rather than fit two adapters after D/E, while charging enumeration and endpoint refresh. No credit for a factored dictionary that already performs the same edit.

### L3-13 · Reserve a direction whose effect no current user can see
- **Mechanism:** Record a bounded reservation whose effect is null on current service but becomes measurable on a later, declared comparison. Require fresh evidence after that comparison appears; a reservation does not authorize serving it.
- **Novelty vs nearest prior art:** [OGD][ogd] protects previous outputs; DS12 preserves a rejected proposal destination. The gap is a verified transition from a behaviorally silent slot to a current usable correction under a normal user comparison.
- **Cheapest first test:** In a tiny model, an old feature never activates until a policy change. Include activation decoys where the new evidence favors neither candidate. Compare empty spare, random reserve, and a sidecar storing the candidate instruction.
- **Old-task retention:** Check old cases both with the previously unseen feature now present and without it, including a case where it should remain irrelevant.
- **Beat the Stack on revisions:** Reach the newly observable E target with fewer labels and no new serving rank while preserving the originally neutral default through D.

### L3-14 · Let two later feedback messages jointly select one option
- **Mechanism:** Leave the slot neutral until two separately authorized observations distinguish a candidate from a plausible common correction. Store one selection rule and the surviving slot, not a pending private weight for each message.
- **Novelty vs nearest prior art:** [VPL][vpl] actively elicits preference and [ACL][acl] meta-learns updates. The test is whether two partial pieces can authorize one bounded edit without persisting partial serving changes.
- **Cheapest first test:** Use a 2-bit task where either observation alone leaves both signed options possible, but their conjunction identifies an edit or neither. Compare a symbolic accumulator and a recurrent updater with the same evidence.
- **Old-task retention:** Interleave ordinary A/B between both messages and check that the first message cannot change their answers.
- **Beat the Stack on revisions:** Use fewer provisional writes and lower peak bytes across D/E without increasing the number of questions needed to reach the same target.

### L3-15 · Release one direction while keeping the other feasible
- **Mechanism:** After feedback changes the authorized scope, revoke one endpoint and reuse its freed budget for another skill, while retaining the first endpoint and shared neutral behavior.
- **Novelty vs nearest prior art:** [C-LoRA][clora] controls stability and plasticity and [O-LoRA][olora] isolates task updates; the proposed operation is partial revocation of a discrete reservation. If both signs are fully encoded by one scalar, there are no endpoint bytes to free, and the candidate fails.
- **Cheapest first test:** Enumerate a quantized slot whose two nonlinear endpoints require distinct metadata. Reallocate one candidate's metadata budget and compare ordinary sparse packing and a both-or-neither port.
- **Old-task retention:** Verify old service and the surviving permitted correction after the reallocation; an old forbidden correction must not become implicitly authorized.
- **Beat the Stack on revisions:** Fit a new E direction in the same peak memory while honoring the earlier endpoint, with fewer separate updates than repacking the routed library.

### L3-16 · Donate an unused reservation without donating authority
- **Mechanism:** Let another skill borrow the physical slot during an interval when the owning skill needs neither endpoint. It must restore a valid neutral state and both future options by a declared return event, without transferring who may grant an amendment.
- **Novelty vs nearest prior art:** [VeRA][vera] shares fixed low-rank matrices and [C-LoRA][clora] shares an adapter. The target is bounded reuse of an idle write obligation with a tested return, not free storage attributed to an offloaded copy.
- **Cheapest first test:** Two finite workflows have staggered feedback deadlines. Compare an explicit allocator with the same return obligations, static separate slots, and a schedule where deadlines overlap.
- **Old-task retention:** Check both workflows' old calls during borrowing and after a return in which both allowed edits are exercised separately.
- **Beat the Stack on revisions:** Lower peak reservation bytes over two alternating amendments with no missed return deadlines; bill any restoration bits and extra write.

### L3-17 · Retain the reserve after one endpoint is used
- **Mechanism:** Instead of treating each reservation as one-shot, require a write path from the committed option to the other through a post-revision neutral point. The neutral point incorporates unrelated changes and is not a saved checkpoint.
- **Novelty vs nearest prior art:** [OML][oml] learns representations good for successive online updates and [InfLoRA][inf] protects old subspaces. The claim is an explicit, feedback-gated path that remains callable after a separate amendment consumes some write budget.
- **Cheapest first test:** Enumerate a short factor lattice with one safe two-move switch and a matched lattice with no switch after D. Compare ordinary signed update, checkpoint subtraction, and fresh search.
- **Old-task retention:** Check normal old requests at the intermediate neutral value as well as at both endpoints, including the task learned at D.
- **Beat the Stack on revisions:** Switch at E with fewer labels or checks than retraining a child, while preserving D and charging every serving transition.

### L3-18 · Fit two roles for one direction, not two full directions
- **Mechanism:** Reuse one change vector but attach two mutually exclusive interpretations of when it is legal to use. For one cohort the result is a default; for the other it is an exception to a rule. Opposed feedback can thus require opposite *scope* changes even if the local logit increment is identical.
- **Novelty vs nearest prior art:** [VeRA][vera] shares fixed low-rank factors and [MiCRo][micro] selects preference mixtures. The candidate preserves opposite amendment semantics over a shared vector, not a parameter compression claim from sharing a basis alone.
- **Cheapest first test:** A toy classifier receives one same-sign correction that applies to complementary subsets under the two cohorts' feedback. Compare equal-byte scope masks, ordinary factor sharing, and two edit tables.
- **Old-task retention:** Check the complements of both affected sets and old requests belonging to both.
- **Beat the Stack on revisions:** Teach both distinct E scopes with fewer reserved coefficients without leaking a default across cohorts; tie if an explicit signed scope mask already does it as cheaply.

## C · Make rejoin and reserve work across repeated changes

### L3-19 · Rejoin at the point with the cheapest legal next moves
- **Mechanism:** Among shared serving ties, select a rejoin point by enumerating actual future amendment moves through one reserved slot. Keep a short witness that both independently licensed moves are possible, rather than guessing from a global plasticity score.
- **Novelty vs nearest prior art:** [OML][oml] trains representations to learn faster later and [CtM][ctm] seeks shared low-rank coordinates. This candidate chooses among merges by the cost of two specific retaining next writes through a constrained interface.
- **Cheapest first test:** Create two exact service ties with equal measured rank and unequal legal distances to the two amendments. Include a case where a same-size symbolic updater makes both distances equal.
- **Old-task retention:** Check old tasks at each candidate rejoin and at both subsequent endpoints after D changes an unrelated output.
- **Beat the Stack on revisions:** Achieve lower cumulative refitting cost after C and E at the same rank and worst-cohort retention; include proof cost and compare the symbolic tie.

### L3-20 · Reuse one slot for two independent directions over time
- **Mechanism:** Encode two edits as a neutral core and a compact rule for materializing one from current feedback. After applying it, release the scratch slot and maintain sufficient semantics for the other; do not promise simultaneous fits in one degree of freedom.
- **Novelty vs nearest prior art:** [VeRA][vera] shares a fixed basis and [LoRA-XS][xs] learns compact cores. The gap is serial reuse of a write interface with an explicit next-edit obligation on the remaining route, not storage of two independent values in a scalar.
- **Cheapest first test:** Enumerate a two-step task where user amendments never overlap, then repeat with simultaneous amendments. Compare a full explicit update table, shared scalar plus router, and two slots.
- **Old-task retention:** Check both old cohorts between serial writes and in the overlap case where one slot must refuse or buy capacity.
- **Beat the Stack on revisions:** Lower peak writable state over C/D/E without increasing conflicts or paying as much rebuilding; expect no advantage under genuinely simultaneous independent demands.

### L3-21 · Repair the reserve when an ordinary correction steals its direction
- **Mechanism:** If an unrelated shared edit takes away one dormant direction, write the smallest substitution that restores it while preserving the already-applied change and the other route. Revalidate in the new shared frame.
- **Novelty vs nearest prior art:** [InfLoRA][inf] chooses noninterfering subspaces and [C-LoRA][clora] adapts rank-one contributions. The target is restoring a particular dormant teachability obligation after loss, not just making some free rank available.
- **Cheapest first test:** Use a two-layer toy with three named writable columns; make D consume one formerly valid endpoint. Compare unused rank, protected-subspace recomputation, and exact constrained refitting.
- **Old-task retention:** Check old requests protected by the stolen direction, D's new rule, and the undamaged cohort after each candidate repair.
- **Beat the Stack on revisions:** Pay for one local substitution rather than regenerating both skills; exact recomputation at the same cost is a tie.

### L3-22 · Compose only the reservations that remain callable together
- **Mechanism:** Before admitting a second rejoin, test whether its reserved options block either legal option of the first rejoin under an overlapping arrival schedule. If they do, jointly recompile the reservations or keep the cheaper separate service.
- **Novelty vs nearest prior art:** [O-LoRA][olora] separates task updates and [GLAM][glam] groups adapters. This tests joint compatibility of yet-unexecuted amendments, including which order keeps the other callable.
- **Cheapest first test:** Enumerate two rejoined skills where each has two safe endpoints alone, but one endpoint pair cannot be reached in one order. Compare per-slot checks, orthogonal allocation, and explicit joint scheduling.
- **Old-task retention:** Check old A/B at every prefix of both amendment orders, not just after both finish.
- **Beat the Stack on revisions:** Keep the cheaper shared configuration when compatible and save the rejected joint rewrite when incompatible; bill both order checks.

### L3-23 · Transfer the chooser without transferring the direction
- **Mechanism:** A rejoined skill can export the rule for which evidence resolves an opposite edit, not its adapter coordinates. The recipient must discover legal local endpoints and recheck whether the same paired feedback selects them.
- **Novelty vs nearest prior art:** [VPL][vpl] can infer preference latents and [MiCRo][micro] routes them. The distinction is reuse of a policy for resolving a reserved write under different local edit geometry; no transferred preference label can authorize the new write unaided.
- **Cheapest first test:** Reuse a “shared default versus personal exception” comparison pattern on two toys whose valid factor directions are deliberately remapped. Compare transfer of the latent, transfer of the delta, and training a new chooser.
- **Old-task retention:** Check source behavior after export and recipient requests not licensed by the imported chooser, including a mismatched scope.
- **Beat the Stack on revisions:** Buy fewer labels on later recipient revisions without storing a copied child adapter or accepting more false splits.

### L3-24 · Get independent correction from crossed examples
- **Mechanism:** Retain two provisional directions only if feedback on a small pair of examples distinguishes crossing effects: teaching cohort A on example one should change scope in its later example two, but the same correction from B should not.
- **Novelty vs nearest prior art:** [OGD][ogd] preserves old predictive outputs and [OML][oml] learns sparse representations for future learning. The candidate uses a *crossed future edit response* to tell useful independence from merely orthogonal numbers.
- **Cheapest first test:** Match immediate outputs, rank, and marginal feedback; vary whether the next two examples have shared or separate correction scope. Compare an analytic scope table and a single meta-updater with identical evidence.
- **Old-task retention:** Test old counterexamples that involve both scopes, and original cohort tasks after changing each scope independently.
- **Beat the Stack on revisions:** Need fewer repeated E corrections than feedback pooling, at lower bytes than keeping two active children; fail if the explicit scope table ties.

### L3-25 · Pay both alternatives' opportunity cost at rejoin
- **Mechanism:** Charge a reservation by the fresh edits it precludes while it is idle. Drop the less useful option only on a declared bound and buy it back with fresh feedback if it later becomes worthwhile; do not preserve both by default.
- **Novelty vs nearest prior art:** [C-LoRA][clora] trades off stability and plasticity and [VPL][vpl] prioritizes informative feedback. The candidate records a cost for guaranteeing a dormant edit versus using that same capacity for unrelated learning.
- **Cheapest first test:** Use an exact small capacity allocator with sparse versus frequent opposite amendments, and a rare branch whose missed deadline is expensive. Compare a fixed reserve, no reserve, and an optimal finite allocator as a ceiling.
- **Old-task retention:** Check rare older corrections while capacity is lent and after an actually required option is restored.
- **Beat the Stack on revisions:** Fit more useful D revisions without missing protected E deadlines and without higher peak bytes; no credit for treating rare users' losses as uncharged.

### L3-26 · Rejoin only what can be safely reopened
- **Mechanism:** Require a lawful service rejoin and a short reopening plan that relies on a future shared comparison, not automatic rollback. If the future comparison cannot be shown to both cohorts under the allowed interface, share only where a split won't be required by the contract.
- **Novelty vs nearest prior art:** [GLAM][glam] compacts adapters and [MiCRo][micro] routes on available context. This proposal makes the ability to acquire *common exposure* part of deciding what can safely be merged today.
- **Cheapest first test:** Match today's agreements in two environments; one permits a common future probe within the deadline, the other hides one option from a cohort. Compare keep-both, unconditional merge, and budgeted active querying.
- **Old-task retention:** Check old ordinary requests and rare clients excluded from the future probe; no fallback to hidden child weights.
- **Beat the Stack on revisions:** Keep lower serving bytes in the reopenable condition without paying more failed writes or losing either cohort at E; no split credit in the non-overlap condition.

### L3-27 · Rejoin, reserve, and explain the option that neither group chose
- **Mechanism:** After a common comparison, retain both old routes only if they still explain distinguishable, legal future amendments. If neither reserved edit matches the new feedback, write a new shared edit if feasible and retire the obsolete reserve rather than routing to the nearest sign.
- **Novelty vs nearest prior art:** [MaxMin-RLHF][maxmin] learns a single policy against mixtures; [VPL][vpl] conditions policies on latent preference. The candidate operation switches from separately teachable routes to a new common climb while invalidating old latent edit options.
- **Cheapest first test:** Alternate opposite, shared, and third-direction rounds with identical exposure and add a disjoint-exposure decoy. Compare nearest-sign selection, fixed personalized routing, and exact joint fitting given the same evidence.
- **Old-task retention:** Run the old requests that once distinguished both branches, then an ordinary new shared correction unrelated to their original opposition.
- **Beat the Stack on revisions:** Reach the third direction without an unnecessary pair of redistillations or persistent branch bytes while retaining both cohorts' old utility; shared joint fitting can negate the advantage.

## Ranked deeper questions

1. **What survives when we delete both serving children?** Find the smallest state that preserves two independently teachable amendments after a genuine rejoin and an intervening shared rewrite. Require a new target the old children would get wrong, and one intervention that should collapse the two routes. Does it beat an equal-byte explicit sidecar and the routed Stack at matched ordinary retention (L3-01–L3-09, L3-19)?
2. **When is an opposite-edit reserve more than a signed coefficient?** Start from the case where a scalar is exactly sufficient. Is there a constrained or nonlinear write interface where one neutral slot with two licensed write paths can survive another revision more cheaply than InfLoRA, OML, a spare coordinate, and a precomputed pair (L3-10–L3-18)?
3. **Can both normal service and separate teachability survive a second rejoin?** Test a shared agreement interval, an unrelated rewrite, and a later conflict. Count a split only on a common-item disagreement with a valid pre-action route. Ask whether a candidate beats the Stack on cumulative bytes, evidence, and revision work when the next shift instead agrees, disagrees, or favors neither old direction (L3-19–L3-27).
4. **When should we keep two policies instead of compromising or merging?** Use MaxMin as an explicitly non-branching control and VPL/MiCRo-style conditioning as strong personalization controls. Compare each cohort's gains, not the pooled mean, on matched comparisons; if a shared cue-conditioned policy delivers both gains at lower revision cost, serving copies are not necessary.

[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L473
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[ds12]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L463
[t2l]: https://arxiv.org/abs/2506.06105
[dnd]: https://arxiv.org/abs/2506.16406
[opcd]: https://arxiv.org/abs/2602.12275
[arrow]: https://arxiv.org/abs/2405.11157
[maxmin]: https://arxiv.org/abs/2402.08925
[vpl]: https://arxiv.org/abs/2408.10075
[micro]: https://arxiv.org/abs/2505.24846
[soups]: https://arxiv.org/abs/2310.11564
[ident]: https://arxiv.org/abs/2203.07475
[inf]: https://arxiv.org/abs/2404.00228
[olora]: https://arxiv.org/abs/2310.14152
[ogd]: https://arxiv.org/abs/1910.07104
[oml]: https://arxiv.org/abs/1905.12588
[glam]: https://arxiv.org/abs/2509.13211
[ctm]: https://arxiv.org/abs/2606.03723
[clora]: https://arxiv.org/abs/2502.17920
[fedrep]: https://arxiv.org/abs/2102.07078
[xs]: https://arxiv.org/abs/2405.17604
[vera]: https://arxiv.org/abs/2310.11454
[acl]: https://arxiv.org/abs/2312.00276
