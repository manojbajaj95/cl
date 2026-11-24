# Preview-aimed momentum and order-neutral rebatching

**Status:** Ideas only; no pilot, implementation, or GPU work. **Parent:** [Protective orders](protective-orders.md) ([PR #207](https://github.com/manojbajaj95/cl/pull/207)). **Review seeds:** [Flood triage, line 318](https://github.com/manojbajaj95/cl/blob/78c09a6263dafb1cad2c8afd9c6f53cca97c819c/reviews/flood-triage.md#L318) scores parent cards **02** (aim carryover using one preview of the next task) and **22** (change batch membership so every arrival order is safe) at 3. Read the [idea ledger](https://github.com/manojbajaj95/cl/blob/78c09a6263dafb1cad2c8afd9c6f53cca97c819c/reviews/idea-ledger.md) first.

The two seeds change different freedoms. **Preview aiming** selects one order of the outgoing window, at fixed seam weights, to cancel a specific incoming disturbance without editing optimizer state. **Rebatching** changes the partition of the incoming window, not its examples or batch size, so the loader need not promise an order. The first needs an informative preview and a reachable slot; the second needs a partition with a proof that survives weight and slot evolution.

## Contract and novelty boundary

- **One preview, one seam.** Before the outgoing window runs, admit one labelled B2 batch for one gradient evaluation at a predeclared, available checkpoint; charge the evaluation and waiting. If the checkpoint differs from the seam, include gradient-transport error in any guarantee. The preview is not trained on and is disjoint from both the hidden B2 suffix and evaluation. Keep full-lookahead and direct slot writes as separate oracles. Pin the optimizer, schedule, seam-weight target (relative to a reference order), and admissible prefix budget before seeing the preview. Once B2 starts, the shield cannot intervene. Prefer exact ties; for tolerance ties, cross weights and slots to separate their effects.
- **All orders means all orders of the declared atomic batches.** Use every original example exactly once, at the original batch size, with no reweighting. The guarantee does not cover different membership, omissions, duplicates, or within-batch randomness unless explicitly bounded. Charge buffering, per-example sketches, proof, checking, and fallback. At equal exposure, match B1 learning for aiming and B2 held-out gain for both. Record B2 step count, revision latency, and wall-clock; show a frontier when budgets cannot be matched simultaneously.
- **Freeze the protected reads.** Derive the A-sensitive projection from a design bank of logits/margins or loss functionals, not only a mean old loss gradient, which can vanish at an old optimum. Certify named reads and budgets, not an unseen population. Audit held-out ordinary and rare A and a stable control C pre-window, at every exposed prefix, at the seam, and after 10 B2 steps (and 50 total when claiming persistence). In the cards, “A/C” includes those checks where applicable.
- **Floors, not strawmen.** Carry the ledger’s bounded-delay kill, the parent’s constant-LR heavy-ball lock, margin matching, and a clock-matched optimizer ([shuffle-order analysis]). Compare shields with blind replay-last allowing free endpoints, partial [Adam reset], direct writes, and B2-time [GPM]/[FOGO] or [STABLE] damping. Compare rebatching with random and stratified partitions, [GraB] grouped into batches, pinning, and the parent’s certificate on the original batches. Use tuned gradient accumulation at equal latency for both: with an additive objective and no need for more or earlier updates, a single macro-step is order-independent by construction. Mark controls ruled out by the interface, not empirically beaten.
- **Prior-art boundary.** [GraB] balances discrepancies to select an order (including over examples); slicing it can already change batch membership. [FullCert] bounds training and inference under its data-perturbation model. [Per-sample interference] optimizes the update itself; [AdamW response] already derives signed horizon responses from slots; [Overshoot] evaluates current-batch gradients at lookahead *weights*, not on a sampled future task. The bets are **synthesizing** a fixed-membership partition with a retention guarantee over all its orders, and **realizing** a preview-selected response by past order alone at a fixed seam.

## Three pencil-and-paper fixtures

Use heavy-ball: `m⁺ = βm + g`, `θ⁺ = θ − ηm⁺`, `β = 1/2`. These fixtures check implications, not prevalence or speed.

**W1 · Opposite slots at the same weights.** Scale the parent's zero-endpoint warmup by `λ > 0`: LR `(1, 1, 2, 2)`, x-gradients `λ(−4, 4, −1, 1)` or their negatives, initial x and slots zero. Both end at `x = 0`, with `m_x = +λ` or `−λ`; y is untouched. Let old loss be `x²`. One preview gradient `(sλ/2, −1)`, `s ∈ {−1, 1}`, predicts the first unseen B2 gradient; subsequent gradients are `(0, −1)` in this frozen-slope fixture. With B2 LR 1, choosing `m_x = −sλ` zeros x and its slot throughout B2. At B2 step `t ≥ 1`, reset gives `x = −sλ(1 − 2⁻ᵗ)` and a wrong-sign choice gives twice that displacement. All arms have identical improving y-read (e.g. held-out `(y − 20)²` through step 10). The outgoing prefixes reach `|x| = 4λ`, so a tighter prefix budget can rule out both orders. If the *same* preview is compatible with both signs of the true shock, then `max_s |m_x/2 + sλ/2| ≥ λ/2`: no slot beats reset on worst-case first-step displacement. This is an information obstruction, not a search failure.

For a separation under one bound, scale only the predeclared outgoing LR by `1/16`. The seam slots and weights are unchanged, while the prefix maximum falls to `λ/4`. With that same bound in B2, the aimed orders pass and reset fails at the first unseen step. This deliberately uses a nonconstant LR schedule; it says nothing about the availability of useful ties at constant LR.

**W2 · Same examples and step count, different universal safety.** Start from zero with LR 1. Four examples have x-gradient parts `{1, 1, −1, −1}` and y-part `−1` each. For size-two like-sign batches, either order gives x-prefix magnitudes `1, 1/2`, violating the bound `|x| ≤ 1/2` at the first step. Both opposite-sign batches have x-part zero, so all orders keep `x = m_x = 0`, with the same `y = 5/2` as the original. In a zero-mean negative with x-parts `{3, −1, −1, −1}`, every size-two partition has a batch with mean `+1` that could arrive first. Accumulating all four would remove the obstruction but change the step contract.

**W3 · Equal anchor gradients do not certify curved safety.** Two strictly convex batch losses are `(x² + y²)/2 ± xy/2 − y`. Both have anchor gradient `(0, −1)`; either first step gives `(x, y) = (0, η)`. The other batch now gives x-gradient `±η/2`, so the two orders end at `x = ±η²/2`. Frozen-gradient balance without a remainder falsely accepts any x-bound smaller than `η²/2`.

### Two proof handles

For heavy-ball, aim for `P_A(βm_K + g_preview) = 0` on the first unseen step, and constrain `(I − P_A)(m_K − m_ref)` to avoid affecting B2-only motion relative to the reference. This equality is for a predicted impulse, not a guarantee about the true suffix: projected momentum zero on consecutive steps implies projected gradient zero on the second step. A single slot cannot exactly cancel an arbitrary sequence. Multi-step claims need a margin tube or a change in dynamics.

For additive frozen gradients, let `q` be a linear protected read, `ḡ` the unchanged window mean, and `e_q = max_i |q(g_i − ḡ)|` over formed batch gradients. Relative to the trajectory driven by repeated `ḡ` from the *same* weights and slots, the heavy-ball recurrence bounds every prefix:

`|q(θ_t − θ̄_t)| ≤ e_q × Σ_{j=1}^t Σ_{k=j}^t η_k β^(k−j)`.

This holds for nonnegative LR and `0 ≤ β < 1`. Add the mean trajectory’s drift and a **sound** remainder before checking the old-task margin. Matching a harmful mean proves nothing. Curvature, adaptive preconditioning, and nonlinear joint reads need joint-state bounds; propagate the reachable seam states through any declared suffix.

## Idea cards

**P** = candidate primitive if the proposed object beats the strongest matched controls; **I** = improvement or falsification audit, not a standalone pilot candidate under the ledger. All tests below are proposed CPU-scale checks.

### A. One preview buys one order decision

#### 01. Preview-indexed seam actuator (P)
- **Mechanism:** Enumerate a menu of same-weight outgoing orders with different seam slots. Dispatch against the preview’s projected shock, subject to a B-only carryover bound.
- **Novelty vs nearest prior art:** The parent's seed becomes a preview-addressable set of legal state actions. Replay-last is blind to the preview; [GPM] acts during B2.
- **Cheapest first test:** W1, then a six-batch warmup with unseen shock directions including a null projection. Compare blind order, replay-last, GPM, direct write, reset, and wrong-preview arms.
- **Old-task retention check:** Audit A/C at outgoing prefixes and B2 step 10, at matched B2 gain. A null preview should spend no extra margin.

#### 02. A preview alias proves that no shield can work (P)
- **Mechanism:** Find two admissible suffixes consistent with one preview but requiring disjoint safe seam-slot sets. Return that pair as a reason to abstain independently of order search.
- **Novelty vs nearest prior art:** Indistinguishability bounds are old; this witness ties a measured preview to infeasibility at a specific serving endpoint.
- **Cheapest first test:** W1’s same-preview sign flip, then a two-dimensional cone. Compare exhaustive legal orders, randomization, and a full-lookahead oracle.
- **Old-task retention check:** Score A/C on both aliases including the fallback, not just on suffixes that resemble the preview.

#### 03. Spend the preview on resolving a slot choice (P)
- **Mechanism:** Select one preview batch using only permitted ex ante metadata. Optimize the choice of stratum for distinguishing reachable shield actions rather than for estimating the mean B2 gradient.
- **Novelty vs nearest prior art:** Active sampling seeks informative observations; this would sample against the decision boundary of a discrete, fixed-weight actuator.
- **Cheapest first test:** Two source strata, one noisy in sign and one biased in magnitude but informative in sign. Compare uniform, representative, and no-preview dispatch with the same waiting rules.
- **Old-task retention check:** Report A/C worst-tail results on blind source mixtures and wrong metadata, and B2 gain on both sources.

#### 04. Invert a signed finite-horizon response tube (P)
- **Mechanism:** Map each reachable seam slot to a short B2 margin trajectory. Use the single preview plus a development-fitted suffix uncertainty set; deploy only when the whole response fits the budget. A distributional prediction set warrants only its stated coverage, not universal safety.
- **Novelty vs nearest prior art:** [AdamW response] already supplies signed response operators; the candidate is a constrained inverse over legal outgoing orders with an abstention region.
- **Cheapest first test:** Enumerate impulse, persistent, and alternating shocks in a smooth quadratic. Contrast first-step aiming, robust direct writes, and exact suffix enumeration.
- **Old-task retention check:** Check worst A/C prefix through step 10, including an initially good cancellation that fails later.

#### 05. Endpoint-neutral swaps as a basis for data-only actuation (P)
- **Mechanism:** Seek disjoint block switches whose weight effects cancel at the *global* seam while their slot responses add. With a common frozen suffix after block end j, neutrality at K requires `Δθ_j = Δm_j × Σ_{r=j+1}^K η_r β^(r−j)`; local weight ties alone fail. Verify reachable signed sums, not their unconstrained span.
- **Novelty vs nearest prior art:** [Slot splices](slot-splices.md) directly insert state; this proposed alphabet of actions comes from unchanged examples and has a seam-weight proof.
- **Cheapest first test:** Enumerate two-block switches and compare exact unrestricted search. Use naive concatenation of W1 blocks as a negative, then search for tail-compensated variants; check residual-weight-only controls under coupling.
- **Old-task retention check:** Check A/C at internal block boundaries and after the worst admitted switch combination, not just the endpoint.

#### 06. Isolate the preview × slot interaction (I)
- **Mechanism:** Cross true/shuffled preview, shield/reference weights, and shield/reference slots, with a direct write from the same preview as an actuation oracle.
- **Novelty vs nearest prior art:** Factorial ablation and [AdamW response] paired trajectories cover identification. This audit kills weight-residual and generic replay explanations.
- **Cheapest first test:** One smooth stream with exact endpoint ties where possible and a predeclared tolerance sweep otherwise. Require a true-preview benefit on the slot-only arm.
- **Old-task retention check:** Match seam A per-item margins and B2 gain; compare A/C at step 10 and after slot decay.

#### 07. Spend an impulse on avoiding a gate crossing (P)
- **Mechanism:** Use the preview-indexed slot to keep the trajectory on the safe side of an old activation boundary until the shock passes, with no B2-time intervention.
- **Novelty vs nearest prior art:** Parent card 04 already has gate steering. The bet is a preview-selectable branch with opposite shields for distinct shifts, not another demonstration of training hysteresis.
- **Cheapest first test:** Two-gate ReLU toy with mirrored shifts. Compare blind gate steering, projection, an exact slot swap, and a smooth/no-gate twin.
- **Old-task retention check:** Audit A/C at steps 10/50 and at recurrence with slots reset *after* the gate event to distinguish branch persistence from lingering carryover.

#### 08. Cancel threatened reads, not all old directions (P)
- **Mechanism:** Use one-sided slack per protected read. Aim only at threatened faces so B2-useful motion in old directions remains when it meets every other active margin.
- **Novelty vs nearest prior art:** [Per-sample interference] and [GPM] constrain the current update; here a predicted active face selects a past order. Face-aware projection plus replay is the strong control.
- **Cheapest first test:** Three-read quadratic with one useful shared direction, one threatened read, and one near-zero margin. Compare whole-subspace cancellation, face-aware projection, and exact order search.
- **Old-task retention check:** Match B2 gain and inspect each protected slice, especially where an apparently helpful direction flips one rare A/C read.

#### 09. A preview shield valid across hidden entering slots (P)
- **Mechanism:** If the scheduler cannot read the entering slot, compile a single preview-to-order map with a proof over the joint set of legal starts. Require the same public seam target and decline if it cannot be met.
- **Novelty vs nearest prior art:** [AdamW response] models perturbed states and parent card 20 handles jitter. This quantifies over hidden starting histories, not over order perturbations.
- **Cheapest first test:** Two histories with the same weights but different slots. Compare a robust map, state-specific schedules, direct read/reset, and a slot spread that breaks the declared seam tolerance.
- **Old-task retention check:** Check the full hidden-history × suffix grid on A/C without excluding the incompatible histories from coverage.

#### 10. Second-moment decoy for preview aiming (I)
- **Mechanism:** Seek weight-tied AdamW orders with similar first moments but different second moments. Separate signed cancellation from slowing every update, or report that the necessary pairs are unreachable.
- **Novelty vs nearest prior art:** Parent card 03, [AdamW response], and [STABLE] already cover slot-dependent damping; this is a directional-mechanism falsifier.
- **Cheapest first test:** Exhaust short warmup orders at fixed bias clock. Cross m-only, v-only, and both-slot interventions; compare with an effective-step-size-matched slowdown.
- **Old-task retention check:** A/C benefits must track the threatened read and preview sign at matched B2 gain, not just a blanket slowdown.

### B. Change the partition, then let any batch arrive first

#### 11. A universal-retention compiler for fixed-size batches (P)
- **Mechanism:** Synthesize a partition minimizing the worst protected-read excursion over all resulting batch orders; emit the batches and proof or decline. Optimize membership and adversarial order as separate variables.
- **Novelty vs nearest prior art:** Slicing [GraB] can also change membership. The proposed separation is a verified property of an *unordered* multiset, not a bound on the prefixes of GraB’s chosen ordering.
- **Cheapest first test:** W2, then blind 12-example windows of size-two batches. Enumerate every partition and arrival order; compare GraB-and-slice, random/stratified grouping, original-batch certification, pinning, and accumulation.
- **Old-task retention check:** Report minimum A/C margins over all orders and served prefixes, along with B gain and the fraction of blind windows certified.

#### 12. Proof that no legal rebatch will work (P)
- **Mechanism:** Use common mean drift, an indivisible outlier, or an equal-size vector partition lower bound to witness a violation under every partition. Distinguish infeasibility from a solver timeout.
- **Novelty vs nearest prior art:** Partition infeasibility and assignment duals are known; the proposed object ties an obstruction to the first violated optimizer prefix and old-task margin.
- **Cheapest first test:** W2’s zero-mean outlier and mean-matched feasible twins. Compare a short lower-bound witness with exact integer search under fixed size.
- **Old-task retention check:** Exhibit an A/C-violating prefix for each size-valid assignment in the negative fixture; verify the fallback on the same examples.

#### 13. Compile a common protected-state transition (P)
- **Mechanism:** For affine batch gradients `g_i(θ) = H_i θ + b_i`, seek `Q H_i = H_* Q` and `Q b_i = b_*` for a fixed old-read map `Q` and common `H_*, b_*`. Projected heavy-ball weights and slots then follow a common trajectory regardless of B-only dynamics. Certify that trajectory against the margin.
- **Novelty vs nearest prior art:** The closure condition is standard state aggregation. The opportunity is to *synthesize* closure through truthful batch membership, not to project away updates at run time as in [GPM].
- **Cheapest first test:** Enumerate size-two partitions of coupled quadratics, including W3. Compare pointwise gradient balancing and projection; perturb a hidden B direction to test closure.
- **Old-task retention check:** Check all A/C reads in the certificate and audit unseen old probes outside `Q` separately.

#### 14. Balance gradients and cross-curvature together (P)
- **Mechanism:** Approximate card 13 by balancing both protected gradients and derivatives along reachable B directions, with a bound on what the sketch omits over a certified local tube.
- **Novelty vs nearest prior art:** [Shuffle-order analysis] identifies curvature/order terms; [GPM] measures old subspaces. Here the partition aligns the dynamics, not just the gradients at the anchor.
- **Cheapest first test:** W3 plus eight examples admitting two different Hessian pairings at identical pointwise balance. Compare a directional proof with the same partition tested by a generic smoothness bound.
- **Old-task retention check:** Check both cross-curvature signs, including rare probes outside the sketch, and raise LR until the proof must abstain.

#### 15. Rebatch for Adam’s joint numerator and denominator (P)
- **Mechanism:** Group examples to shape pairs `(g_i, g_i ⊙ g_i)` and bound joint weight/slot trajectories under the bias clock. Square the batch **mean gradient**; averaging squared example gradients is not the same statistic.
- **Novelty vs nearest prior art:** Parent card 09 certifies fixed batches; [AdamW response] tracks both slots. Here grouping is a control variable for whether joint certification is possible.
- **Cheapest first test:** Exhaust two-coordinate partitions from cold and warmed starts; compare joint proofs with gradient-only balancing and independent slot bounds.
- **Old-task retention check:** Check every certified order on A/C, including scale imbalance and near-zero second moments with finite optimizer epsilon; report abstentions.

#### 16. Rebatch intact units under nonadditive objectives (P)
- **Mechanism:** Keep required positive/negative or sequence relations intact and use actual batch gradients or bounded context interactions. Cached singleton gradients are a proposal heuristic, never the certificate.
- **Novelty vs nearest prior art:** Stratified grouping already keeps correlated examples together. The proposed object verifies a partition under batch-context-dependent transitions instead of assuming its objective is additive.
- **Cheapest first test:** Eight contrastive embeddings with two paired positives and a hard negative. Compare true-batch enumeration, singleton sketches, relation-preserving random batches, and accumulation with the same negative context if available.
- **Old-task retention check:** Check A/C on held-out relations for every certified order; separate changed objective/context from balancing when interpreting B2 gain.

#### 17. Delete-on-use batch proofs with a shared margin budget (P)
- **Mechanism:** The certificate carries the remaining authorized batch IDs, budget consumed by real prefixes, and a reachable state set. Each update consumes a batch ID and narrows the possible continuations without renewing margin.
- **Novelty vs nearest prior art:** [Order handoffs](https://github.com/manojbajaj95/cl/pull/205) already tracks residual proof and spent budget. The increment would be a compact membership-specific proof cheaper than residual replay for an all-orders rebatch.
- **Cheapest first test:** Six-batch prefix tree. Compare correlated remaining-set states, static worst bounds, and exact replay; include duplicate and missing batch negatives.
- **Old-task retention check:** Score A/C on every admitted continuation and across handoffs; retaining old tasks only after silently renewing slack is a failure.

#### 18. Availability-aware batches, without a hidden barrier (P)
- **Mechanism:** Synthesize a fixed-size partition under cross-shard waiting constraints; use deadlines only to limit which examples can be paired. The proof still covers unrestricted arrival of the formed atomic batches.
- **Novelty vs nearest prior art:** Parent card 16 narrows the allowed orders; this limits grouping cost instead. The candidate increment over ordinary deadline packing is provable asynchronous progress at equal retention.
- **Cheapest first test:** Two shards with early same-sign examples and late compensators. Compare local/global grouping, GraB, pinning, and accumulation at equal maximum wait; sweep shard skew.
- **Old-task retention check:** Check A/C at first service and after a worst jitter schedule. Do not count a timeout that ran an uncertified partial batch as certified.

#### 19. Preserve a useful B spectrum behind an old-state guarantee (P)
- **Mechanism:** First certify protected dynamics for every order, then select among safe partitions for helpful B-only variability or convergence. Freeze the selection rule before blind windows.
- **Novelty vs nearest prior art:** [GraB] targets convergence through a chosen order. The bet is independent control of certified old dynamics and useful new dynamics through membership alone.
- **Cheapest first test:** Two partitions with the same protected gradient and Hessian signatures but different B-block gradients. Compare random safe grouping, stratification, and tuned accumulation; rule out effective LR as the explanation.
- **Old-task retention check:** Require the same A/C budget for both partitions and report worst as well as mean B2 progress over orders.

#### 20. A proof-carrying swap that repairs the worst arrival (P)
- **Mechanism:** Use a violating order and read to propose a two-example swap between equal-size batches. Certify the new global worst case instead of checking only the old counterexample.
- **Novelty vs nearest prior art:** Counterexample-guided refinement and parent quarantine already exist. A zero-drop partition repair is interesting only if it retains proofs cheaply across unseen windows.
- **Cheapest first test:** Eight examples where a swap fixing one read breaks another. Compare witness-directed swaps, exact search, random swaps, and original membership plus a single fence.
- **Old-task retention check:** Audit A/C on the *new* worst order after every proposed repair; an old failure disappearing alone proves nothing.

### C. Joint tests and deployment gates

#### 21. Co-design the shield and the partition it will face (P)
- **Mechanism:** Choose the seam order with only the preview; later form the incoming partition from the examples then legally available. Learn the policy pair on development streams so that more joint starts admit an all-orders certificate, without revealing the actual examples at the earlier decision.
- **Novelty vs nearest prior art:** Parent card 20 shuffles within chosen shield blocks. Here the first action changes the feasible partition problem for the next window; it counts only if the interaction beats independently tuned shield and rebatcher stacked together.
- **Cheapest first test:** Feed two W1-style seam states with distinct slots into the same incoming partition problem. Compare co-design, budget-matched stacked controls, and an explicitly out-of-contract full-lookahead oracle.
- **Old-task retention check:** Score A/C on outgoing prefixes, the common seam and every B2 order, plus a common unassisted suffix to catch deferred harm.

#### 22. The serving and throughput crossover (I)
- **Mechanism:** Test which real constraint binds: fixed seam weights, independent batch arrival, or a need for multiple exposed updates before the window closes. Default to a standard method when none binds.
- **Novelty vs nearest prior art:** Extends the parent’s cost audit, not a primitive. Charge the preview, assembly, proof, enforcement and fallbacks; tune accumulation and pinning under the same timing contract.
- **Cheapest first test:** CPU event traces with bounded buffers and exogenous deliveries, paired with small exhaustible learning models. Include a no-intermediate-service negative and compare cost per certifiable update at matched B2 gain.
- **Old-task retention check:** A/C prequential error at the same service opportunities; report worst-order violations, coverage, and fallback retention separately.

## Ranked deeper questions

1. **Can membership alone buy sound, useful freedom on blind windows?** Start with 11–14 and 22. Freeze a realistic prefix budget, solve exact small instances, then include curvature and actual assembly costs. Require better coverage than original batches/GraB or lower cost than pinning at matched B progress. Stop if tuned equal-latency accumulation dominates or all accepted cases were already safe.
2. **Is there enough usable preview information on a safe endpoint fiber?** Start with 01, 02, 04 and 06. Separate information failure (full lookahead wins but one preview aliases sign), actuation failure (direct write wins but no legal order reaches it), and mechanism failure (even the right direct write fails at matched B2 gain). Kill the generic preview shield if the true-preview slot interaction vanishes by step 10 or is reproduced by weight-only controls.
3. **Can all-order proofs stay tight in nonlinear hosts without changing the training job?** Start with 13–16 and 19. Require soundness on exhaustible small instances plus non-vacuous coverage on blind windows. If batch interaction, old-read leakage, or optimizer coupling defeats the proofs, restrict claims to additive objectives or genuinely closed dynamics.
4. **Does co-design buy anything beyond its parts?** Start with 17, 18 and 21. Match B gain, overhead, and old budget against the best legal shield plus rebatcher plus their fallbacks across an unseen successor window. Discard the combined idea if it needs early access to the future partition or a budget reset at the seam.

**Research call:** Rebatching is the stronger first bet: ask if actual partition choices expand sound all-order coverage. Keep preview aiming conditional on an informative preview and a prefix-safe reachable slot; W1 shows why either gate can fail. The paper fixtures alone do not warrant a pilot.

[Adam reset]: https://arxiv.org/abs/2306.17833
[AdamW response]: https://arxiv.org/abs/2608.19762
[FOGO]: https://arxiv.org/abs/2606.10406
[FullCert]: https://arxiv.org/abs/2406.11522
[GPM]: https://arxiv.org/abs/2103.09762
[GraB]: https://arxiv.org/abs/2205.10733
[Overshoot]: https://arxiv.org/abs/2501.09556
[Per-sample interference]: https://arxiv.org/abs/2607.16261
[shuffle-order analysis]: https://arxiv.org/abs/2606.29554
[STABLE]: https://arxiv.org/abs/2611.10655
