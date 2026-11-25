# Merge-window splits: return the width, keep the cancellation

**Status:** Ideas only; no pilots, training runs, or GPU work. **Parent:** [Partner-helping unit splits](partner-splits.md) ([PR #215](https://github.com/manojbajaj95/cl/pull/215)). **Review seed:** [Flood triage row 328](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L328) picks out two score-3 ideas: #07, split a gate only while its merge is pending, then refold the committed model without changing its function; #14, two learners pre-agree opposite-signed read-outs on the receivers the other will shift and publish only sign certificates and receiver IDs.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). A paper identity is not a retention or admission result. The killed coded-interference line rules out a fitted surrogate as proof; the plasticity-reserve kill demands measurable spread after matching retention; the width/laziness kill requires a [μP control](https://arxiv.org/abs/2506.16884) for trained width comparisons. Beat the best controls stacked at equal budget, not each in isolation. **P** means a candidate operation other methods could build on; **I** means an improvement or audit, not a pilot recommendation.

## What would be new?

- **A split with an enforceable return.** [Net2Net](https://arxiv.org/abs/1511.05641) widens without changing the function, [Exact Network Surgery](https://arxiv.org/abs/2607.16568) treats exact live insertion, [Neural Compression over Equivalence Classes](https://arxiv.org/abs/2611.07233) searches equivalent parameterizations for cheaper encoding, and [Partial Fusion](https://arxiv.org/abs/2605.22350) trades retained width against aggregation. The candidate operation isn't another fold. It buys blind merge admission with transient width and owes an exact return on the **actual merged function**, under every commit it pre-admits. [Fold-earned headroom](https://github.com/manojbajaj95/cl/pull/193) makes credits partner-indexed; [branch handshakes](https://github.com/manojbajaj95/cl/pull/212) and [escrowed paired leases](https://github.com/manojbajaj95/cl/pull/214) already supply deadline and reservation ideas.
- **A reciprocal cancellation interface with limited disclosure.** [CAMFT](https://arxiv.org/abs/2609.22253) makes fine-tuning merge-aware; [Decentralized Instruction Tuning](https://arxiv.org/abs/2606.01717) divides training to manage conflict and later reconciles weights. [TIES](https://arxiv.org/abs/2306.01708) elects parameter signs after training; [orthogonal gradient descent](https://arxiv.org/abs/1910.07104) projects updates to protect prior outputs. The candidate is a pre-training two-way contract where both learners deliberately create cancelling mixed terms, with neither solo function changed by the placement. [Joint releases](https://github.com/manojbajaj95/cl/pull/198) and [cancelling counterweights](https://github.com/manojbajaj95/cl/pull/208) already compose paired residuals; what must survive here is coordination from receiver IDs and sign certificates alone, given a frozen public host contract.

These are working novelty comparisons from an alphaXiv search and arXiv abstracts, not claims of priority.

### Contract and common first-test rules

- Fix base, additive merge operator, promised domain D, protected slices, old-task floors and new-task utility before a run. Use the parent's mixed residual R = f_AB − f_A − f_B + f₀ and J = sup_D |R|. Check tasks separately: small J alone does not imply retention. Widen only after opening a real pending merge against a declared partner class. The split is exactly solo-equivalent, and a commit is admitted only if there is a legal exact refold by the deadline with the same merged function on D. End the window on that commit and refold, or on a safe abort that restores the unsplit solo. A changed merge output or a forever-live split isn't a refund.
- Charge peak width, width × pending steps, stored parameters and optimizer state, proof/checkpoint bytes, and verification work. A zeroed receiver counts as returned capacity only when its resources can be reclaimed and the next permitted learner can use them without breaking tasks. Charge empty windows, overlap and aborts too. A pointwise identity in real arithmetic does not establish bit-exact deployment or suffix-training equivalence.
- Agree on receiver IDs and opposite-signed placements before training. Each branch publishes only IDs and sign certificates, bound to the frozen host and certified scope; the ordinary committed updates still reach the merger. No gradients, read-out magnitudes, drift magnitudes, learned envelopes, or hidden routing information are exchanged during coordination. If a magnitude relation or range is needed, it must follow from the public host contract fixed before either learner trains, not from the signs. Refuse or recertify after a sign flip; reduced disclosure is not a privacy guarantee.
- **Window controls:** permanent #204#01/#215 split, Net2Net then pruning, #204 single-receiver fold, fresh isolation blocks, post-merge correction, wait-for-commit + exact refold, and matched-μP width and solo scores. Include a commit that makes exact refold impossible. **Reciprocal controls:** #204#05 one-sided fold, CAMFT-style shared objective, TIES, orthogonal training, sign-uncorrelated and midpoint sign-flip partners. Compare against their best admissible stack with identical information, deadlines and retention floors; report a full-information oracle separately. Every retention check covers old A/C and each admitted new skill (B and partner skill where applicable) through the next useful suffix, not just the final merge.

## Two paper witnesses (not pilots)

**W1 — The narrow representative can depend on which partner commits.** On D = [−1,1] two twins u,v compute [x]₊ and branch A writes total read-out 1 over them. Each of two partners shifts exactly one receiver by −2 and has zero solo read-out there. Every blind one-receiver placement has worst J = 1 (the chosen receiver can go silent). The half-split gives J = 1/2 for either commit and never changes A's solo. On commit the shifted receiver is silent on D, so remove it and keep read-out 1/2 on the unshifted receiver: the actual merged contribution remains [x]₊/2. Both old-output paths are untouched if kept outside these receivers, and the new contribution is zero on the protected slice [−1,0]. Predeclare a committed new-utility floor that accepts [x]₊/2 but not zero; exact refold cannot repair a failed utility check. A −1/2 shift instead produces two nonzero interior slope jumps, at 0 and 1/2: no one-ReLU refold can preserve that contribution, even with a free affine skip. This is a hedge-and-return fixture, not a win over late binding: if the same decision can wait until commit, choosing the surviving receiver and matching the accepted function is cheaper.

**W2 — Signs direct the placement, but a public relation supplies the cancellation.** On D = [0,1], give each branch a disjoint receiver bank of twins [x]₊. In its bank a branch puts +2 on a forced receiver and −1 on a choice of two twins: the incoming partner shifts one, while the other remains clean. Each solo contribution is x regardless of that choice; its own shifts in the other bank have zero solo read-out. For each bank, the incoming partner shifts the forced receiver by t and the exposed twin by 2t, t > 0, via one public tied parameter; neither needs to disclose its t to the other. Choosing the exposed twin gives a mixed term 2t − 2t = 0, against 2t when choosing the clean twin. Do this reciprocally and R = 0 in both banks, so the merged output equals the additive ideal (which must itself pass old and new tasks). If the twin shift is independently configurable, t/2 has the same positive sign and ID as 2t but the mixed term becomes 3t/2. The signs did not prove the cancellation. At x = 0 both solos leave the base output intact, and the tied pair does too; the untied mismatch would change it.

## Idea cards

### Borrow width only while the merge is pending

#### 01. Hedge now, return the committed function (P)
- **Mechanism:** Admit a pending split only with a map from every pre-admitted outcome to a narrow representative of its merged function, not merely a reversible solo split.
- **Novelty vs nearest prior art:** #215#07 is the seed, not new; compared with Net2Net plus pruning, the candidate object is the pre-admission commitment to exact, outcome-dependent repayment.
- **Cheapest first test:** Play W1 with a real pre-commit deadline and partner choices revealed only after a joint obligation requires a placement. Compare permanent split, wait-and-refold and the window; count safe admissions and width-steps. If nothing needs a placement before commit, stop.
- **Old-task retention check:** A/C before and during the split, at each commit, immediately after refund, and after a useful suffix; require the declared B/partner floors where admitted.

#### 02. Refund on an activation proof, not twin identity (P)
- **Mechanism:** Partition commits by which shards can ever fire on D. A surviving shard and an affine bias may represent several drift classes even when no incoming weights are twins.
- **Novelty vs nearest prior art:** Exact Network Surgery supplies local equivalences; #215's twin fiber assumes proportional features. A prevalidated branch of the return map can key on activation regions rather than weights.
- **Cheapest first test:** Enumerate rational shifts on three twins and find the minimum exact width on their activation cells with and without a pre-existing affine skip; compare a twin-only folder and exact post-commit compression.
- **Old-task retention check:** Check A/C on boundary points and across all occupied cells before/after each allowed fold, and on held-out A/C after slot reuse.

#### 03. Purchase the earliest safe narrowing time (P)
- **Mechanism:** Design a split whose first certifiable narrow representative is triggered by a binding commit receipt that rules out some, but not all, drift possibilities before the update arrives. Release at commitment only if one fold works for every remaining possibility without changing any of their merged functions.
- **Novelty vs nearest prior art:** #214 leases and #212 deadlines track a right to act; the candidate geometry is a single exact fold over a shrinking partner class, not early release of an unverified right.
- **Cheapest first test:** Give three commit traces equal latency but different order of sign, scope and final revelation. Compare early exact elimination, full-commit waiting and a paid metadata oracle at equal information.
- **Old-task retention check:** Check A/C and new functionality for every remaining commit at early narrowing and for useful work before the final receipt.

#### 04. Choose the split by its worst-case return width (P)
- **Mechanism:** Optimize the maximum minimal post-commit width over the pre-admitted class subject to the same window J cap. A slightly worse split during the window can be the only one that clears the return budget.
- **Novelty vs nearest prior art:** #215's minimax LP selects coefficients by window J; compression over equivalence classes narrows a fixed function. The candidate objective selects a window policy against the width needed for *each possible* merged function.
- **Cheapest first test:** Exhaustively search ternary read-out shares and a finite partner set on one-dimensional ReLUs. Require a nonempty case where optimizing J first cannot return all borrowed slots while the joint objective can.
- **Old-task retention check:** Require A/C on the same inputs under all feasible splits at merge plus after refund, not only for the partner that minimizes width.

#### 05. Give an explicit no-refund witness (I)
- **Mechanism:** Expose an extra nonzero slope jump or, in a vector head, a jump rank that no admissible narrower architecture represents; output a counterexample rather than rounded pruning.
- **Novelty vs nearest prior art:** ReLU identifiability ([Beyond Structural Symmetries](https://arxiv.org/abs/2606.04754)) and exact compression already study equivalence; using their obstructions to reject a provisional admission is an audit.
- **Cheapest first test:** Apply W1's interior-kink commit, opposite-weight coincident jumps that do cancel, and a free affine skip. Compare a breakpoint witness with exact search and grid-only pruning.
- **Old-task retention check:** Confirm refusal serves A/C on the last lawful state, while the admitted coincident-jump control passes old tasks after actual narrowing.

#### 06. Return a writable receiver, not just a zero (P)
- **Mechanism:** After refold, embed the same merged function in a narrow host with an explicit free write direction for the next learner; reject folds that leave old readers dependent on the released slot via other paths.
- **Novelty vs nearest prior art:** #193 credits a current partner and [successor recovery](https://github.com/manojbajaj95/cl/pull/196) recovers a witness. What must be new here is using the same short-lived split to make a subsequent unseen write admissible without storing its payload.
- **Cheapest first test:** On the same merged function compare two exact folds with different free receiver IDs. Present a blind job whose legal writes are bound by ID; compare arbitrary exact folding plus full future recertification.
- **Old-task retention check:** Check A/C and first-pair skills unchanged under the actual successful next write, not just the zero at handoff.

#### 07. Refold both the function and its next update (P)
- **Mechanism:** Treat the refold as returning state only if the next authorized learning map agrees in output with the unreduced map on a declared update class; restrict to where a lawful optimizer-state image exists.
- **Novelty vs nearest prior art:** #212 changes optimizer bases at fixed width. Exact Network Surgery preserves insertion-time function while keeping parameters trainable; it does not by itself identify a quotient that commutes with continuation after partner drift.
- **Cheapest first test:** Work in one frozen ReLU cell with two shards, scalar momentum and tied gradients; compare push-forward, reset and permanent split on two useful gradient steps. Include independently directed gradients as an obstruction.
- **Old-task retention check:** A/C exactly at refund, then report paired retention and B learning through both suffix steps at matched utility.

#### 08. Spend the window on a genuinely blind duty (P)
- **Mechanism:** Bind a provisional representation to a required mixed evaluation or downstream obligation before the identity of the committing partner can be observed. Release at commit, not after an arbitrary training phase.
- **Novelty vs nearest prior art:** #212's live first move already binds a deadline; this candidate needs an obligation that reads the split-dependent merge residual, not just a scheduler that delays publication.
- **Cheapest first test:** Give pending W1 branches an external decision requiring a certified mixed bound; compare defer, precommit one fold, atomically select late, and temporarily split. Repeat with that reader disconnected to detect vacuity.
- **Old-task retention check:** A/C through the provisional evaluation, both legal commits and the subsequent actual job; provisional checks cannot count as new-task delivery.

#### 09. Reclaim width under overlapping commitments (I)
- **Mechanism:** Reserve peak width for jointly reachable open windows, and account for the actual order of exact refunds rather than crediting each pair separately.
- **Novelty vs nearest prior art:** #212#04 already binds overlapping handshakes and #214 recycles escrow; this is a width-specific falsifier, not a new scheduler.
- **Cheapest first test:** Simulate two W1 openings against one spare pool, with a joint trace that prevents either refund before the second opening. Compare per-window accounting with exact reachability and serialized reservations.
- **Old-task retention check:** Track old A/C and both earlier acquisitions on all admitted interleavings and on a timeout abort without dropping a committed skill.

#### 10. Make exactness face softer gates and real arithmetic (I)
- **Mechanism:** Separate exact return, bounded approximation and exact deployed arithmetic. Measure how often only ReLU inactivity or cancellation under ideal arithmetic supports a refund.
- **Novelty vs nearest prior art:** #215 already calls for a softplus audit; Exact Network Surgery calls out bit-exact hypotheses. This audit tests committed **narrowing**, not growth.
- **Cheapest first test:** Repeat W1 and its obstruction under softplus and a fixed-point implementation; keep exact and tolerance frontiers distinct, compare Net2Net then pruning, and match μP and solo scores if training is added.
- **Old-task retention check:** A/C at ReLU corners and near decision margins, before and after refund and one suffix; report tolerance-induced label flips separately.

### Pre-agree the signs, then make the mixed terms cancel

#### 11. Reciprocal placement without gradient exchange (P)
- **Mechanism:** Before training each learner commits to negative read-out on an ID the other certifies it will shift positively (or vice versa). Each placement is solo-equivalent; check both cross terms at the merge under the frozen host contract.
- **Novelty vs nearest prior art:** This is #215#14, not a novelty claim. The distinction from one-sided #204#05 and CAMFT is reciprocal mixed cancellation under a sign/ID-only interface.
- **Cheapest first test:** Cross W2's two placement choices in a 2 × 2 ablation. Compare one-sided folds, TIES, CAMFT-style coordination and orthogonal training with equal solo scores and communication; force a mid-training sign flip and require refusal.
- **Old-task retention check:** Recheck each learner's A/C before merge, merged A/C and both new skills, then the same tasks after the first useful suffix.

#### 12. Prove when sign-only coordination cannot work (I)
- **Mechanism:** Pair admissible completions with identical sign/ID transcripts but incompatible legal placements. No selector using that transcript can choose a common valid non-abstaining response.
- **Novelty vs nearest prior art:** [Obstruction bundles](https://github.com/manojbajaj95/cl/pull/194) already develop minimal counter-histories. This specializes the indistinguishability audit to two-sided mixed residuals.
- **Cheapest first test:** Give two exposed twins the same positive certificates and exchange which has drift 2t versus t/2 in two hidden worlds. With placements restricted to choosing one twin for the fixed negative mass, enumerate whether any common placement clears a predeclared cap below 3t/2; compare to a full-information oracle.
- **Old-task retention check:** Show rejected worlds preserve A/C on the current model, and evaluate A/C in the counterfactual bad admission at x = 0.

#### 13. Tie the ray, leave its amplitude learned locally (P)
- **Mechanism:** Make drift a learned scalar times a frozen receiver vector. Solve the solo-equivalent read-out against this vector beforehand, so cancellation is robust to any allowed amplitude without transmitting it.
- **Novelty vs nearest prior art:** Orthogonal gradient descent protects old outputs by projecting training; #208 cancels known residual parts. The question is whether a public drift parameterization can still learn useful local tasks while supporting reciprocal cancellation.
- **Cheapest first test:** Compare W2's rank-one ties, matched OGD and unrestricted CAMFT-style training on scalar regression tasks; vary whether the tasks need a component outside the ray.
- **Old-task retention check:** A/C and both new-task floors with the ray intact, plus an off-ray suffix as a negative control requiring refusal.

#### 14. Cancel to a fixed cap without exact magnitudes (P)
- **Mechanism:** Use predeclared public device limits to bound each signed term as an interval, then require the joint signed residual's entire interval inside the cap. If the box contains a lone cross term larger than the cap, forbid the pair.
- **Novelty vs nearest prior art:** #215's signed LP prices known partner classes; the candidate use is a contract with two blind learners and success despite privately chosen amplitudes, not rebadged interval arithmetic.
- **Cheapest first test:** Enumerate endpoints of fixed public amplitude ranges on W2, including independent ranges touching zero. Compare unsigned bounds, one-sided folds and exact joint verification.
- **Old-task retention check:** A/C at the worst residual endpoints and after a legal suffix that stays in the public ranges; match acquired-task performance.

#### 15. Share geometry across activation cells, not just signs (P)
- **Mechanism:** Use a frozen proportionality relation between the two response functions on a predeclared cell arrangement, and require a single read-out placement to satisfy all cells. Refuse if the activation thresholds break that relation.
- **Novelty vs nearest prior art:** #208#04 checks exact compensation over cells with a known counterweight; this card asks if a public architectural relation lets learners select compatible placements *before* knowing shifts.
- **Cheapest first test:** Extend W2 to x < 0. Compare an aligned public-threshold host, ordinary tied magnitudes with misaligned thresholds, and exact post-hoc signed folds.
- **Old-task retention check:** A/C at every protected breakpoint and on the newly added negative-input slice, before and after the useful suffix.

#### 16. Test whether the interface transports across unseen receivers (P)
- **Mechanism:** Freeze a rule from receiver IDs and certificates to compatible solo-equivalent placements, then relabel or recombine previously unused certified receiver banks without retraining the coordination rule.
- **Novelty vs nearest prior art:** #208 and [description partners](https://github.com/manojbajaj95/cl/pull/218) already test unseen addresses and cancellations. Here the specific wager is no description of drift beyond the sign certificate, and both sides must do useful work.
- **Cheapest first test:** Train on two bank pairings, freeze and test crossed held-out pairings and random ID relabelings. Compare an equal-byte lookup, reoptimization and CAMFT-style training at equal solo utility.
- **Old-task retention check:** A/C on held-out banks through merge and re-use; verify earlier bank-specific tasks still work, not only the newest pair.

#### 17. Measure how much the certificate actually discloses (I)
- **Mechanism:** In a small finite model, count transcript distinctions induced by ID choices, refusal and certificate publication. Treat any inferred amplitude or task information as disclosure, not transport for free.
- **Novelty vs nearest prior art:** #208#16 already considers hiding singletons; the audit detects whether claimed sign-only coordination is smuggling a magnitude through the receiver selection.
- **Cheapest first test:** Enumerate private tasks with identical intended signs; compare fixed ID policy versus magnitude-selected IDs, counting which tasks or magnitudes each transcript identifies. Do not claim differential privacy.
- **Old-task retention check:** A/C after merge under both ID policies; retain new-task floors so the low-disclosure policy cannot win by refusing all useful pairs.

#### 18. Stay safe when the earliest promised sign flips (P)
- **Mechanism:** Choose read-out placements with a second solo-equivalent fallback whose residual is provably safe when a precommit sign claim is voided, without passing extra training information.
- **Novelty vs nearest prior art:** #215#15 expires a sign claim, #212 fences readers, and #214 handles default. The candidate is a public fallback placement that preserves timely work rather than only detecting the breach.
- **Cheapest first test:** In W2 add one clean twin and a sign-flip trace. Compare local fallback, full abort and fresh one-sided recheck; include a trace where every fallback breaks the cap and must refuse.
- **Old-task retention check:** A/C at breach detection, after fallback or abort, and after a later admitted pair, with no damage to already installed skills.

#### 19. Try to explain the gain with ordinary sign election (I)
- **Mechanism:** Differentiate agreement of parameter deltas from cancellation of signed *output* effects by changing the receiver sign pairing while preserving the parameter-sign histogram and solo outputs.
- **Novelty vs nearest prior art:** TIES elects signs of parameter updates; #215 already separates signed bounds from unsigned ones. This is a confound test for the reciprocal claim.
- **Cheapest first test:** Swap exposed twin IDs in one W2 bank under equal parameter-sign counts. Compare TIES, one-sided folds and the reciprocal pair on exact J and new-task success.
- **Old-task retention check:** A/C on both sides of the crossover, including a protected input where residuals affect a decision, and after one suffix.

### Cross the two seeds without giving either a free win

#### 20. Cancel the breakpoints that prevent refund (P)
- **Mechanism:** Pre-agree placements so opposite signed shards cancel the *nonrepresentable* part of the committed function, leaving the useful narrow component. Neither unilateral cancellation nor a wider permanent model earns a refund.
- **Novelty vs nearest prior art:** #208 supplies paired counterweights and #215#07 supplies refolding. The new claim must be that sign/ID coordination expands the set of commits which can shed borrowed width exactly, not merely that it lowers J.
- **Cheapest first test:** Use W1's interior-kink refusal with a complementary branch able to create the same kink under a frozen tied gate. Compare both sides alone, the best independently chosen split-plus-cancellation stack, and a same-sign or displaced-kink commit. Require a nonzero narrow useful contribution.
- **Old-task retention check:** A/C throughout the window, for every admitted commit and refund, then while a third learner writes into the returned slot; keep both new contributions useful.

#### 21. Make a deep receiver contract survive downstream drift (P)
- **Mechanism:** Bind the sign to a receiver and a frozen downstream response relation, not just its preactivation. Use this to test whether shifts in different layers can support reciprocal cancellation and leave an exact narrow refold.
- **Novelty vs nearest prior art:** #215#06 splits upstream paths and [LR-Merge](https://arxiv.org/abs/2611.25000) forecasts interference with directional derivatives. A two-layer contract must certify the actual joint response, including newly crossed gates.
- **Cheapest first test:** Enumerate cells of a two-layer, two-input ReLU host; compare frozen-response, sign-only, derivative and exact post-merge controls. Include the same preactivation sign followed by opposite downstream output effects.
- **Old-task retention check:** A/C on each protected cell and on boundaries, checking both new skills after narrowing and after a downstream suffix update.

#### 22. Require an interaction on the returned-width frontier (I)
- **Mechanism:** Factor windowing and reciprocal placement independently. Ask whether the combined method admits functions under *both* a peak and a terminal width cap where either alone or their independent stack cannot.
- **Novelty vs nearest prior art:** The ledger's stacked-control rule and #198's joint-only frontier already set this standard. This is the go/no-go audit, not a third seed.
- **Cheapest first test:** Run the 2 × 2 on an enumerated W1/W2-style stream with at least three real consecutive merges, varying overlap and refusal outcomes. Compare same-width isolation plus exact recertification, stacked window plus one-sided repair, and a full-information optimizer reported separately. Require spread across commits rather than a hand-picked pair.
- **Old-task retention check:** Match A/C and every earlier skill at each pending stage, admission, refund and useful slot reuse; count a slipped deadline, forgotten skill or inactive no-op as no admission.

## Ranked deeper questions

1. **Does any real pending duty justify borrowing width before commitment?** Start with 01, 04 and 08. Show a strict safe-admission/width-step win over waiting plus exact narrowing, and reclaim a slot a later job actually uses (06). If late binding meets the same deadline, stop the lifecycle line.
2. **What is the weakest public host constraint that makes reciprocal sign-only admission sound and useful?** Try 12 before 13–16: rule out indistinguishable bad completions, then see whether architectural ties or ranges still leave room to acquire two real tasks. Otherwise the interface is either unsound or an expensive refusal rule.
3. **Can reciprocal cancellation buy an exact refund that neither seed buys alone?** Use 20 and 22. The deciding result is a strict gap over the matched stack, due to removing a width obstruction rather than paying for extra isolation, proof bytes, narrower domains or correction.
4. **Does the returned resource survive deployed arithmetic and subsequent learning?** Test 07, 10, 18 and 21. A fold that preserves one idealized ReLU frame but loses important tasks or usable optimizer state at the next ordinary update has not returned usable width.

**Verdict:** Keep both seeds as conditional candidates, not results. The first gate is a pre-commit duty that late binding can't serve; the second is a public response relation that makes the sign/ID contract sound without exposing magnitudes. If the best stacked control matches safe admissions, exact width return and A/B/C retention, neither seed earns a new primitive.
