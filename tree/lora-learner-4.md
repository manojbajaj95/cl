# LoRA Learner 4: Delete the Branches, Repair the Next Move

Child of [LoRA Learner 3](lora-learner-3.md) ([PR #348](https://github.com/manojbajaj95/cl/pull/348), depth 3) · 27 candidate primitives · 4 ranked questions · Ideas only; no experiments run

**Thesis.** Two groups that want different outcomes should be able to steer different policies, not live with a max-min compromise. When their service needs truly converge, delete both children rather than storing them in a different form. Keep only enough knowledge to learn their next distinct corrections from fresh feedback. If useful shared learning later consumes one reserved direction, repair the *ability to make that next move*, not the old adapter or the old factor coordinates.

**Parent verdict.** The [review of #348, row 476][triage] scores no card 4 and keeps L3-02 (delete both children under a reconstruction embargo) and L3-21 (repair a reserve after an ordinary edit takes its direction). The signed spare coefficient is now a required control; an unhit reserve that acts as one signed scalar is not a reason to advance the reserve line. The [idea ledger][ledger] also rules out treating a readiness score, checkpoint restore, or a split-only hierarchy as a new primitive.

## Shared repeated-revision protocol

- **Stream.** Freeze a tiny linear or ReLU Executor and have the neural Learner write actual LoRA factors. Start with old tasks A/B (including rare B) and cohorts with distinct child adapters. Make them agree on normal service, rejoin, and delete both child products. Introduce a real unrelated shared revision D after deletion. Later reveal fresh E feedback that demands new cohort targets the old children would get wrong. Include D that consumes a dormant direction, D that leaves it intact, E that needs either option, E that needs neither, and durable agreement. Revisit A/B and add a second rewrite or split–rejoin cycle. A reserved option is a legal future effect in a declared write interface, not just a direction vector.
- **Reconstruction embargo.** In the proposed arm, forbid child serving factors and products, exact checkpoints, caches of enough logits or trajectories to recover them, and hidden copies in writer, router, optimizer, source, or decoder state. Declare and bill every retained field before D; freeze the common writer or train it only on disjoint scenario families. Keep permissible task evidence and fresh feedback equal across embargo arms. In an exact toy, choose several old child product pairs with different behavior on a discarded slice but the same valid shared service and permissible amendment summary. Check that the **entire** retained state is identical across this family and that old snapshots fail E. For learned variants use a held-out reconstruction challenge (failure of a tested decoder isn't a privacy or unlearning guarantee). This is non-restoration of serving children, not erasure of all learned knowledge, and not permission to lose old tasks. Keeping both children and an equal-byte exact-restore code are charged **controls**, not legal embargo implementations; report when the code cannot fit, and also compare best lossy retained child at that budget, fresh regrowth and a single meta-updater.
- **Mandatory common-item gate.** Apply to every scored split/reopening below: both groups must actually see and rate the **same request and output pair** under matched presentation. Randomize order, pay for repeated ratings, and show reliable disagreement on the co-rated intersection. Disjoint-exposure decoys with the same pooled discordance earn zero splits. Provisional writes and unilateral feedback are not split evidence. Require a feasible pre-action route and failure of the strongest equally budgeted shared write before crediting separate serving policies.
- **Mandatory signed-spare control (“Signed”).** Run first, on every card below. Give the baseline one genuinely usable spare signed coefficient over the best feasible fixed basis chosen from the same pre-D evidence, a tuned step in either direction, the same cue and fresh feedback, and identical bytes/rank and deadlines. Compare an *unrepaired* signed coefficient over D, and for repair cards also a repicked basis or fresh [InfLoRA][inf] allocation with the same paid measurement and write budget; add [OML][oml], an empty spare, a paid precomputed pair, and exact search/refit where feasible. If Signed ties on the unhit linear case, accept the tie. Only claim reserve repair when D makes the old endpoint infeasible, a new endpoint is reachable, and the repair is cheaper or more reliable than repicking, without changing D or the intact route. No gain from hiding extra rank in decoder state.
- **Baseline on every card (“Stack”).** Rerun the stronger static [Text-to-LoRA][t2l] or [Drag-and-Drop][dnd] writer on revised descriptions or prompt batches, refine by **per-skill distillation** ([OPCD][opcd] where appropriate), and serve through a **routed LoRA library** ([Arrow][arrow]-style). Give it the same feedback, routes/cues and deadlines; include a shared cue-conditioned adapter. Track unconstrained Stack and embargo-matched Stack separately so a forced deletion isn't mistaken for a method advantage. Bill stored and peak bytes, write attempts, probe/evidence cost, decoder work, and serving compute. Each card names a particular repeated-stream comparison in addition to Signed and its nearest control.
- **Retention.** Run ordinary hidden A/B through the normal serving interface after rejoin, after D, after a repair (before using it), after E for each legal choice, and on the next stream return. Also check D's legitimate new behavior and the unhit cohort's ability to use its route. Report task-wise and worst-cohort floors with fresh adaptation; neither retaining checkpoints in secret nor declining all changes counts.

## Literature check

Used Hugging Face Papers discovery and checked original arXiv abstracts for mechanisms. These are nearest comparisons, not full-paper or priority claims.

| Prior art | Boundary for this node |
|---|---|
| [GLAM][glam] groups and merges adapters; [Compress-then-Merge][ctm] projects adapters into a shared low-rank core before merging. [Latent-LoRA][latent] uses compact latent-space adapters and gradient-free routing; [FedRep][fedrep] retains separate local heads with a shared representation. | A compact or merged serving representation isn't itself a new object. Disallow per-child reconstruction and measure correction at a *different future target*. |
| [SISA][sisa] limits data-point influence to expedite removing data; [Suppression or Deletion][del] tests whether behaviors treated as unlearned can be restored by internal steering. | The comparison motivates a restoration challenge, not a claim of machine unlearning: old child products must not be recoverable from permitted state, while legitimate historical service stays. |
| [InfLoRA][inf], [OGD][ogd], and [AlphaEdit][alpha] protect old behavior with constrained updates; [Null-LoRA][null] constrains low-rank increments in a null space; [RLSEdit][rls] fits sequential edits using soft constraints and recursive least squares. | Reprojection, null-space search, and online refitting are controls. The narrow claim is economical repair of *the same prospective correction obligation* after a legitimate write, with D and the unaffected option still intact. |
| [C-LoRA][clora] decomposes stability and plasticity within a shared adapter; [AdaLoRA][ada] allocates rank budget adaptively; [PaLoRA][palo] addresses accumulated leakage even under directional constraints; [OML][oml] trains representations for faster retaining future updates; [VeRA][vera] supplies small scaling parameters over shared factors. | Spare rank, signed scaling, and good future adaptation alone aren't new. Score the actual cost and work of repairing a known, broken option, not a proxy for plasticity. |
| [MaxMin-RLHF][maxmin] learns a max-min policy against diverse preferences; [VPL][vpl] conditions reward and policy models on user latents; [MiCRo][micro] adapts preference mixture weights with context-aware routing. | Compare separate steering to a single compromise and to standard personalized routing. Neither a latent preference nor a route is evidence that deleted serving weights cannot be restored or that a reserved correction can still be made. |

## A · Delete both children and keep only what can teach

### L4-01 · Export the equivalence class of a correction
- **Mechanism:** Summarize pre-rejoin learning by what authorized feedback should change after rejoin, grouping old child pairs that imply the same correction but had different discarded serving behavior. Store the shared class identifier, not the representative.
- **Novelty vs nearest prior art:** [CtM][ctm] merges projected serving coordinates. An equivalence class over future edit responses can deliberately identify old pairs whose serving products differ.
- **Cheapest first test:** Construct an eight-state head with a train-time nuisance bit choosing between old child behaviors. Verify the full retained state is identical across both nuisance values and test E on unseen scopes.
- **Old-task retention:** Check old inputs adjacent to the discarded slice, any legitimate shared features, and rare B after D and E.
- **Beat the Stack on revisions:** Match fresh E gains with fewer retained bytes or labels than routed refitting; Signed plus a same-size explicit class table can erase the claimed gain.

### L4-02 · Separate teaching bits from discarded-answer bits
- **Mechanism:** Learn a small feedback decoder over independently varied teaching and serving choices. Carry only bits predicting how a formerly authorized correction should generalize; check that the retained bits cannot identify independently randomized old products in the finite toy.
- **Novelty vs nearest prior art:** [Latent-LoRA][latent] uses small latent serving adapters. Here low dimensionality isn't enough; old child identity must be nonrecoverable from the permitted state while future correction remains possible.
- **Cheapest first test:** Cross a balanced two-bit old serving identity with a one-bit amendment rule and enumerate reachable summary collisions. Compare a lossy autoencoder, an exact code and a hard-coded teaching bit.
- **Old-task retention:** Check routine A/B independent of the nuisance identity and old rare inputs whose legitimate rule must survive.
- **Beat the Stack on revisions:** Get the one-bit correction benefit after D without paying to store the independent serving bits; if the explicit bit plus Signed matches it, use that instead.

### L4-03 · Export a difference in what an example teaches
- **Mechanism:** Save a relation such as “this feedback changes rounding only for the originating cohort,” not the old rounded outputs. Teach from a novel numerical value after D, requiring a new low-rank product instead of replaying an old endpoint.
- **Novelty vs nearest prior art:** [OPCD][opcd] internalizes behavior from trajectories and [VPL][vpl] conditions on inferred preferences. The candidate exports a rule about how to extrapolate one future example after serving state has been removed.
- **Cheapest first test:** Rejoin on integer values, change scale at D, and give E feedback on a previously unseen half-unit. Compare a small extrapolation table, fresh distillation and copied children.
- **Old-task retention:** Check existing formatting rules and cases where old rounding should remain unchanged despite the new scale.
- **Beat the Stack on revisions:** Need fewer E demonstrations to apply the rule at new scales without retaining private outputs; compare Signed with the same extrapolation table.

### L4-04 · Keep a constraint the old children cannot meet
- **Mechanism:** Export a partial obligation for the next authorized correction, expressed relative to a new common anchor after rejoin. Select test targets on which neither erased child is good enough even if reloaded exactly.
- **Novelty vs nearest prior art:** [FedRep][fedrep] keeps client heads; [RLSEdit][rls] fits sequential targets with an anchor. Here the transferred object is the relative obligation used to build a new child, not the prior head or its old fitted targets.
- **Cheapest first test:** Change a shared normalization offset at D, then teach unit increase versus a capped exception. Use a full grid to compare old snapshots, an anchor-based symbolic rule and fresh refit.
- **Old-task retention:** Check D's new shared normalization and ordinary old targets outside the correction scope after both candidate changes.
- **Beat the Stack on revisions:** Reuse one obligation through D and E rather than distilling two adapters twice; a fixed Signed basis under the new anchor may already fit.

### L4-05 · Delete the decoder's access to old child identities
- **Mechanism:** Keep a common decoder trained before it ever sees the evaluated children. Permit only a bounded typed amendment message from each erased child. Test whether the message helps on E without the decoder learning a unique shortcut to the deleted outputs.
- **Novelty vs nearest prior art:** [Text-to-LoRA][t2l] learns to generate adapters from descriptions. The candidate tests whether an explicitly restricted update message can transfer teachability rather than recovering an adapter already memorized by the shared generator.
- **Cheapest first test:** Hold out complete child families; permute nuisance IDs and test reconstructed products on an auditor-only discarded slice. Compare a sidecar using the identical typed messages.
- **Old-task retention:** Score old requests under unseen child identifiers and for previously shared input boundaries after E.
- **Beat the Stack on revisions:** Reduce retraining/annotation on unseen child families at matched serving memory, including a Stack and Signed decoder exposed to the exact same training evidence.

### L4-06 · Preserve the scope of a correction, not the policy
- **Mechanism:** Keep a compact witness of which old cases must remain unaffected by an authorized correction. Use that witness to rule out bad descendant edits; do not keep any target output for the discarded cells.
- **Novelty vs nearest prior art:** [AlphaEdit][alpha] protects pre-existing knowledge via a null-space projection. The distinction is retaining an edit's no-change *scope* through deletion and a new shared anchor, rather than retaining the old outputs as explicit distillation targets.
- **Cheapest first test:** Train a two-rule toy and delete its branches. Check whether a small membership predicate identifies protected cases after D without retaining their old child values. Compare parametric null-space checks and an explicit scope mask.
- **Old-task retention:** Check ordinary tasks on hidden inputs inside the protected region and old D-dependent cases on its boundary.
- **Beat the Stack on revisions:** Prove or find a valid E edit with fewer queries than redistilling both scopes; give Signed the same predicate and charge any proof.

### L4-07 · Retain a counterexample to the wrong correction rule
- **Mechanism:** Delete old serving examples except a compact relation that rules out a plausible but wrong amendment interpretation. Use subsequent independent evidence to license the right edit; the retained relation alone is not an update command.
- **Novelty vs nearest prior art:** [OPCD][opcd] trains on behavior-bearing trajectories; [VPL][vpl] can ask informative questions. The candidate preserves a negative constraint on learning, not an old prediction or labels to replay.
- **Cheapest first test:** Build two candidate scope rules with identical early agreement. Keep a counterexample to one scope but no case label from either deleted child; test a novel disagreement after D.
- **Old-task retention:** Exercise the once-ambiguous old scope and unrelated old tasks after both a justified edit and a refused edit.
- **Beat the Stack on revisions:** Resolve E with one fewer paid comparison than rebuilding; if Signed or a tiny stored counterexample gives the same result, there is no representational advantage.

### L4-08 · Test both erasure and learnability with an exchanged summary
- **Mechanism:** Swap retained amendment summaries between rejoined toys while holding their shared serving adapter fixed. A valid summary swaps the fresh correction behavior but neither restores nor swaps the erased policies' nuisance behaviors.
- **Novelty vs nearest prior art:** [Suppression or Deletion][del] uses restoration to detect retained knowledge. This candidate pairs a non-restoration check with a positive causal test that the retained state drives genuinely new writes.
- **Cheapest first test:** In a finite fixture swap summaries, nuisance identities, both, or neither; compare an auditor with decoder access to all permitted state and a flat symbolic summary.
- **Old-task retention:** Check A/B and both ordinary cohort paths after swaps and E, excluding any unauthorized serving changes.
- **Beat the Stack on revisions:** Demonstrate that the cheaper retained state, not an off-path child cache, causes a revision gain that a matched Stack and Signed comparison cannot reproduce.

### L4-09 · Reset the common anchor without reopening either child
- **Mechanism:** When D substantially changes common service, update the semantics of a retained amendment relative to the new anchor using paired observations of the new shared policy only.
- **Novelty vs nearest prior art:** [RLSEdit][rls] regularizes around anchor mappings and [CtM][ctm] uses shared cores. The claim is amending an edit interface without reopening deleted serving products, not just reusing a common basis.
- **Cheapest first test:** In a closed-form two-output head change the meaning of an old “increase” example under D. Compare anchor-relative translation, an equally sized sidecar and fresh clarification.
- **Old-task retention:** Verify D and all previously common old calls before any private edit and after either authorized E.
- **Beat the Stack on revisions:** Avoid buying both source reannotations after an anchor shift; compare Signed after analytic renormalization and expect a tie when the translation is just a scalar.

## B · Repair a reserve after a useful edit consumes it

### L4-10 · Replace a lost port without rewriting the intact port
- **Mechanism:** Treat a reserve as two scoped obligations. After D disables one, replace only the failed low-rank factor or writable address. The repaired option must meet its former effect contract relative to D and leave the surviving option callable.
- **Novelty vs nearest prior art:** [InfLoRA][inf] finds a protected update subspace. The proposed operation patches a single failed obligation while preserving another previously certified write, rather than choosing a whole new space.
- **Cheapest first test:** Enumerate three writable columns of a frozen two-layer toy; D blocks the first, an unhit control D′ does not, and the third is an admissible substitute. Add a no-substitute case.
- **Old-task retention:** Check rare A/B, D's newly learned output, and the unhit edit before and after exercising the repaired option.
- **Beat the Stack on revisions:** Spend less on D/E than regenerating both child skills and less than measured Signed basis reselection or a fresh InfLoRA subspace; require ties on the unhit case.

### L4-11 · Repair the port where the conflict occurs
- **Mechanism:** Identify the smallest subset of protected effects that D newly couples to the reserve. Repair the reserve only on that subset, reusing the old factor addresses where their effects are unchanged.
- **Novelty vs nearest prior art:** [AlphaEdit][alpha] projects against protected knowledge. The candidate takes an already-tested effect contract as input and attempts a local repair of its failed subset rather than reprojecting all endpoints.
- **Cheapest first test:** Use a block-diagonal head with one off-diagonal coupling created by D. Compare whole-space reprojection, a same-size block-masked update, and an unrelated D′ with matched scale.
- **Old-task retention:** Check the coupled old block and an uncoupled rare old block whose output must remain unchanged even after E.
- **Beat the Stack on revisions:** Reduce total checks and writes to reach E relative to Stack and repicked Signed; a blockwise analytic projection that ties defeats the claim.

### L4-12 · Preserve the effect by repairing the input factor
- **Mechanism:** If D changes which hidden inputs a reserved LoRA responds to, hold the output direction fixed and rewrite only the input factor. Repair the other factor only in a matched condition where the loss is on the effect side.
- **Novelty vs nearest prior art:** [VeRA][vera] and [Null-LoRA][null] constrain factors or updates for efficiency. This tests when a failure can be repaired on one side of a live option without moving its established output or affecting its sibling.
- **Cheapest first test:** Cross input drift and output drift in a frozen two-layer model with a changeable LoRA. Offer an equal-byte fixed signed basis, same-cost rank-one refit, and a known analytic factor replacement.
- **Old-task retention:** Check old-trigger cases and old-output cases separately, including a rare premise where D changed the activation distribution.
- **Beat the Stack on revisions:** Avoid layer-wide redistillation across D/E with fewer writes than repicked Signed or whole-factor refit; gain must disappear when D misses the reserve.

### L4-13 · Replace a vanished port with two legal bounded moves
- **Mechanism:** When no single legal move realizes the old effect, compile a shortest permitted two-write path whose served intermediate state keeps A/B and D. Do not call it a repair if the intermediate step violates retention or exceeds the original deadline.
- **Novelty vs nearest prior art:** [OGD][ogd] constrains individual directions and [PaLoRA][palo] controls leakage under repeated updates. The candidate preserves an already-promised outcome by changing its implementation from one move to a bounded path.
- **Cheapest first test:** Enumerate a quantized factor lattice where D removes one edge but leaves a two-edge detour, plus a matched cut with no path. Compare exact reachability and sequential projection.
- **Old-task retention:** Run normal traffic at the path midpoint and endpoint, and check the unaffected route can still receive an ordinary amendment.
- **Beat the Stack on revisions:** Meet E at lower cumulative cost than a fresh child plus routing and a tuned Signed head; charge both writes and compare an exact two-step optimizer.

### L4-14 · Repair under a finite precision change
- **Mechanism:** When D forces rounding or reuses part of the slot's scale, repair the endangered endpoint with a quantized replacement that preserves the certified effect margin and does not change current service.
- **Novelty vs nearest prior art:** [PaLoRA][palo] studies finite-precision leakage under direction constraints, [AdaLoRA][ada] allocates parameter budgets. The target is preserving one named next edit when its previous representation is no longer realizable at the same precision.
- **Cheapest first test:** Enumerate 3-bit coefficients in a fixed-rank toy; vary D's genuine effect and scale separately. Compare re-quantization with the same bits, spare Signed magnitude tuning, and full endpoint refit.
- **Old-task retention:** Check old near-tie logits under quantized serving and immediately after both clean and repaired options.
- **Beat the Stack on revisions:** Use fewer added bits or refinement attempts across D/E while matching D and E; an equal-bit numerical solver that ties is sufficient.

### L4-15 · Hand a blocked reserve to an equivalent address
- **Mechanism:** Compile a local substitution map from two addresses that induce the same allowed feedback effect. Rebind after D only if the receiving address is still free and matches the declared effect, including the intact option's applicability.
- **Novelty vs nearest prior art:** [C-LoRA][clora] controls rank-one contributions within one adapter and [InfLoRA][inf] opens legal subspaces. The claim is reuse of a small verified address substitution, not just moving capacity among layers.
- **Cheapest first test:** Design two addresses with matched effects for one scope but not another. Block the first address with D and compare nearest free address, exact local matching, and signed basis reselection.
- **Old-task retention:** Check old requests that can distinguish the two addresses and the unhit cohort's next correction.
- **Beat the Stack on revisions:** Avoid new training examples after D by using the substitution relation, at lower total check cost than native Stack or repicked Signed.

### L4-16 · Check that repair preserves the unchosen option's future
- **Mechanism:** A repair must not merely keep the other endpoint legal now. Require that after exercising the repaired option, a subsequent ordinary correction can still reach the unaffected route under the original budget.
- **Novelty vs nearest prior art:** [OML][oml] improves future adaptation and [RLSEdit][rls] tracks past and current constraints. The new claimed object is a repair contract tested on the other option's *next ordinary write*.
- **Cheapest first test:** Compare two local repairs equal on present endpoints but unequal on a second move after E. Use a known finite transition table and an equal-byte explicit update-rule sidecar.
- **Old-task retention:** Test A/B and D before the first exercise, between exercises, and after the other cohort's correction.
- **Beat the Stack on revisions:** Avoid a second redistillation cycle while retaining both routes; the same-depth planning version of Signed must pay identical probing cost.

### L4-17 · Refuse a repair whose substitute would change D
- **Mechanism:** If all substitutes violate D or the intact route, emit a scoped infeasibility witness instead of moving the newly learned rule back or narrowing the old floor to make the repair appear legal.
- **Novelty vs nearest prior art:** [AlphaEdit][alpha] projects an edit into a preservation subspace, which may leave insufficient useful directions. The candidate propagates a failed repair as a precise constraint on what fresh evidence or capacity could make it feasible.
- **Cheapest first test:** Enumerate a two-dimensional case with the only E-improving axis consumed by D; vary whether one extra legal coordinate or a scope correction restores feasibility. Compare solver refusal and least-norm projection.
- **Old-task retention:** Check the hard D slice and old A/B through the refused repair; test a later permissible edit so permanent abstention cannot win.
- **Beat the Stack on revisions:** Save futile attempted writes without missing the first truly feasible E correction compared with Stack and expanded Signed; exact solver refusal is an explicit tie.

### L4-18 · Pay for a repair only if fresh feedback can use it
- **Mechanism:** After detecting a hit, mark the slot invalid without restoring it immediately. Test a diagnostic of whether either legal new target will need the replacement; repair lazily when that diagnostic and authorized feedback justify the cost.
- **Novelty vs nearest prior art:** [VPL][vpl] buys informative preferences and [AdaLoRA][ada] reallocates capacity. The candidate couples delayed repair of a *known broken option* with forward cost accounting, not just when to open rank.
- **Cheapest first test:** Match early D hit effects across three worlds, then reveal E requiring the lost endpoint, the intact endpoint, or neither. Compare eager repair, delayed full refit, and a lazy repicked Signed coefficient.
- **Old-task retention:** Check old behavior while the broken option is marked unavailable and after each of the three E reveals.
- **Beat the Stack on revisions:** Use less cumulative write work without worse deadlines or additional feedback; local repair must beat the lazy signed control on the hit-and-needed cell.

## C · Test deletion and repair together

### L4-19 · Carry a repairable constraint across deletion, not a vector
- **Mechanism:** On rejoin, discard both products and store each authorized edit's behavioral obligation in a common coordinate system. If D consumes the old implementation, compile a new low-rank implementation from the obligation and fresh E feedback.
- **Novelty vs nearest prior art:** [CtM][ctm] keeps merged serving coordinates and [InfLoRA][inf] selects a legal subspace. Here the surviving object must permit relocation of a future edit *without* the old implementations being recoverable.
- **Cheapest first test:** Combine a randomized discarded old product with a fixed measurable edit obligation; let D switch which factor address realizes it. Compare an explicit contract table, scratch regrowth, and a fresh Signed basis.
- **Old-task retention:** Protect common service from the discarded slice through rejoin, keep D intact, and test the unaffected old scope after E.
- **Beat the Stack on revisions:** Repair an actual hit without keeping/restoring the child and using fewer E labels or writes than embargo-matched Stack and repicked Signed.

### L4-20 · Inherit the evidence requirements after the port moves
- **Mechanism:** After relocating a broken port, transfer its scope and which authorizations must be reacquired. Evidence that licensed the old implementation is reusable only if it still measures the same behavioral comparison.
- **Novelty vs nearest prior art:** [MiCRo][micro] updates context-sensitive routing and [VPL][vpl] adjusts preference uncertainty. This preserves the *evidence contract* of an edit through both removal of serving state and a change in its implementation.
- **Cheapest first test:** Match old scope but switch whether D changes the alternatives named in a correction. Compare unconditional evidence carryover, re-query-all, and a scope-aware signed sidecar.
- **Old-task retention:** Check prior clients whose old requests use the same text with a changed meaning, plus durable ordinary D requests.
- **Beat the Stack on revisions:** Reuse legitimately matched evidence after D with fewer repeats while not replaying invalid labels into E; compare the scope-aware Signed control.

### L4-21 · Teach the writer to distinguish hit signatures from noise
- **Mechanism:** During writer training, use matched D/D′ pairs that produce the same current service change but only D breaks a reserved effect; teach the writer to propose repair only when a held-out intervention confirms the broken option.
- **Novelty vs nearest prior art:** [OML][oml] trains through future updates and [PaLoRA][palo] models cumulative leakage. The candidate supervision is a paired *obligation-loss event* rather than current regression or future loss alone.
- **Cheapest first test:** Enumerate tiny service-equivalent D/D′ edits with different later reachable endpoints. Train on one layout and test another; compare a flat classifier given the same interventions and exact reachability.
- **Old-task retention:** Check rare A/B and D across both paired conditions, including false positives where repair could break a functioning path.
- **Beat the Stack on revisions:** Spend fewer paid repairs and E queries than Stack or a Signed basis refreshed on every D; charge writer training separately.

### L4-22 · Remove an old route and test which repair still works
- **Mechanism:** Intervene on the retained summary by dropping one cohort's amendment rule after rejoin. A successful repair should now help only the other scope; if both still recover, look for hidden reconstruction or redundant state.
- **Novelty vs nearest prior art:** [Suppression or Deletion][del] diagnoses latent recoverability; [FedRep][fedrep] naturally permits head ablation. The candidate is an audit of causal locality of recovery when serving children no longer exist.
- **Cheapest first test:** Cross omitted-summary and intact-summary arms with D hitting either route. Give the auditor all legal retained state but no hidden teacher, and include an intentional cache-positive control.
- **Old-task retention:** Check that removing a dormant rule leaves shared old tasks intact and that the surviving cohort can apply its later E correction.
- **Beat the Stack on revisions:** Attribute a genuine cost/success advantage to the surviving compact rule rather than both old adapters; require the matched explicit rule and Signed control not to tie.

### L4-23 · Separate an embargo violation from a legitimate behavioral tie
- **Mechanism:** Put randomized differences in discarded child products and keep normal old behavior fixed. Declare restoration only when the state predicts those differences, not when fresh learning happens to reproduce a correct shared response.
- **Novelty vs nearest prior art:** [SISA][sisa] targets deletion of training influence; [Suppression or Deletion][del] distinguishes residual representations from removed behavior. This control tests child identity separately from old-task retention and credit for a new E write.
- **Cheapest first test:** Use four old product pairs with identical A/B and different inactive rows; add a cache-based positive control and a legitimate A/B tie after D. Check all allowable states in the finite toy.
- **Old-task retention:** Preserve identical ordinary old outputs during the embargo and run the new scoped correction without recovering the discarded rows.
- **Beat the Stack on revisions:** Match or exceed Stack at E under the identity-audit budget, not just by throwing bits away; Signed plus a non-restoring sidecar is the critical tie.

### L4-24 · Restore the relation between two directions, not the old signs
- **Mechanism:** If D makes two former directions no longer jointly compatible, recompile a pair that realizes the original independently teachable effects in the new shared frame. The signatures may rotate or change sign; no fixed historical factors are retained.
- **Novelty vs nearest prior art:** [O-LoRA][olora] separates tasks in orthogonal subspaces; [C-LoRA][clora] guides stability and plasticity. This tests repair of a relation between two feedback-conditioned edits after deleting the original children.
- **Cheapest first test:** Use a two-mode toy where the post-D signs no longer isolate the two scopes; include a cell where a reparameterized single Signed scalar ties, and a cell where two actual effect obligations need separate handling.
- **Old-task retention:** Check each original safe scope, D's behavior and the other route after each candidate repair.
- **Beat the Stack on revisions:** Recover both E effects without reconstructing either child, using fewer re-fit attempts than Stack and equal-rank fresh allocation.

### L4-25 · Carry a failing witness into the next rejoin
- **Mechanism:** After local repair fails, retain only the small fact explaining failure (for example, that D consumed a projection needed by the scope) so the next rejoin can avoid recreating the same broken route. No old child or exact previous reserve is stored.
- **Novelty vs nearest prior art:** [OML][oml] learns for future updates and [AlphaEdit][alpha] protects old knowledge. The claim is reuse of a failed *prospective edit obligation* across two rejoin cycles, not expanding the historical output constraint set.
- **Cheapest first test:** Run two rejoin cycles with different old products but one shared obstruction. Compare storing failed directions, a symbolic no-good constraint, a fresh Signed allocation, and full recompilation.
- **Old-task retention:** Check A/B and D across both rejoin cycles, including old cases that need the previously unhit direction.
- **Beat the Stack on revisions:** Avoid repeated failed repairs with fewer bits than storing old directions and lower total write cost than rebuild-on-each-cycle; a same-size no-good table may tie.

### L4-26 · Charge the repair against the full cost of staying branched
- **Mechanism:** Treat the rejoin as a resource decision: preserve only edit semantics if the expected decoders, matched probes and repairs are cheaper than retaining children, and allow separate policies when the checked break-even condition reverses.
- **Novelty vs nearest prior art:** [GLAM][glam] limits growth by adapter merging and [Latent-LoRA][latent] reduces adapter cost. This candidate exposes a decision boundary that includes the cost of *future destructive interference with edit options* after erasure.
- **Cheapest first test:** Cross sparse versus frequent reserve hits with cheap versus expensive common comparisons in a finite budget model. Compare greedy merge, always-branch, and exact offline allocation as a ceiling.
- **Old-task retention:** Require old floors under high churn and outlier feedback, not just on the low-cost mean stream.
- **Beat the Stack on revisions:** Find a regime with lower total cost than both the unconstrained Stack and the Signed policy while keeping the same old and new floors; otherwise leave the branches intact.

### L4-27 · Require a new direction on the second reopening
- **Mechanism:** Test two complete delete–rewrite–reopen cycles where the second conflict points toward a novel outcome, not one of the previously saved signs. Repair only what remains supported and build the genuinely new direction from common-item feedback.
- **Novelty vs nearest prior art:** [VPL][vpl] supports user-specific objectives and [RLSEdit][rls] handles long editing sequences. The candidate evaluates repeated non-restoring adaptation: neither cloned children nor a static two-endpoint reserve can succeed by replaying the same answers.
- **Cheapest first test:** Use three possible policy modes and two independent revisions that absorb different directions, with a disjoint-exposure decoy before the real second disagreement. Compare exact restore, a fresh adaptive Signed control and independent regrowth.
- **Old-task retention:** Check rare B, each legitimate D rule and both ordinary cohorts after both deletes, repairs and actual reopenings.
- **Beat the Stack on revisions:** Pay fewer cumulative bytes, labels or updates than rebuilding at each reopening while matching both new targets and all old floors; count no split on the decoy.

## Ranked deeper questions

1. **Can a lost direction be repaired more cheaply than picking a fresh one?** Run the signed-spare control first, including repicking the basis. After a real D hit, require a replacement that keeps D, ordinary A/B, and the other option live. If fresh InfLoRA or exact refit ties, the repair primitive has not earned its place (L4-10–L4-18).
2. **What can the Learner retain without encoding either old child?** Look for a finite family of genuinely different child products with identical permitted retained state. Can that state reduce the cost of achieving two new targets after deletion and a shared rewrite, versus fresh regrowth, a single meta-updater, and a same-size explicit teaching message (L4-01–L4-09)?
3. **Does reconstruction-free repair still pay twice?** Put two delete–rewrite–reopen cycles in one stream, with a second new direction and an exposure-only decoy. Credit only common-item disagreements with a usable pre-action route. Compare cumulative cost to embargo-matched and unconstrained Stack and tuned Signed at matched old and new floors (L4-19–L4-27).
4. **Where should rejoin lose by design?** Map the boundary where a narrow signed reserve is enough, where a justified repair is cheaper, and where real, durable preference conflict makes two policies better than max-min or a cue-conditioned shared write. The target is a measured choice between these regimes, not rejoin everywhere.

[triage]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L476
[ledger]: https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md
[t2l]: https://arxiv.org/abs/2506.06105
[dnd]: https://arxiv.org/abs/2506.16406
[opcd]: https://arxiv.org/abs/2602.12275
[arrow]: https://arxiv.org/abs/2405.11157
[glam]: https://arxiv.org/abs/2509.13211
[ctm]: https://arxiv.org/abs/2606.03723
[latent]: https://arxiv.org/abs/2607.23837
[fedrep]: https://arxiv.org/abs/2102.07078
[sisa]: https://arxiv.org/abs/1912.03817
[del]: https://arxiv.org/abs/2602.18505
[inf]: https://arxiv.org/abs/2404.00228
[ogd]: https://arxiv.org/abs/1910.07104
[alpha]: https://arxiv.org/abs/2410.02355
[null]: https://arxiv.org/abs/2512.15233
[rls]: https://arxiv.org/abs/2601.15686
[clora]: https://arxiv.org/abs/2502.17920
[ada]: https://arxiv.org/abs/2303.10512
[palo]: https://arxiv.org/abs/2610.04226
[oml]: https://arxiv.org/abs/1905.12588
[vera]: https://arxiv.org/abs/2310.11454
[olora]: https://arxiv.org/abs/2310.14152
[maxmin]: https://arxiv.org/abs/2402.08925
[vpl]: https://arxiv.org/abs/2408.10075
[micro]: https://arxiv.org/abs/2505.24846
