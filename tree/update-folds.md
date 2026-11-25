# Update-preserving fold-backs: return width without changing the next lesson

**Status:** Ideas only; no pilots, training runs, or GPU work. **Parent:** [Window splits](window-splits.md) ([PR #228](https://github.com/manojbajaj95/cl/pull/228)). **Review seed:** [Flood triage row 340](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L340), two score-3 cards: #07 only counts width as returned when the reduced model takes the same next learning step in output space for a declared update class; #20 pre-places opposite-signed pieces so two learners cancel otherwise unrepresentable kinks and return width exactly.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). The coded-interference kill rules out a fitted proxy as proof of cancellation. The retention-matched reserve rerun requires a real spread in useful next writes before ranking folds; the Noether-memory kill warns against treating a gradient-flow invariant as a finite-step optimizer invariant. Use a [μP control](https://arxiv.org/abs/2506.16884) when training wider references. **P** denotes a candidate reusable operation; **I** an improvement or falsifier. A P is not a priority claim or a pilot recommendation.

## What would be new?

[Net2Net](https://arxiv.org/abs/1511.05641) and [Exact Network Surgery](https://arxiv.org/abs/2607.16568) preserve the function when growing a network; the latter preserves unaffected optimizer state and makes the insert trainable. [Cut Less, Fold More](https://arxiv.org/abs/2602.18116) folds by weight clustering for deployment, and [Neural Compression over Equivalence Classes](https://arxiv.org/abs/2611.07233) uses equivalent representations for cheaper encoding. None of these comparisons by itself buys exact agreement with the **unfolded** optimizer's next output after a drifted merge. Exact state aggregation (the deterministic analogue of [lumpability](https://doi.org/10.2307/3215235)) already gives the mathematical test; applying it to tied duplicates is not the research result.

[CAMFT](https://arxiv.org/abs/2609.22253) trains sparse updates to reduce conflict, [TIES](https://arxiv.org/abs/2306.01708) elects parameter signs after training, and [paired counterweights](https://github.com/manojbajaj95/cl/pull/208) already cancel joint effects. [ReLU identifiability](https://arxiv.org/abs/2606.04754) supplies geometric obstructions to equivalence. Summing opposite spline atoms at the same knot is ordinary algebra. The candidate primitive is a **precommit placement and continuation certificate**: independently trained branches can remove an actual width obstruction without disclosing magnitudes in advance, and the merger can delete both the shards and their private optimizer slots without changing what a later independent learner gets from an authorized write. The alphaXiv search and targeted PDF excerpts inform these comparisons; they are not a claim of priority.

## Refund contract

- Fix the host, peak and terminal widths, merge rule, domain D, old-task floors, new-task utility, update class U and arithmetic before the window opens. Each u in U binds a batch/loss, trainable mask, hyperparameters, and any stochastic inputs (or a predeclared coupling). Use the same training signal and the actual permanent-split policy as the unfolded reference; a change to that policy is a separate experiment. Any learning-rate or state conversion on the narrow host must be a fixed lawful rule, not chosen by seeing the reference's answer to u.
- Write s for merged wide state (weights, slots, and any other state that affects learning), F(s) for the fold, Tᵤ for the wide step and Sᵤ for the narrow one. Require f(s) = f(F(s)) and f(Tᵤ(s)) = f(Sᵤ(F(s))) on D for **every** u in U at an admitted s. Include reachable precision, RNG and mutable-buffer behavior if in scope. If the right side is identical for two states with the same F(s) but the left sides differ for one u, the proposed fold cannot work. For a reusable receipt additionally require F(Tᵤ(s)) = Sᵤ(F(s)) on an invariant reachable set, or prove an equivalent relation closed under the steps; equal outputs at the first step alone do not imply closure.
- Before training, exchange only receiver IDs and sign certificates keyed to the public host. Exact knot, amplitude or optimizer-state ties must follow from that host, or be checked at commit with a fail-closed scope; if a tie is merely checked, report the refusal rate and do not claim that all pre-admitted commits are guaranteed. Signs alone don't establish equality. The actual updates still reach the merger. Track A/C (old tasks), B and P (both new partners' skills) separately from equality, from the parent's mixed residual, and from any further gain on a third task. Check old tasks at window, commit, fold and actual permitted continuation; matching a wide reference that forgets is not success.
- Count a slot only once its weights, optimizer memory and other live readers can be released and a real third writer can use the resource. Report matching the reference during U and subsequently using the released slot as separate checks; if reuse itself is in U, specify the corresponding wide action and compare the two. Charge peak width, width-steps, state/proof bytes, verification, refused commits and deadlines. Stack exact function-only narrowing + legal state transport/reset + ordinary merge-aware training/counterweights + exact recertification as the main control; also include permanent split and wait-for-commit plus exact fold at matched information and solo scores. Give a full-information search only as an oracle. Reject wins based on a frozen/no-op U, a narrower D, poorer retention, or storing the deleted state in a cache.

## Two paper witnesses (not pilots)

**W1 — The next update sees a moment that the function cannot see.** Freeze one nonzero feature h(x) = [x]₊ with two read-out copies a₁ and a₂. The wide output is (a₁+a₂)h. Let U be any finite batch with differentiable loss in the output, and common scalar momentum recurrence vᵢ′ = βvᵢ+g with aᵢ′ = aᵢ−ηvᵢ′. Here g is the same scalar derivative for each wide copy. The narrow state is a = a₁+a₂, v = (v₁+v₂)/2, with v′ = βv+g and a′ = a−2ηv′. The sum of the wide weights and average of the new slots agree with the narrow ones, so the equality iterates. If β ≠ 0, two same-output wide states with different moment sums disprove the reset fold (choose a zero-gradient batch to isolate this). Even with reset moments, a nonzero g disproves using the old learning rate unchanged. If U grants arbitrary per-copy updates unseen by the narrow learner, equal starting state and batch need not determine the wide next output. This witness is an exact control, not evidence that useful untied features can be folded.

**W2 — Removing the kink must survive a legal update, not just the merge.** Let D = [−1,1], hₜ = [x−t]₊ for a public −1 < t < 1, and suppose the host already has an affine path with terminal budget zero hinge slots. In the shared two-slot window, branches can choose which of two identical receivers holds their signed read-out. Their useful affine contributions are c_B x and c_P x, with c_B,c_P > 0. On the public host each branch's unsigned shard amplitude is the same nonzero q, fixed before training. Place +q and −q on *distinct* receiver IDs; with additive merge the result is (c_B+c_P)x + qhₜ−qhₜ. Each unilateral function has a nonzero interior slope jump, so cannot meet the terminal budget; the joint output can. Distinct IDs are needed to test dropping physical slots rather than just zeroing one sum, not to make coincident hinges cancel. Same sign, or a rational nonzero knot displacement inside D, leaves nonzero slope jumps. For this witness the scoped U trains the shared affine coefficient by ordinary SGD; it can also issue identical tied changes to the two knots (while interior) without changing their cancellation. All affine gradients match, so the hinge pair and any state used only for its tied motion can be dropped. Under an authorized independent finite change to one knot, or one read-out, the hidden component can reappear and the refund fails. For a toy retention floor take A: x = −1 maps negative, C: x = 1 maps positive; keep c_B+c_P positive in the tested suffix and 0 < q(1−t) < min(c_B,c_P) for solo retention. This shows the obstruction and a nonzero surviving output, **not** independent task acquisition or superiority to dropping terms upstream: test two independently scored skills and a binding pending duty for that claim.

## Idea cards

### What must the narrow learner remember?

#### 01. Return width only against a named update class (P)
- **Mechanism:** Make F, U, S and the released resources part of the receipt; issue nothing for an equal function with a missing state image.
- **Novelty vs nearest prior art:** Restates #228#07; Exact Network Surgery keeps unaffected slots, whereas this deletes changed slots only if next-update equivalence is proved.
- **Cheapest first test:** Enumerate rational W1 batches and moments; compare averaged slot transport, reset, exact function-only fold and permanent split. Include a nonzero-gradient batch and misspecified learning rate.
- **Old-task retention check:** Test A/C and B/P on the commit, fold and two nonzero-gradient suffix steps at matched progress.

#### 02. Find the smallest sufficient optimizer slot (P)
- **Mechanism:** Partition same-function wide states by their response to all permitted batches. Keep only the smallest statistic that separates next-output classes and fits existing narrow storage.
- **Novelty vs nearest prior art:** Exact lumpability supplies the equivalence test; the candidate is a width-and-state receipt that can certify a lower bound on continuation memory, not just compression.
- **Cheapest first test:** Enumerate a finite fixed-feature momentum state space, construct the exact partition, and compare keeping sum, reset, and copying all slots at equal state bytes.
- **Old-task retention check:** Include a slow A/C probe whose first error distinguishes two aliased moment sums; retain B/P through the next useful step.

#### 03. Refuse Adam folds using a single distinguishing batch (I)
- **Mechanism:** For same-function states with the same candidate moment summaries, seek a batch whose next step differs because the per-shard denominators differ.
- **Novelty vs nearest prior art:** [Adam](https://arxiv.org/abs/1412.6980) already normalizes each coordinate independently; this is an obstruction to a proposed state image, not a new optimizer.
- **Cheapest first test:** Assign twin slots second moments (1,9) or (5,5), with equal nonzero first moments and equal counters. Try zero and nonzero gradients; compare next-output algebra with pooling moments and keeping both slots.
- **Old-task retention check:** Put A/C near a decision boundary separating the two witness outputs; on refusal keep the last lawful model and confirm B/P remain.

#### 04. Trade state bytes for a broader learner, not for identically frozen width (P)
- **Mechanism:** Publish a Pareto set of legal narrow optimizer maps with different continuation summaries and incomparable update classes; let a later writer choose without knowing the removed weights.
- **Novelty vs nearest prior art:** Compression over equivalence classes prices representations; a menu priced by which future jobs it can execute rather than which current outputs it encodes is the candidate.
- **Cheapest first test:** Enumerate scalar momentum folds on two read-out groups, comparing exact finite-state minimization, a fixed all-purpose summary and a byte-matched cache; reveal the third job after the menu is published.
- **Old-task retention check:** Check A/C and B/P for every advertised job, then replay the selected job and its newly acquired behavior.

#### 05. Certify an update across a gate crossing (P)
- **Mechanism:** Refine cells in joint input × update space so cancellation is checked before and after the optimizer moves a gate; don't replace a finite step with a tangent.
- **Novelty vs nearest prior art:** [ReluDiff](https://arxiv.org/abs/2001.03662) compares networks; the candidate receipt applies the paired-function proof to optimizer-generated endpoints, including changed active sets.
- **Cheapest first test:** Enumerate rational one-step changes of tied and almost-tied knots. Compare exact cell enumeration, Jacobian equality, and an exact checker rebuilt for each admitted job.
- **Old-task retention check:** Include old inputs in each reachable cell, at the moving breakpoints and on both sides; check B/P at the same endpoint.

#### 06. Share the optimizer's random event, not its private history (P)
- **Mechanism:** Bind a public randomness coupling to matching fold groups. Distinguish samplewise equality under the coupling from equal expected predictions.
- **Novelty vs nearest prior art:** Common random numbers and correlated dropout are known; the candidate is a valid return under an existing stochastic policy, not after silently replacing independent shard masks.
- **Cheapest first test:** Enumerate all two-bit dropout masks on twins; test whether a narrow action of the same law can reproduce wide steps on A/C. Price every extra latent bit and use exact distribution matching as a control.
- **Old-task retention check:** Compare worst-event A/C and B/P as well as averages; an expectation match cannot earn an exact refund.

#### 07. Build the largest safe continuation language (P)
- **Mechanism:** Refine one-step output classes under legal action sequences, and advertise only update sequences that stay in the quotient relation, rather than assuming every individually allowed step composes.
- **Novelty vs nearest prior art:** State minimization and [precondition writes](https://github.com/manojbajaj95/cl/pull/158) already support guarded sequences; use them to return width without retaining a wide fallback between certified steps.
- **Cheapest first test:** Make two slots differ only in hidden velocity exposed after a first read-out-only step by a later mask change. Compare reachable-state partition refinement, two per-step recertifications and a fixed mask.
- **Old-task retention check:** Check A/C and B/P at every admitted prefix, including the shortest prefix rejected only by the sequence guard.

#### 08. Use an independently callable no-refund witness (I)
- **Mechanism:** Return a pair of wide legal states indistinguishable through the proposed fold, plus one public batch and one input on which the wide next outputs disagree.
- **Novelty vs nearest prior art:** Counterexample-guided abstraction and the parent's no-refund breakpoint already supply the method; this translates it into a finite-step optimizer falsifier.
- **Cheapest first test:** Produce rational W1 reset counterexamples and W2 with divergent knot motion. Compare the witness checker with brute enumeration and measure false acceptances on an endpoint-only checker.
- **Old-task retention check:** Confirm A/C remain served and B/P are not dropped on refusal; include an old query that distinguishes the putatively equal continuations.

### What must partners agree before they learn?

#### 09. Sign/ID placement that deletes a genuine width obstruction (P)
- **Mechanism:** Bind opposite-signed placements to public compatible receivers before training, then sum signed slope jumps at each actual interior knot and release the obstruction slots only when every required sum is zero.
- **Novelty vs nearest prior art:** Restates #228#20. TIES aligns parameter signs and #208 cancels residuals; the claim needs an exact terminal-width separation, not just a lower interaction score.
- **Cheapest first test:** Use W2 with same-sign, displaced-knot and unilateral controls, then add a pending duty that cannot delete the shards immediately. Compare wait-and-narrow and upstream cancellation plus exact folding.
- **Old-task retention check:** Check A/C at all lifecycle stages and B/P with separate skill probes; reject a merge that merely cancels the two learned skills.

#### 10. Negotiate with signed vector jump matrices (P)
- **Mechanism:** For a shared gate in a multi-output model, place each branch's jump in a publicly admissible output direction. Permit cancellation of forbidden components in the sum without canceling the components used by either new skill.
- **Novelty vs nearest prior art:** Multi-task merging and ReLU identifiability already compare output effects; test a public placement that projects nuisance effects away exactly without spending more output channels or learning joint magnitudes.
- **Cheapest first test:** On a three-output spline, have partners carry opposite jumps on a nuisance channel and affine utility on distinct channels. Compare scalar sign election, exact post-merge compression and private isolation at equal width; rotate one jump as an adversarial control.
- **Old-task retention check:** Probe old A/C on all heads and boundary cells; inspect B/P on their separate heads after fold and a third write.

#### 11. Make one public controller tie both position and motion (P)
- **Mechanism:** Derive shard knots and signed read-outs from public host coordinates during the window and specify which updates must move both together. Scope authorization to the tie rather than reintroducing a removed kink via an untied slot.
- **Novelty vs nearest prior art:** Weight tying and #228's tied rays cover shared position; the candidate coordinates return and optimizer transport for independently learned affine or surviving components around the tie.
- **Cheapest first test:** Enumerate a W2 tie and a commit at the same positions with unequal velocities. Compare shared-controller, merge-time-only knot equality, and freezing the entire hinge bank, including whether that freeze can meet the pending duty.
- **Old-task retention check:** Test A/C around the moving knot, and check both new skills before admission and after a useful update.

#### 12. Prove what sign-only messages cannot promise (I)
- **Mechanism:** Generate two commits indistinguishable before placement: one has matching jumps, the other a displaced knot or unequal amplitude. Record which additional public tie or abort is necessary.
- **Novelty vs nearest prior art:** #228's sign-only contract and indistinguishability already predict this; the audit separates guaranteed return from post-commit selection.
- **Cheapest first test:** Enumerate rational hidden magnitudes with identical ID/sign transcripts; compare sign-only, public architectural ties and a magnitude-aware oracle, and count refusals rather than filtering to successes.
- **Old-task retention check:** Check A/C and already installed skills on the refusal path and on the accepted commit after its next update.

#### 13. Return capacity even when some sites don't cancel (P)
- **Mechanism:** Reserve terminal slots by exact surviving knot count and map the remaining knots to narrow writable receivers; two partners may cancel just the jumps that exceed the cap.
- **Novelty vs nearest prior art:** Partial fusion and exact spline compression choose what survives after observing the merge. The distinction is whether a blind placement can guarantee a writable surviving layout across multiple commits.
- **Cheapest first test:** Enumerate four rational knots, one terminal hinge slot and two hidden commit types with different surviving knots. Compare one fixed blind placement, one-sided folds, and late-choice exact narrowing.
- **Old-task retention check:** Verify A/C at all four knots and B/P after the surviving hinge is moved by an authorized job.

#### 14. Certify cancellation only where the partner can actually act (P)
- **Mechanism:** In a two-layer host, bind signed pieces to shared downstream activation cells; use equality of output jumps on each reachable facet rather than preactivation signs.
- **Novelty vs nearest prior art:** #228#21 asks for a downstream response relation; the added test is that the relation is enough for the next learning step, not only the merge output.
- **Cheapest first test:** Enumerate activation cells for rational weights in a two-layer two-input ReLU net. Include a commit where matching first-layer knots sit behind different downstream masks; compare exact paired verification and frozen downstream updates.
- **Old-task retention check:** Track A/C in exposed and shielded cells and B/P following an authorized downstream update.

#### 15. Allow canceling mixed terms without sacrificing solo behavior (P)
- **Mechanism:** Place a redundant opposite pair per solo branch that cancels on its own input domain. Cross-branch shifts expose the two nuisance terms, which must cancel jointly on the merged domain and remain canceled under U.
- **Novelty vs nearest prior art:** The parent's W2 already hides potential mixed terms; this candidate asks whether the *update effects*, not only the mixed predictions, can vanish while both learners retain distinct new skills.
- **Cheapest first test:** Use two rational receiver banks and exhaust ternary solo-equivalent placements and tied partner drifts. Compare #215 reciprocal placement followed by an exact folder, plus a full-information oracle; require a useful nonzero narrow suffix.
- **Old-task retention check:** Test A/C on solo and merged domains, and B/P separately before and after one authorized update on the other learner's slice.

#### 16. Check deployed cancellation where rounding is asymmetric (I)
- **Mechanism:** Define the arithmetic in the receipt; distinguish algebraic cancellation, exact deployed outputs/updates, and bounded discrepancy.
- **Novelty vs nearest prior art:** Exact Network Surgery already states bit-exact hypotheses and #228#10 proposes this comparison for function refunds. Test full optimizer steps and keep approximate return a separate result.
- **Cheapest first test:** Work through low-bit round-to-nearest examples with both addition orders, e.g. adding 1 to a large positive term before adding its negative. Compare a shared accumulator, exact rational arithmetic and tolerance pruning; include softplus where shifted nonidentical pieces can't be judged by ReLU knot counts.
- **Old-task retention check:** Probe A/C at near-ties and B/P after a low-precision nonzero step; report label flips separately from narrow-vs-wide numerical mismatch.

### Can the two certificates buy something together?

#### 17. Pre-place for cancellation after the step, not just before it (P)
- **Mechanism:** Pair receivers by how each authorized batch changes their signed contributions; select a placement that cancels initial jumps and their finite post-step images. Park returning shards on a public orbit only if the pending duty and useful next step still work.
- **Novelty vs nearest prior art:** CAMFT shapes mergeability and the parent handles commit-point cancellation; the candidate targets a strict intersection of exact width and usable next-step maps at the same deadline.
- **Cheapest first test:** Make two opposite placements identical at commit but only one tied under the designated suffix. Compare best exact merge-then-fold with state transport, permanent split and a publicly tied architecture without negotiation.
- **Old-task retention check:** Include A/C inputs near the otherwise reappearing knot; require separate B/P retention and real suffix gain.

#### 18. Fit a third learner into the returned resources (P)
- **Mechanism:** Redeploy the freed bank for a blind third job, after checking continuation on the installed model. Use an explicit embedding of the same third action in the wide reference if claiming its behavior is matched too.
- **Novelty vs nearest prior art:** [PackNet](https://arxiv.org/abs/1711.05769) frees parameters to reuse; #228#06 wants a writable receiver. The claim here is useful reuse after an exact optimizer-aware return, not mere zero coefficients.
- **Cheapest first test:** Three jobs on disjoint rational intervals, with the third requiring a hinge at a fresh revealed location. Compare exact restarts, permanent split, isolation and return under the same peak cap and frozen third-job template.
- **Old-task retention check:** Require A/C and B/P before the third job, after every admitted step, and at its matched final utility.

#### 19. Compose two partner receipts without restoring wide state (P)
- **Mechanism:** Let a later pair operate directly on a previous narrow representative and carry forward only its lawful optimizer image. Reject if the next merge reads distinctions already discarded by the first fold.
- **Novelty vs nearest prior art:** Two-phase releases and compositional verification already check interacting writes; the candidate is deletion of the wide checkpoint without losing an otherwise admissible continuation class across successive merges.
- **Cheapest first test:** Enumerate two W2-style windows sharing a read-out group. Compare serial return, overlapping admissions, independent receipt checking and exact joint recertification. Include a second merge that distinguishes members of a previous fold fiber.
- **Old-task retention check:** Check A/C and both first-round skills through the second fold, plus both second-round skills after the suffix.

#### 20. Sell the return only if the pending duty uses the soon-deleted shard (I)
- **Mechanism:** Remove the provisional reader in an ablation. A late binder or exact upstream cancellation should tie whenever no useful action depends on the shard before commit.
- **Novelty vs nearest prior art:** #228#08 already tests the deadline. This audit couples that rule to the declared optimizer policy so a temporary, inert widening doesn't get credited as a learning primitive.
- **Cheapest first test:** Construct a frozen decision with a pre-commit deadline and hidden partner ID; compare early paired placement, defer, precommit a narrow policy and exact late binding, with/without the reader and matched proof bytes.
- **Old-task retention check:** Keep A/C valid during the required provisional action, at timeout, and after admitted B/P and the subsequent useful update.

#### 21. Extract the bottleneck from failed joint placement (P)
- **Mechanism:** A conflict report distinguishes unmatched post-merge knots from a non-lumpable optimizer fiber. Search the smallest public receiver or update-class relaxation that fixes the specific obstruction without exposing branch magnitudes.
- **Novelty vs nearest prior art:** Unsatisfiable cores and [guard repair](https://github.com/manojbajaj95/cl/pull/160) already locate conflicts; the claim is a reusable repair that serves a later hidden partner while still returning capacity.
- **Cheapest first test:** Enumerate small infeasible spline merges with one spare public tie and one optional mask rule. Compare minimal-core repair, brute-force fresh search and ordinary counterweights plus state reset at equal information.
- **Old-task retention check:** Preserve A/C and installed B/P on refusal and rerun them after the repair and a different admissible partner's update.

#### 22. Demand a strict gain over the stacked controls (I)
- **Mechanism:** Cross pre-placement vs no pre-placement with update-aware vs function-only folds, enforcing the same U in all arms; score complete useful admissions and terminal width/state, not isolated algebraic wins.
- **Novelty vs nearest prior art:** This is the ledger's stacked-control rule made specific to #228#07/#20; a matched exact merge-and-fold tie kills the joint novelty claim.
- **Cheapest first test:** Exhaust rational toy streams with at least two committed pairs, one non-canceling attempt and a third job revealed after return. Compare the best admissible stack, permanent split and the full-information oracle separately; report counts by obstruction and width-steps.
- **Old-task retention check:** Match worst-prefix A/C and all previously admitted skills at matched new-task utility. Count a refused or delayed job, continuation mismatch or forgotten skill as no complete admission.

## Ranked deeper questions

1. **Can pre-placement buy a useful third write that exact merge-then-fold with state transport cannot?** Start with 17, 18 and 22. Hold the pending deadline, U, peak width, information and retention fixed; require a nonvacuous U with a useful job that was not known during placement. If the exact stacked control ties, neither algebraic identity is a new learning primitive.
2. **Where is the first unavoidable state-memory cost?** Use 02, 03 and 07. Classify the smallest optimizer summaries for SGD, momentum and Adam under the same allowed trainable masks. A counterexample should identify whether the missing information is in the fold, the optimizer or a mutable reader; if the necessary state is as large as the discarded state, report a storage non-refund.
3. **What can two partners guarantee without disclosing magnitudes?** Use 09–12 and 15. Seek the weakest public relation that implies coincident, opposite jump responses both at commit and after useful finite steps. If all viable examples need magnitude exchange, exact joint training or a frozen/no-op continuation, narrow or drop the sign/ID claim.
4. **Can a receipt survive reuse and a second independent merge?** Use 05, 16, 19 and 20. Look for the first reachable gate, optimizer state change or arithmetic event that reopens an obstruction, and compare rechecking cost with exact recertification while keeping worst-prefix A/C and earlier new skills fixed.

**Verdict:** Keep both score-3 seeds as conditional candidates. W1 and W2 separate exact function return, optimizer-state return and cancellation; they do not show a useful independent admission advantage. Count width as returned only when the named update class agrees with the permanent split and real capacity is released. Look for a strict blind-admission win over exact folding with lawful state transport plus ordinary merge-aware training; stop if that stack ties.
