# Batch-order interventions: can an order of batches the receiver already holds act as an optimizer-slot write?

**Status:** Ideas only; no experiments, probe code, or GPU work. Two small exact-arithmetic CPU checks were run by hand to set up the cards (below); no code is committed. **Parent:** [Slot splices](slot-splices.md) ([PR #185](https://github.com/manojbajaj95/cl/pull/185)). **Review seeds:** [Flood triage, row 292](https://github.com/manojbajaj95/cl/blob/13e1623/reviews/flood-triage.md#L292) scores #185 cards **15** (an order key recovered from a batch multiset: ship only a checked permutation of truthful batches the receiver already holds, so different orders of the same multiset act as distinct slot writes with identical endpoint weights) and **20** (an impossibility witness for a sample-only actuator: when no legal weight-returning batch word reaches the needed response region, return a separating or finite-exhaustion certificate instead of more search) at 3. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/13e1623/reviews/idea-ledger.md).

Ledger constraints that bind this node:

- **Bounded-delay stability scheduling (killed):** reordering within a window changes end weights only at `O(η²)`, and gradient accumulation removes the order effect at the same latency. That kill assumed a memoryless update. [Optimizer Memory Makes Shuffle Order a First-Order Source of Fine-Tuning Noise][shuffle] (2606.29554) shows fixed-clock optimizers (AdamW, Lion, even a bare fixed-β momentum buffer) make equal-multiset order contrasts `O(η)`, while a clock-matched memory (state advancing in `τ = ηk`) restores `O(η²)`. So the channel exists, but gradient accumulation and a **clock-matched optimizer** are required negative controls for every card.
- **Decode training order from weights (killed as a study):** no card may be "recover the order". The object here is an order *chosen and checked as an intervention*.
- **Margin confound, ties-a-simple-baseline, true-by-construction:** a planted gate flip or the paper pair below is bookkeeping, not evidence. Match per-item margins and B utility; beat replay scheduling, partial optimizer reset and direct slot writes run together.

## What is new here, and what is not

Order as a training-time control is old. [Batch-order poisoning and backdoors][brrr] (BRRR, 2104.09667) steer SGD with clean data reordered by an attacker. [GraB][grab] (2205.10733) picks permutations by herding for faster convergence. [Process-tensor tomography][ptensor] (2601.16563) treats batch choices as instruments and certifies memory. [2606.29554][shuffle] sizes the order channel as noise. [Delayed optimizer-state transport][transport] (2608.24593) and [slot mediation][stored] (2608.20442) make optimizer state a causal carrier. [MTT][mtt] and [gradient matching][gm] choose sequences; [iterative machine teaching][imt] (1705.10470) picks examples for a learner's update rule.

None of these ships an order as a **checked, endpoint-neutral slot intervention**: a permutation of a multiset the receiver already holds, accepted only with (i) a multiset-equality check, (ii) an endpoint-weight tolerance relative to the receiver's default order, (iii) prefix A/C safety, and (iv) a declared later-response target. The dual object is a **certificate that no legal order reaches the target**, separating what a permitted slot write can do from what truthful data order can. Both count only if, on blind edits, they admit more useful work or cost less than the stacked controls: direct slot write ([#185](slot-splices.md) card 01), partial optimizer reset ([2306.17833][reset]), replay scheduling, MTT constrained to the same multiset, and exhaustive enumeration with caching.

## Two hand checks that shape the node

These are small exhaustive enumerations on frozen gradients (every example kept in a linear region, e.g. an active hinge), not experiments.

**1. Heavy-ball momentum locks weights to momentum.** For `m_k = β m_{k-1} + g_k`, `θ_k = θ_{k-1} − η m_k`, constant `η`, frozen gradients and any `m_0`:

```
m_K = β^K m_0 + Σ_j β^(K−j) g_j,     Σ_k m_k = (Σ_k β^k) m_0 + (S − β Σ_j β^(K−j) g_j) / (1 − β),     S = Σ_j g_j
⇒  θ_K = θ_0 − η/(1−β) · (S − β m_K) + c(m_0, β, K, η)      (c is order-invariant)
```
So two orders of the same multiset end at the same weights **iff** they end with the same momentum. The EMA form `(1−β)`-scales the same identity and the Nesterov form adds `η·S`; both lock. Verified exactly on 200 random integer windows of length 5. **Consequence:** under constant-LR heavy-ball with frozen gradients, a weight-silent order key does not exist at first order; any key must come from a nonconstant schedule, from θ-dependent gradients (the `O(η²)` bracket), or from a normalizer. Heavy-ball at constant LR is therefore a free, class-wide impossibility certificate and the natural negative host.

**2. Constant-LR Adam showed no exact weight ties either.** Enumerating every distinct order of `±1` multisets in exact rationals (length 10 for `β₁ ∈ {1/2, 9/10}`, length 6 for `β₁ = 1/3`; with `|g| = 1` the corrected `v̂ ≡ 1`, so Adam is `θ −= η m̂_k`), and of mixed-magnitude multisets such as `{3,−1,−1,−1,0,0}` and `{1,1,−1,−1,0,0}` up to length 6 in floating point (tolerance `10⁻¹²`, `ε = 10⁻⁸`, `(β₁,β₂) ∈ {(0.5,0.9),(0.9,0.999)}`), found **zero** pairs with equal endpoint weight and different `(m, v)`: every distinct order gave a distinct weight. The [#185 paper witness](slot-splices.md) gets its exact return only through the predeclared schedule `η, 3η`. This is evidence, not a proof, that for generic `β` the per-coordinate endpoint map is injective on multiset orders at constant LR; card 04 asks for the proof or a counterexample.

Together these change the seed's wording. "Identical endpoint weights" is a binding, non-generic constraint: under constant-LR coordinatewise optimizers, orders move weights at `O(η)` ([2606.29554][shuffle]) and appear not to tie exactly. Keys are therefore of three kinds, each with its own controls: **schedule-carried** (exact under a schedule frozen before search), **curvature-carried** (`O(η²)`, gradients depend on the path), and **tolerance keys** (endpoint within `ε`, with a residual-weight-only arm that must not explain the effect).

### What is held fixed

- Fix the batch multiset, update law, hyperparameters, LR schedule, precedence constraints (arrival times), and the receiver's default order **before** key search. The no-key reference is the receiver's own default order, with the same clock and work. Check endpoint weights by realized update vectors on a common probe, not logits.
- Declare the target as a later response: the immediate update on a frozen next pulse, or a gate outcome after a declared suffix. Endpoint equality makes immediate A/C identical by construction, so retention is scored at every **prefix** of the window, after the later pulse or shift, and after unassisted B continuation.
- Charge key search, failed candidates, multiset hashing, receiver checks and certificate checks. Report keys and certificates on blind, independently generated windows, separately from planted worlds.
- Old suites: A (with a rare slice) and C (unaffected control), current task B, frozen useful edit. Match B progress and initial margins throughout.

## Idea cards

**P** = candidate primitive if it works on blind windows beyond the stacked controls; **I** = improvement, diagnostic or audit. Labels are proposal judgments, not review scores. All first tests are proposed tiny CPU studies or hand enumeration.

### A. The two seeds, made to fail first

#### 01. A checked order key over a held multiset (P)
- **Mechanism:** The sender ships only a permutation index of `n` batches the receiver already holds (at most `log₂ n!` bits, no values). The receiver accepts it only if the multiset hash matches, its own first-order replay predicts endpoint weights within `ε` of the default order, and every prefix keeps A/C above floor; otherwise it trains in default order.
- **Novelty vs nearest prior art:** [BRRR][brrr] uses reordering as an unchecked attack on weights; [GraB][grab] orders for convergence; [2606.29554][shuffle] measures the same channel as noise. The new object is an endpoint-neutral, receiver-checked order write aimed at a later response.
- **Cheapest first test:** Two-coordinate Adam with a predeclared warmup schedule and 6 held batches (720 orders, exhaustible). Choose the key on 5 training histories, ship it to 5 unseen histories, and score the next-pulse update. Controls: uniform, greedy and GraB orders; MTT constrained to the same multiset and compute; direct slot write as ceiling; clock-matched Adam and constant-LR heavy-ball as negatives (both should give no key).
- **Old-task retention check:** A/C at every prefix (an order that dips A mid-window and returns is rejected even with equal endpoints), then after the later pulse and 20 B steps at matched B gain.

#### 02. An assignment-dual impossibility certificate (P)
- **Mechanism:** Linearize the window at frozen gradients: endpoint weights and slots are linear in the permutation matrix `P` (impulse weights by position). Relax `P` to the Birkhoff polytope; require the weight equality (or `ε`-band) and the target halfspace. If this LP is infeasible, its Farkas dual (assignment potentials `u, v` plus a separating hyperplane) proves every one of the `n!` orders misses, checkable in `O(n²)`. Add an explicit second-order remainder bound (Hessian-Lipschitz times path length) so the certificate is rigorous, not just first-order.
- **Novelty vs nearest prior art:** [Reachability][reach] certifies inaccessible regions generically, and assignment LP duality is textbook. The candidate primitive is a cheap, reusable certificate that separates two training interfaces (a legal slot write succeeds; no truthful order does) on the same retention and deadline.
- **Cheapest first test:** Windows of `n = 6..9` with exhaustive ground truth. Report the fraction of truly infeasible targets that the LP certifies (tightness), the false-certificate rate (must be zero with the remainder bound), and the check cost against cached exhaustion. Include a blind library where adding one legal batch makes the target feasible (card 22).
- **Old-task retention check:** When a certificate routes the receiver to a direct slot write instead, verify A/C after that write and after B; when it wrongly blocks (relaxation slack), count the lost useful edit.

#### 03. Use the momentum–weight lock as a class certificate (I)
- **Mechanism:** Hand check 1 as a reusable rule: for heavy-ball, EMA or Nesterov momentum at constant LR, "same weights" implies "same momentum" up to `O(η²)`. Any claimed order key on such a host must be curvature-carried, so its effect must scale as `η²`.
- **Novelty vs nearest prior art:** [2606.29554][shuffle] derives the impulse-weight kernel but uses it to size noise; the observation that the weight and slot kernels are linked for heavy-ball (so no endpoint-neutral key exists at first order) is the content here. It is a diagnostic, not a method.
- **Cheapest first test:** On a small nonlinear MLP with momentum SGD, search order pairs with endpoint weight distance below `ε` and measure the slot difference versus `η` on a log grid; the slope must be ≈ 2. A slope near 1 falsifies the lock outside the frozen-gradient regime.
- **Old-task retention check:** Record A/C at prefixes for the best curvature-carried pair; a key that only exists with large intermediate excursions is reported as unsafe.

#### 04. Prove or break constant-LR Adam injectivity (I)
- **Mechanism:** Hand check 2 suggests that, per coordinate, Adam's endpoint weight determines the order of a multiset at constant LR for generic `β`. Prove it (e.g. distinct position-weight vectors from bias correction give a lexicographic argument) or find the algebraic `β` where ties appear.
- **Novelty vs nearest prior art:** None claimed as a primitive. The result decides whether exact keys at constant LR are impossible (then only schedule, curvature and tolerance keys remain) for the whole node.
- **Cheapest first test:** Symbolic search over `β₁` as a variable for length-6 `±1` multisets: weight-tie conditions are polynomial in `β₁`; list real roots in `(0,1)` and check them exactly.
- **Old-task retention check:** At any tie value found, rerun card 01 and score A/C at prefixes; a tie that only exists at an unusable `β` is recorded as such.

### B. Where can a key live?

#### 05. Schedule-carried exact keys (P)
- **Mechanism:** A nonconstant schedule (warmup, cosine, step drop) gives position weights that break the lock, so exact weight ties with distinct slots exist (as in #185's `η, 3η` witness). The key is legal only if the schedule was fixed before the key was searched.
- **Novelty vs nearest prior art:** [2606.29554][shuffle] notes the clock dependence; [#141](https://github.com/manojbajaj95/cl/pull/141) writes slots with extra examples. The claim is exact, sample-free slot control from a schedule the receiver was running anyway.
- **Cheapest first test:** For constant, linear-warmup and cosine schedules over 8 sign-gradient batches, count weight-tied order classes and the spread of `m` within each class. If ordinary schedules give no ties, the key needs a contrived schedule and the card dies.
- **Old-task retention check:** Score A/C at prefixes and after a shift, comparing the best tied order against the default order in the same class.

#### 06. An exponent fingerprint for where a key lives (I)
- **Mechanism:** Measure how a key's later-response effect scales with `η` at fixed window: slope 1 means a fixed-clock slot channel, slope 2 a curvature bracket, slope 0 a planted threshold.
- **Novelty vs nearest prior art:** [2606.29554][shuffle] uses exponent splits for SGD vs AdamW vs matched-clock. Using the slope as an acceptance test for a claimed key (reject keys whose channel the host cannot carry) is the audit added here.
- **Cheapest first test:** Run the card 01 key over four `η` values and the clock-matched control; a slope-1 effect that survives the clock-matched control is a bug.
- **Old-task retention check:** At each `η`, A/C at prefixes; report the largest `η` at which the key is still prefix-safe.

#### 07. A per-coordinate marginal certificate (P)
- **Mechanism:** Adam is coordinatewise, so each coordinate sees only its own sequence of gradient values. If, in one target coordinate, no order of that coordinate's multiset gives the needed `(θ_c, m_c, v_c)` region, no global order can. In one coordinate, linear impulse objectives are extremized by sorted orders (rearrangement inequality), so the bound is `O(n log n)`.
- **Novelty vs nearest prior art:** Rearrangement bounds are classical; the use is a near-free first-pass refusal before the full card 02 LP.
- **Cheapest first test:** On card 02's windows, count how many infeasible targets the marginal test already refuses and its cost against the LP.
- **Old-task retention check:** As card 02: a refusal reroutes to the direct write or no write; score A/C for whatever is committed.

#### 08. The shared-permutation coupling gap (P)
- **Mechanism:** Different coordinates can each be satisfiable by a different order, while no single permutation satisfies all at once. Certify this coupling infeasibility with a multi-coordinate assignment LP and report the windows where marginal tests pass but the coupled test fails.
- **Novelty vs nearest prior art:** Multi-index assignment is known to be hard in general; the claim is that the gap is common in realistic windows, so the full certificate earns its cost beyond card 07.
- **Cheapest first test:** Two- and three-coordinate windows of 7 batches; measure the share of targets in the gap and whether LP relaxation closes it.
- **Old-task retention check:** For targets just inside the coupled feasible set, check that the achieving order does not buy the target coordinate by breaking an A coordinate at a prefix.

#### 09. Order-key capacity modulo duplicate batches (I)
- **Mechanism:** Batches with equal gradients on the declared support are interchangeable, so the real key space is the number of distinct slot outcomes, not `n!`. Report the capacity spectrum (distinct reachable slot states at matched weights) per window.
- **Novelty vs nearest prior art:** Pure counting; it bounds how many targets any order key can hit and sets the size a slot packet must beat.
- **Cheapest first test:** Exhaust windows with 0, 2 and 4 duplicated batches; plot distinct weight-tied slot states.
- **Old-task retention check:** Not a training intervention; check that the capacity counted is over prefix-safe orders only.

#### 10. Curvature-carried keys for memoryless hosts (P)
- **Mechanism:** For plain SGD, endpoint order effects live in the gradient bracket `[∇g_i, g_j]` at `O(η²)` ([implicit regularization in SGD][smith]). Search pairs of orders that agree on weights to first and second order but differ in a later-response quantity that depends on the path through curvature (e.g. which batch was seen at the sharpest point).
- **Novelty vs nearest prior art:** The ledger kill says these effects are `O(η²)` and removed by accumulation; the card tests whether a deliberately chosen bracket can still move a later gate. Likely to die; it is the honest negative for slot-free hosts.
- **Cheapest first test:** One-hidden-unit ReLU network with plain SGD; exhaust 6 batches and test a later gate at three `η`. Gradient accumulation of the window is the control that should tie.
- **Old-task retention check:** A/C at prefixes and after the later pulse.

### C. Making the check cheaper than the replay

#### 11. A receiver check below one replay (P)
- **Mechanism:** The receiver verifies endpoint neutrality from cached per-batch gradient sketches and position weights, plus a remainder bound, instead of running both orders. Only accepted keys are trained.
- **Novelty vs nearest prior art:** [Proof of learning][pol] (2103.05633) logs and replays training; [neural proof sharing][proof] (2608.19351) reuses proofs. The claim is a sub-replay acceptance check specific to order writes.
- **Cheapest first test:** Compare sketch-check accept/reject decisions against true replay on 200 blind windows; count false accepts (must be zero inside the bound) and check cost.
- **Old-task retention check:** For falsely rejected keys, nothing is lost; for every accepted key, run the true A/C prefix audit afterwards.

#### 12. Precedence-legal keys (P)
- **Mechanism:** In a stream, a batch cannot be trained before it arrives, and some batches must precede others (dependencies). Legal keys are linear extensions of a poset; relax to the linear-ordering polytope and certify over that instead of all `n!`.
- **Novelty vs nearest prior art:** Scheduling under precedence is classical. [Two-clock examples (PR #187)](https://github.com/manojbajaj95/cl/pull/187) card 12 reorders swappable B updates for proof options; this card gives the reachability certificate for that legal set.
- **Cheapest first test:** Windows with 0, 3 and 6 precedence edges; measure how fast certified-infeasible targets grow as edges are added.
- **Old-task retention check:** As card 01 under each legal set.

#### 13. Prefix-safe key search by subset DP (P)
- **Mechanism:** Treat A/C floors at every prefix as part of legality. Dynamic programming over subsets (`2ⁿ` states with linearized slots) finds a prefix-safe key or certifies none exists, exactly for `n ≤ 20`.
- **Novelty vs nearest prior art:** Held–Karp style DP is classical; the use is an exact prefix-safety certificate for order writes, which endpoint-only searches (MTT, GraB) do not give.
- **Cheapest first test:** On card 02's windows, compare DP refusals with endpoint-only LP refusals; count targets where the LP says feasible but every achieving order breaks A at some prefix.
- **Old-task retention check:** This card *is* the prefix retention check; after the key, also score A/C after the later pulse and B continuation.

#### 14. Audit against gradient accumulation at equal latency (I)
- **Mechanism:** The ledger kill's control, applied to every surviving key: accumulating the window into one step removes order entirely. If accumulation plus a direct reset or replay reaches the same later response and retention at the same latency, the key is moot.
- **Novelty vs nearest prior art:** None; this is the mandatory audit.
- **Cheapest first test:** For each key from cards 01/05, run accumulated, default-order and keyed windows with matched B gain.
- **Old-task retention check:** A/C after the window and after the later shift for all three arms.

### D. Using order keys for continual learning

#### 15. A momentum shield before a known shift (P)
- **Mechanism:** When the receiver knows a shift (new task B2) arrives after the window, choose a key that ends the window with momentum pointing along an old-task-protective direction (e.g. old-replay batches late), at matched weights, so the first B2 steps are deflected away from A-sensitive directions.
- **Novelty vs nearest prior art:** [Delayed transport][transport] chooses loss weights; replay scheduling and curricula choose what to replay and when. The new claim is protection carried only by order at equal endpoint weights. Controls: replay-last scheduling with free endpoints, partial optimizer reset at shift ([2306.17833][reset]), [GPM][gpm] projection.
- **Cheapest first test:** Two-task linear-ReLU world with Adam and warmup; exhaust 8 window orders; score A after 10 B2 steps against the controls at matched B2 gain.
- **Old-task retention check:** A (rare slice) and C after B2; also at window prefixes.

#### 16. Second-moment keys that damp old-task coordinates (P)
- **Mechanism:** Order changes Adam's `v` at matched weights. Place large-gradient old-task batches so `v` is large in A-sensitive coordinates when new data arrives, damping their effective LR, a data-only analogue of importance-weighted damping.
- **Novelty vs nearest prior art:** [Matched Specialization][matched] shows second-moment swaps matter; EWC-style and Adam-state methods ([STABLE][stable]) set damping directly. Novelty requires beating a direct `v` write and Fisher-weighted damping at equal retention, using only order.
- **Cheapest first test:** Same world as card 15 with mixed gradient magnitudes; compare keyed `v` against direct `v` write and no-key at matched B2 gain.
- **Old-task retention check:** A/C after B2 and after 50 further B steps (damping must not freeze useful B learning).

#### 17. Compile a slot splice into an order with zero new examples (P)
- **Mechanism:** Take a validated two-sided splice from [#185](slot-splices.md) card 01 and ask for an order of held batches that realizes its response contract at matched weights. Return the order, or the card 02 certificate that none exists.
- **Novelty vs nearest prior art:** #185 card 14 compiles a splice into a batch word with new truthful examples; this uses none, so the splice travels without the donor checkpoint and without data transfer. Control: #185 card 14 with the same compute, and the direct splice.
- **Cheapest first test:** Use #185's four-block world; give the receiver 8 held batches; count splices that compile, and transfer to a blind second editor.
- **Old-task retention check:** A/C at prefixes and after the second editor's edit plus B continuation.

#### 18. Keys that survive the receiver's own noise (P)
- **Mechanism:** Dropout, augmentation and nondeterministic kernels perturb gradients. Choose keys that hit the target with probability `≥ 1−δ` over that noise and certify it by a concentration bound on the linearized slot map.
- **Novelty vs nearest prior art:** Chance-constrained planning is known; [2606.29554][shuffle] measures the channel under fixed seeds. The claim is a portable key whose acceptance holds under declared noise.
- **Cheapest first test:** Add Gaussian gradient noise at three levels to card 01's world; measure key success on unseen noise seeds versus the bound.
- **Old-task retention check:** Worst-case A/C over noise seeds at prefixes.

#### 19. Order-safety certificates against ordering attacks (P)
- **Mechanism:** Run card 02 defensively: certify that **no** permutation of the incoming window can move the slots into a region that harms A beyond `δ` after the declared suffix. Windows that pass can be left to an untrusted data pipeline; windows that fail get a fixed (hash-sorted) order.
- **Novelty vs nearest prior art:** [BRRR][brrr] shows the attack; [proof of learning][pol] audits after the fact. A per-window certificate of order robustness, cheaper than fixing the order everywhere, is the candidate.
- **Cheapest first test:** On card 02's windows, run a BRRR-style adversarial order search; certified windows must show no damage, and report the fraction of windows certifiable.
- **Old-task retention check:** A/C under the worst adversarial order for certified windows, versus the hash-sorted fallback.

#### 20. Transfer of a key across receiver histories (P)
- **Mechanism:** For heavy-ball, incoming momentum `m_0` adds an order-invariant term, so a key's slot effect transfers exactly at first order. For Adam, bias-correction clock and `v`-normalization break this. Ship a key with a predicted transfer domain (clock range, `v` range) and refuse outside it.
- **Novelty vs nearest prior art:** #185 card 07 builds clock-independent slot payloads; here the payload is an order, and the domain is derived from the impulse kernel.
- **Cheapest first test:** Choose a key at clock 10, test at clocks 10, 100 and 1000 with varied `v`; compare predicted against realized response.
- **Old-task retention check:** A/C at prefixes and after the later pulse at each clock.

#### 21. Composing keys across windows (I)
- **Mechanism:** Momentum carry decays as `β^K`, so keys in separated windows compose almost additively; keys in adjacent windows interact. Declare a composition rule and check it.
- **Novelty vs nearest prior art:** Inherits #185 card 08 (splice composition); improvement only.
- **Cheapest first test:** Two consecutive 6-batch windows with independently chosen keys; compare composed response with the prediction.
- **Old-task retention check:** A/C after each window and after both.

#### 22. Minimal-augmentation witness when the certificate refuses (P)
- **Mechanism:** When card 02 certifies infeasibility, its dual hyperplane ranks which extra legal batch from a larger pool would break the separation. Return the certificate plus the smallest legal addition that makes the target reachable, so the receiver knows the exact price of switching interfaces.
- **Novelty vs nearest prior art:** Teaching-dimension and [machine teaching][imt] count examples to teach a target; the candidate is a certificate-guided price of the data interface versus a slot write.
- **Cheapest first test:** On infeasible targets from card 02, compare dual-ranked additions against exhaustive one-batch addition: hit rate and cost.
- **Old-task retention check:** A/C after the augmented keyed window, against the direct slot write at matched B gain.

## Ranked deeper questions

1. **Does an exact weight-silent order key exist under constant-LR fixed-clock optimizers, and if only schedule-, curvature- or tolerance-carried keys exist, are they bigger than the order-noise floor of [2606.29554][shuffle]?** Start with cards 04, 05 and 06. Heavy-ball is already locked (hand check 1); constant-LR Adam showed no ties up to length 10 (hand check 2). If keys need contrived schedules or survive only as `η²` effects that accumulation removes (card 14), drop seed #15 as an actuator and keep its certificate side.
2. **Is the Birkhoff/assignment certificate tight enough to decide most real windows, rigorously and far cheaper than exhaustion?** Cards 02, 07, 08 and 13. Tightness, zero false certificates with the remainder bound, and the coupling gap decide whether seed #20 is a primitive or a restatement of reachability.
3. **Does an order-only key change an old-task outcome after a later shift beyond partial reset, replay scheduling and accumulation at equal B utility?** Cards 15 and 16. This is the CL question; without a retention gain here, keys are a curiosity.
4. **Can a certificate make a window safe against adversarial ordering at less cost than fixing the order?** Card 19. A positive answer is a defensive use of seed #20 that does not depend on keys being useful.

**Verdict:** Keep seed #20 (certificates) as the stronger candidate: the assignment-dual certificate is cheap, checkable and still useful if keys turn out tiny, both for routing to a slot write (card 02) and for defending against ordering attacks (card 19). Seed #15 (order keys) faces a structural obstacle found here: heavy-ball locks weights to momentum, and constant-LR Adam appears injective on orders, so exact endpoint-neutral keys need a schedule or curvature. If selected later, run cards 04 and 05 first as cheap falsifiers for #15, and card 02 on exhaustible windows for #20. No pilot is launched here.

[brrr]: https://arxiv.org/abs/2104.09667
[gm]: https://arxiv.org/abs/2006.05929
[gpm]: https://arxiv.org/abs/2103.09762
[grab]: https://arxiv.org/abs/2205.10733
[imt]: https://arxiv.org/abs/1705.10470
[matched]: https://arxiv.org/abs/2610.15830
[mtt]: https://arxiv.org/abs/2203.11932
[pol]: https://arxiv.org/abs/2103.05633
[proof]: https://arxiv.org/abs/2608.19351
[ptensor]: https://arxiv.org/abs/2601.16563
[reach]: https://arxiv.org/abs/1709.07523
[reset]: https://arxiv.org/abs/2306.17833
[shuffle]: https://arxiv.org/abs/2606.29554
[smith]: https://arxiv.org/abs/2101.12176
[stable]: https://arxiv.org/abs/2611.10655
[stored]: https://arxiv.org/abs/2608.20442
[transport]: https://arxiv.org/abs/2608.24593
