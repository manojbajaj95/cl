# Minimal sufficient fold state: the least a narrow learner must remember, and the kinks it must keep

**Status:** Ideas only; no pilots, training runs, or GPU work. **Parent:** [Update-preserving fold-backs](update-folds.md) ([PR #239](https://github.com/manojbajaj95/cl/pull/239)). **Review seed:** [Flood triage row 352](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L352), two score-3 cards: #02 partitions function-equivalent wide states by their response to every permitted batch and keeps only the smallest statistic that separates next-output classes and fits narrow storage, a certified lower bound on fold-back memory; #13 reserves terminal slots for exactly the kinks that survive cancellation and maps leftovers to narrow writable receivers, so partners only cancel the kinks above the cap.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). Relevant rules: the Noether-memory kill (a gradient-flow invariant is not a finite-step SGD/momentum invariant, so every statistic here is checked under the actual discrete optimizer); the plasticity-reserve reruns (no ranking without a real spread in useful next writes); the predictor-pilot variance gate; "true by construction" kills (an exact restore or a threshold built into the toy is not a result); and the merge-card rule (beat the stacked baselines of each part). **P** marks a candidate reusable operation, **I** an improvement or falsifier; neither is a priority claim.

## What would be new?

The equivalence itself is classical. Myhill–Nerode state minimization, predictive state representations (Littman et al. 2001), bisimulation, and exact lumpability all identify states by their response to every future input. The closest recent paper is [Prediction Is Not a Sufficient Memory State](https://arxiv.org/abs/2610.13881) (2610.13881). It already proves that a memory reproducing all current predictions can lack the state needed for the next update. It gives exact continuation dimensions (ridge: dp + d(d+1)/2; on zero-prediction histories d(d+1)/2) and a finite-bit law. It covers exact cumulative learners and kernel attention, not finite-step optimizers on a folded network.

On the optimizer side, [Guarded Compression of Adam State](https://arxiv.org/abs/2611.00589) (2611.00589) accepts a coordinate's compressed moments only if the **first** restored Adam update stays within τ for every clipped gradient; later steps are only measured. [Backpropagated Output Momentum](https://arxiv.org/abs/2609.36738) (2609.36738) moves first-moment history into output space, with an exact batch-level comparison to AdamW. [AdamPM](https://arxiv.org/abs/2610.24598) pools moments to save memory, without an exactness claim.

On the kink side, [spline redundancies of 1-D ReLU nets](https://arxiv.org/abs/2207.14609), [exact compression by ReLU stability](https://arxiv.org/abs/2102.07804), [TropNNC](https://arxiv.org/abs/2409.03945), [NP-hardness of neuron minimization](https://arxiv.org/abs/2610.11313), partial fusion and [budget-aware LoRA merging](https://arxiv.org/abs/2609.22237) all count or allocate capacity **after** seeing the merged model. [TIES](https://arxiv.org/abs/2306.01708) and [CAMFT](https://arxiv.org/abs/2609.22253) shape the merge but return no certified width.

What remains open is narrower than either seed as written:

1. **Seed #02 restricted to finite-step optimizers on function-equivalent wide networks.** The question is which optimizer statistic must survive a width fold so that every permitted update class U gives the same next outputs, and when that statistic provably exceeds the narrow host's slots. That is a no-refund certificate tied to an optimizer, not a new state theory.
2. **Seed #13 restated at the update level.** The function-level survivor count is the wrong budget. A cancelled pair of trainable receivers is invisible in f but re-grows under the next SGD step (F2). So the terminal reservation must count kinks that survive U, not kinks that survive the merge. Blind pre-allocation of that count is the candidate; post-merge exact compression is the control it must beat.

## Contract

- Fix before the window opens: host, peak width, terminal width R, domain D, update class U (batches, masks, hyperparameters, arithmetic, stochastic couplings), horizon H, A/C floors, B/P utilities. A statistic σ is **U-sufficient** at admitted wide state s if f(s) and the outputs on D after every word u₁…u_H ∈ U^H are functions of σ(s) alone. It is **minimal** if every coarser σ' merges two states that some word separates. Write **capacity(narrow)** for the narrow host's slot budget: continuous dimension, or bits for finite arithmetic.
- **No-refund certificate:** a pair (or a smooth family) of reachable wide states, one word in U^H and one input. If the minimal U-sufficient statistic needs more coordinates or bits than capacity(narrow), no fold exists, whatever the decoder. **Refund receipt:** σ, a fixed lawful narrow optimizer map, and a proof that the narrow step matches the wide step on outputs for all of U^H, and is closed if H is unbounded. Do not tune the learning rate or state map after seeing the reference answer.
- **Kink reservation:** before training, publish R, receiver IDs and which receivers U may train. At commit, count the kinks that survive U, meaning nonzero slope jumps plus zero-sum knots whose receivers U still trains. Accept iff the count is ≤ R; otherwise refuse with the last lawful model kept. Report the refusal rate.
- Score A/C at window, commit, fold and each admitted step; B/P separately; peak width, width-steps, statistic bytes, proof cost and refusals. **Main stacked control:** exact post-merge function compression + best lawful state transport (sum/average/reset/guarded quantization) + recertification, at equal bytes and information. Full-information search is reported only as an oracle.

## Two exact fixtures (CPU, rational/symbolic arithmetic, not pilots)

**F1 — The sufficient statistic depends on the optimizer, not on the function.** Take twin read-outs a₁, a₂ on one frozen feature, so the output is (a₁+a₂)h. U is any batch sequence, and the twins always receive the same scalar gradient g. Compute the Jacobian rank of the vector of next-output changes with respect to the twins' slot state, over 7 rational g values × 2-step words (β₁ = 1/2, β₂ = 3/4; sympy):

| Optimizer on the twins | Rank of response map | Minimal U-sufficient statistic | Narrow slots | Verdict |
|---|---|---|---|---|
| Heavy-ball momentum | 1 | m₁+m₂ | 1 | refund (sum transport, lr ×2 as in the parent's W1) |
| Adam, untied second moments (m=(1/2,3/2), v=(1,9)) | 4 | unordered pair {(mᵢ,vᵢ)} | 2 | **certified no-refund** |
| Adam, tied history v₁=v₂ | 2 | (m₁+m₂, v) | 2 | refund |
| Lion-style sign update | discrete; m=(0,0), (−1,1), (−2,2) share Σm=0 yet give responses (−2,−2,−2,0,2,2,2), (−2,−1,0,0,0,1,2), (−2,0,0,0,0,0,2) on g ∈ {−3,−1,−½,0,½,1,3} | multiset {mᵢ} | 1 | **certified no-refund** |

The linear optimizer closes in narrow storage, and nonlinear per-coordinate optimizers do not unless their histories were tied. This parallels 2610.13881's polynomial/non-polynomial split, now for optimizer slots after a merge. The no-refund rows are lower bounds for any continuous decoder (rank argument), not just for the averaging maps the parent tested.

**F2 — Count the kinks that survive the update, not the merge.** Take D = [0,1], public knots t ∈ {1/5, 2/5, 3/5, 4/5}, a host affine term c·x with c = 1, R = 1 reserved receiver. Each partner has one receiver per knot. Commit X: B jumps (1,−1,1,1), P jumps (−1,1,0,−1); the only survivor is 3/5 with jump 1, so R = 1 accepts. Commit Y: P = (−1,0,0,−1) leaves survivors {2/5: −1, 3/5: 1}, so it is refused. Take one SGD step (η = 1/10, squared loss at x₀ = 9/10, y₀ = 0; equal residual 6/5) on X:
- **Full U (every read-out trainable):** the wide twins at each cancelled knot both move, so the cancelled kinks re-grow (jumps after the step: 1/5 → −21/125, 2/5 → −3/25, 4/5 → −3/125). No R = 1 narrow model matches it; outputs first differ at x = 1/4 by 21/2500. Under this U the terminal budget is 4, not 1.
- **U freezes cancelled receivers:** the single reserved receiver at 3/5 with lr 2η matches the wide step exactly on all 21 grid points; with lr η it does not.

So seed #13's survivor count is only valid when U is declared, and the reservation contract must say which receivers stay trainable. This is a bookkeeping fact, not yet an advantage: exact post-merge compression gets the same R = 1 on X. A reservation earns credit only if a blind, pre-allocated R is what lets the pending duty or third writer act before the merge is observed.

## Idea cards

### A. Finding and certifying the minimal statistic

#### 01. Optimizer-indexed fold certificates (P)
- **Mechanism:** For each optimizer family, publish the minimal U-sufficient statistic for twin, k-tuple and near-twin fibers: sum for momentum, tied-history pair for Adam, multiset otherwise. Issue fold receipts only from this table.
- **Novelty vs nearest prior art:** 2610.13881 classifies exact cumulative learners; 2611.00589 guards one Adam step per coordinate. A closed table for finite-step optimizers on width folds, with lower bounds, is not in either.
- **Cheapest first test:** Extend F1 symbolically to SGD, Nesterov, Adam, AdamW (decoupled decay), Lion and Adafactor's factored v, for k = 2, 3 twins and H = 1, 2, 3. Report the rank and a witness pair for each no-refund case.
- **Old-task retention check:** For each witness pair put an A/C probe whose decision flips between the two continuations; A/C must hold on the narrow model under every refunded word.

#### 02. Partition refinement on the reachable set, not the whole slot space (P)
- **Mechanism:** Run Moore/Hopcroft refinement over **reachable** wide states, as produced by the actual merge and training history, under finite U in exact arithmetic. The number of classes is the certified bit lower bound; compare it with the narrow slot's representable values.
- **Novelty vs nearest prior art:** This is classical DFA minimization. The novelty is that reachability under real training can make Adam's untied row of F1 vanish: if twins share history, v₁ = v₂ is invariant.
- **Cheapest first test:** On a 4-bit fixed-point momentum/Adam twin system, enumerate states reached by 3 branch histories followed by merge. Compute classes for H = 1…4 and check against the unrestricted-state partition.
- **Old-task retention check:** Re-run A/C after each admitted word for every class representative, including the representative chosen for the narrow model.

#### 03. Tie the history at birth so the fold stays cheap (P)
- **Mechanism:** When a unit is split for a window, give both shards a shared second-moment slot and only private first moments. F1's tied row then holds by construction at merge, and the fold needs Σm plus one v.
- **Novelty vs nearest prior art:** AdamPM pools moments for memory; here pooling is chosen to keep the post-merge minimal statistic within narrow capacity. Its cost in B/P learning speed is the test.
- **Cheapest first test:** Toy split-train-merge with private v vs shared v vs SGD-momentum. Measure B/P utility at window end and exact fold success.
- **Old-task retention check:** A/C at window end and after two post-fold steps for each arm; shared v must not buy fold exactness by hurting B/P below private-v at matched steps.

#### 04. Horizon-indexed refund prices (P)
- **Mechanism:** Publish the minimal statistic size as a function of H, the number of future steps certified. Sell a cheap H = 1 fold, as in 2611.00589, separately from an H = ∞ closed fold. The narrow learner states which horizon it bought and must recertify or widen after it.
- **Novelty vs nearest prior art:** Guarded compression stops at H = 1 with measured drift after; the parent's card 07 asks for closure. A priced menu by horizon is the candidate.
- **Cheapest first test:** In the 4-bit system of 02, plot classes vs H for momentum, Adam and clipped SGD. Find the first H where the class count exceeds narrow capacity.
- **Old-task retention check:** At H+1 after an H-certified fold, check A/C before the forced recertification; report any drift between expiry and recertification.

#### 05. Separate the statistic the function needs from the one the update needs (I)
- **Mechanism:** Decompose σ into σ_f (current outputs) and σ_u (extra continuation state, the r − d part in 2610.13881's notation). Report σ_u size per fold, since that is the true cost of keeping the learner ready.
- **Novelty vs nearest prior art:** This applies 2610.13881's split to width folds. It is an improvement in accounting, not a primitive.
- **Cheapest first test:** For F1 rows, compute σ_f (= a₁+a₂, 1 coordinate) and σ_u. Check that σ_u equals the rank minus 1 contributed by the function.
- **Old-task retention check:** Show that dropping σ_u keeps A/C at the fold but breaks A/C or B/P after one word; that is the falsifier the receipt must survive.

#### 06. Output-space history as the narrow slot (P)
- **Mechanism:** Fold the wide first moments into a BOM-style output-space EMA q = Σ wₜ sₜ, which is width-independent, and keep the per-parameter slot only where F1 says it is needed.
- **Novelty vs nearest prior art:** BOM relocates momentum for memory and generalization; using it as the fold-invariant carrier of continuation state across a width change is new. The test is whether it is sufficient, not just smaller.
- **Cheapest first test:** On the F1 twins plus a second untied feature, compare exact next outputs for parameter-momentum fold, output-momentum fold and reset, under a batch whose Jacobian differs from the history's.
- **Old-task retention check:** A/C after a deliberately shifted-Jacobian batch, where output-space history is known to omit the covariance term.

#### 07. Near-twin tolerance certificates (P)
- **Mechanism:** For wide states only ε-close to a refundable fiber, bound the next-output gap over U^H by a Lipschitz constant on the minimal statistic. Accept a fold if the gap is below a declared τ, and report exact and τ-refunds separately.
- **Novelty vs nearest prior art:** 2611.00589 does this for one compressed step per coordinate. The extension is the multi-step, cross-coordinate case created by a merge.
- **Cheapest first test:** Perturb F1 tied-Adam twins by v₂ = v₁(1+ε). Compute the exact H = 1, 3 output gap vs ε and compare with the bound.
- **Old-task retention check:** Check A/C margins against the certified τ and count label flips.

#### 08. Witness-search attack on proposed folds (I)
- **Mechanism:** Given a proposed σ, search U^H and reachable state pairs for the cheapest separating word. Report the shortest witness length as the fold's fragility.
- **Novelty vs nearest prior art:** This is CEGAR / the parent's card 08 applied as a falsifier to every card here.
- **Cheapest first test:** Run it against averaged-slot, sum-slot, reset and guarded-8-bit folds on the 4-bit system. Check the witness length against brute-force refinement.
- **Old-task retention check:** Each witness must name an A/C input whose output it changes; witnesses that only touch unused inputs are scored separately.

### B. Reserving end slots for the kinks that survive

#### 09. Reserve by U-survivor count, not f-survivor count (P)
- **Mechanism:** At window open, publish R and which receivers stay trainable after commit. A commit is accepted iff (nonzero jumps) + (zero-sum knots with a trainable receiver) ≤ R, as in F2.
- **Novelty vs nearest prior art:** Post-merge compression counts f-survivors only. F2 shows that count is wrong under full SGD; the update-indexed count is the candidate primitive.
- **Cheapest first test:** Enumerate all ternary jump pairs on 4 knots. Compare f-count reservation, U-count reservation and exact post-merge compression, for the full-U and frozen-cancelled-U classes.
- **Old-task retention check:** A/C at x = 0 and x = 1 plus probes at every knot after one and three post-fold steps; B/P on separate inputs.

#### 10. Cancel only above the cap (P)
- **Mechanism:** Partners agree in advance on a cap R and a public priority order over knots. Each partner only has to make its jumps cancel on knots ranked below the R-th survivor, so they negotiate fewer cancellations than full cancellation (#228#20).
- **Novelty vs nearest prior art:** This weakens #228#20's all-knots cancellation. The claim is that a public priority order lets blind partners succeed more often with the same information.
- **Cheapest first test:** Use random rational partner jump distributions on 6 knots. Measure acceptance rate vs R for full cancellation, ordered cap cancellation and post-merge compression, at equal information.
- **Old-task retention check:** A/C at all knots for accepted and refused commits; B/P after the reserved receivers take one useful step.

#### 11. Movable reserved receivers (P)
- **Mechanism:** A reserved receiver's knot bias is writable. At commit, map each surviving kink onto a reserved receiver by setting its bias, which preserves the function, and transport the merged twins' slots to it. The survivors' positions need not be known at placement.
- **Novelty vs nearest prior art:** Net2Net/Exact Network Surgery insert at chosen positions; here a pre-allocated slot is relocated at commit, and the receipt must include the bias slot's optimizer state.
- **Cheapest first test:** F2 commit X with the survivor at 1/5 instead of 3/5. Compare fixed-position reservation, movable reservation and post-merge compression, then do one SGD and one Adam step with bias trainable.
- **Old-task retention check:** A/C probes near the old and new receiver positions before and after the bias update.

#### 12. Leftover kinks onto writable narrow receivers (P)
- **Mechanism:** When survivors exceed R, map the extras onto existing host hinges whose positions are close enough to absorb them via a lawful bias+amplitude change. Accept only if the update class still matches on the absorbing receivers.
- **Novelty vs nearest prior art:** Spline knot removal does this approximately and post hoc. The candidate is an exact or τ-certified absorption with an optimizer receipt.
- **Cheapest first test:** Commit Y from F2 with one host hinge at 2/5. Exact absorption works; a host hinge at 1/2 gives a τ-absorption. Compare refusal, widening, and post-merge least-squares refit.
- **Old-task retention check:** A/C probes at knots displaced by absorption; refuse if any A/C probe moves beyond its floor.

#### 13. Freeze-on-cancel as part of the contract (I)
- **Mechanism:** Make "cancelled receivers are frozen in the wide reference too" an explicit clause, and measure what it costs B/P. That is what F2 needs for R = 1.
- **Novelty vs nearest prior art:** This is the falsifier for 09–12: if freezing the cancelled receivers in the reference hurts B/P as much as keeping them, the reservation buys nothing.
- **Cheapest first test:** Train B/P for 10 steps after commit with full U and with frozen-cancelled U. Compare utility and terminal width.
- **Old-task retention check:** A/C under both arms across all 10 steps; report the best-prefix and worst-prefix gap.

#### 14. Reservation menus for unknown commits (P)
- **Mechanism:** Publish several (R, trainable-mask, priority order) contracts. Partners choose one at commit, and the host pre-allocates the maximum R across the menu but returns the unused part.
- **Novelty vs nearest prior art:** Finish menus ([PR #222](https://github.com/manojbajaj95/cl/pull/222)) choose among finishes; here the menu prices terminal width against update freedom.
- **Cheapest first test:** Use the 6-knot random commits of 10 with a menu of R ∈ {1,2,3} × {full, frozen-cancelled}. Compare against the best single contract and the post-merge oracle.
- **Old-task retention check:** A/C for every menu item at commit and after one step; check that B/P under the chosen item match the contract.

### C. Joining the two seeds

#### 15. One budget: slots for state and slots for kinks (P)
- **Mechanism:** The narrow host has one byte budget shared by surviving kinks (receivers) and continuation state (σ_u). A fold receipt spends it on whichever mix keeps U-sufficiency, for example dropping a kink and keeping its moment, or the reverse.
- **Novelty vs nearest prior art:** Prior work prices weights and optimizer state separately. Trading them inside one certified budget is the candidate.
- **Cheapest first test:** F2 with Adam: compare R = 1 receiver + full per-receiver slots against R = 2 receivers + shared v at equal bytes, under the same U.
- **Old-task retention check:** A/C and B/P after 3 steps for each allocation; report which budget split loses first.

#### 16. Lower-bound the terminal width before training (P)
- **Mechanism:** From the public host, U and the partners' sign certificates, compute a worst-case minimal statistic + U-survivor count. Refuse to open a window whose certified terminal cost exceeds R.
- **Novelty vs nearest prior art:** Admission control on a certified bound is standard in scheduling. Applying it to merge windows, with a statistic taken from F1-style ranks, is new.
- **Cheapest first test:** Enumerate windows on the 4-knot host with sign-only messages. Compare predicted worst-case cost to realized cost over all commits.
- **Old-task retention check:** For refused windows, confirm A/C on the unchanged host; for opened ones, A/C at every stage.

#### 17. Kinks whose receivers carry history (P)
- **Mechanism:** A zero-sum knot whose twins have **non-cancelling momentum** re-grows even with zero gradient. Count it as a survivor iff its minimal statistic (F1) is nonzero.
- **Novelty vs nearest prior art:** This combines F1 and F2. It is not covered by function-only or gradient-only survivor counts.
- **Cheapest first test:** F2 commit X with momentum slots m = (+1/4, −1/8) on the cancelled 1/5 twins. Check a zero-gradient batch re-grows the kink, and that m = (+1/4, −1/4) does not.
- **Old-task retention check:** A/C at x near 1/5 over 3 zero-gradient steps; a refund that misses this must fail there.

#### 18. Fold a third writer into the returned state (P)
- **Mechanism:** After a certified fold, a third learner trains only on the narrow host. Its result must match the same job run on the wide reference, which shows the returned slots are genuinely usable.
- **Novelty vs nearest prior art:** The parent's card 18 asks this for width; here the third job also tests that the minimal statistic was sufficient for a job unseen at fold time.
- **Cheapest first test:** Run a third rational-interval task on the F2 host after folding X. Compare narrow vs wide outputs over 10 steps for SGD and momentum.
- **Old-task retention check:** A/C and B/P at every step of the third job; match worst-prefix A/C with the wide reference.

#### 19. Statistic transport across a second merge (P)
- **Mechanism:** A narrow model built from a minimal statistic enters a new window. The new merge must not need distinctions σ discarded. Certify this by checking that the second window's U is still within the first fold's sufficiency class.
- **Novelty vs nearest prior art:** This applies the parent's card 19 to statistics rather than weights; a gap is a quantifiable bits deficit.
- **Cheapest first test:** Tied-Adam fold followed by a second window whose shards get private v. Identify the first word that needs the discarded per-twin v.
- **Old-task retention check:** A/C through both windows; first-round B/P after the second fold.

#### 20. Charge the arithmetic (I)
- **Mechanism:** Recompute F1/F2 ranks and class counts in bf16/fp16 with fixed summation order. A refund in reals may become a no-refund in floats, or the reverse when rounding collapses classes.
- **Novelty vs nearest prior art:** 2611.00589 pins FP32 rounding for one step; the [slot-echo](https://github.com/manojbajaj95/cl/pull/229) node shows order-dependent rounding margins. This applies both to fold receipts.
- **Cheapest first test:** Enumerate the F1 momentum twin in binary16 with both addition orders of m₁+m₂. Report class splits and merges vs the rational case.
- **Old-task retention check:** A/C label flips separately from narrow-vs-wide numeric mismatch.

#### 21. Learn σ, then certify it (P)
- **Mechanism:** Train a tiny encoder from wide slot states to a k-dim narrow slot, supervised by the next outputs over sampled words. Then run 08's witness search. Accept only if no witness exists within the certified U.
- **Novelty vs nearest prior art:** This resembles learned optimizer-state compression. The certification step and the rank lower bound (k below rank means certain failure) separate it from fitted proxies, which the coded-interference kill rules out.
- **Cheapest first test:** On F1 Adam untied twins, train encoders with k = 2, 3, 4. Rank 4 predicts that k < 4 fails; check the witness search finds a separating word for k = 2, 3.
- **Old-task retention check:** A/C on witness inputs for every accepted encoder.

#### 22. Strict-gain bar against the stacked control (I)
- **Mechanism:** Cross {minimal statistic, sum/average, reset, guarded-8-bit} with {U-count reservation, f-count reservation, post-merge compression}, all at equal bytes, information and U. Score complete admissions, terminal width and width-steps.
- **Novelty vs nearest prior art:** This is the ledger's stacked-control rule applied to these two seeds. If post-merge compression + best transport + recertification ties, neither seed is a primitive.
- **Cheapest first test:** Exhaust the 4-knot ternary commits × 3 optimizers × H ∈ {1,3}, with one refused commit and a third job after return.
- **Old-task retention check:** Worst-prefix A/C and all admitted skills at matched utility; a forgotten skill is not an admission.

## Ranked deeper questions

1. **Does reachability make nonlinear optimizers foldable?** (01, 02, 03, 19) F1 says untied Adam and sign updates have no narrow refund, but tied histories do. The question is whether ordinary split-train-merge histories stay inside the tied fiber, or whether branches untie it in one step. If they always untie and tied-v costs B/P, seed #02 reduces to "use momentum or reset", and the lower bound is just a no-refund theorem in 2610.13881's style.
2. **Is the U-survivor count ever known blind?** (09, 10, 16, 17) A reservation is only a primitive if R can be fixed before training and still accept useful commits more often than post-merge exact compression at equal peak width and information. If it never accepts something compression cannot handle, it is bookkeeping.
3. **What does freezing cancelled receivers cost?** (13, 15) F2's R = 1 depends on freezing cancelled twins. If B/P need those twins trainable, the true terminal budget is the full knot count and no width returns.
4. **Do horizon-priced folds beat recertify-per-step?** (04, 07, 20) An H = 1 guard is already published. A multi-step certificate is worth it only if its cost is below repeated guarded steps plus recertification, under real rounding.

**Verdict:** Both seeds are conditional. F1 gives a real lower-bound tool: optimizer rank decides foldability, linear momentum folds, and untied nonlinear slots provably do not. The equivalence idea is already in 2610.13881 and PSR/Myhill–Nerode, so the candidate is the optimizer- and reachability-indexed table, not the theory. F2 corrects seed #13: count kinks that survive the update class, not the merge. Advantage over post-merge compression is still unshown. Next step, if any: question 1 on exact toy split-train-merge histories (CPU, minutes).
