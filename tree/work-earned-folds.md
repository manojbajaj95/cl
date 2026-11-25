# Work-earned fold-backs: let useful work erase the hidden difference before the narrow learner takes over

**Status:** Ideas only; no pilots, training runs, or GPU work. The three witnesses below are exact rational paper fixtures, not experiments. **Parent:** [Update-preserving fold-backs](update-folds.md) ([PR #239](https://github.com/manojbajaj95/cl/pull/239)). **Review seed:** [Flood triage row 357](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L357), score-3 merge MRS11 from [cross-pool round 54](https://github.com/manojbajaj95/cl/blob/devin/1795537860-merged-ideas/ideas/flood/cross-pool-54.md#L25): return a temporary split only after required truthful C batches shrink the optimizer echo, including drift caused by different gradients, before the first sensitive step, and carry only the smallest sufficient slot. **Siblings:** [echo-absorbing work](https://github.com/manojbajaj95/cl/blob/devin/1795565045-echo-absorbing-work/tree/echo-absorbing-work.md) (C work that shrinks an echo) and [slot echo](https://github.com/manojbajaj95/cl/blob/devin/1795564677-slot-echo/tree/slot-echo.md).

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). The coded-interference kill means a fitted proxy is never proof that a fold is equal. The Noether-memory kill means a gradient-flow invariant is not a finite-step SGD, momentum or Adam invariant. The retention-matched reserve rerun means a ranking (here: which C order or which fold time) has to show a useful spread before anyone credits it. A merge card has to beat the stack of its parts, not one part. **P** marks a candidate reusable operation; **I** marks an improvement or a falsifier. A P is not a priority claim or a pilot recommendation.

## What would be new?

The parent node gives the refund test: a fold F returns width only if f(Tᵤ(s)) = f(Sᵤ(F(s))) for every u in a declared update class U. When that test fails, the parent's only choices are to refuse, transport more state, or stay wide. MRS11 adds a third choice: **keep training on work you had to do anyway**, and fold at the first boundary where that work has made the wide state lumpable again for the remaining U, and before any consumer can read the difference.

Nearest prior art:

- [Guarded optimizer-state compression](https://www.alphaxiv.org/abs/2611.00589) accepts decoded Adam moments only when the native update stays within tolerance for every gradient in a clipped domain. It tests a fixed state at one restore. It does not schedule training to *reach* an acceptable state, and it does not shrink width.
- [Exact Network Surgery](https://arxiv.org/abs/2607.16568) and [Net2Net](https://arxiv.org/abs/1511.05641) preserve the function and unaffected slots when *growing*. [Growing and elastic networks in online CL](https://www.alphaxiv.org/abs/2608.01475) grow and prune for plasticity, but the excerpts we read make no next-step optimizer equivalence claim at shrink time.
- [Delayed optimizer-state transport](https://www.alphaxiv.org/abs/2608.24593) moves state across a change; it does not use the training stream to make the state smaller.
- [Proximity-regularized continual LoRA merging](https://www.alphaxiv.org/abs/2609.32332), [singular-subspace merge and restore](https://www.alphaxiv.org/abs/2611.10881), [TIES](https://arxiv.org/abs/2306.01708) and [CAMFT](https://arxiv.org/abs/2609.22253) shape weights so a merge hurts less. They do not certify the next optimizer transition after the merge.
- The [echo-absorbing sibling](https://github.com/manojbajaj95/cl/blob/devin/1795565045-echo-absorbing-work/tree/echo-absorbing-work.md) asks whether C work can shrink an echo. This node asks what that buys: **released width, at a certified time, with the smallest carried slot.**

The candidate primitive is a **work-earned fold certificate**: a predeclared schedule of truthful C batches, a fold time τ, a narrow slot map, and a proof that for every u in U after τ the narrow learner takes the same output step as the wide one, plus a refusal rule when C work cannot get there before the first sensitive consumer. A scalar "echo norm went down" is not the certificate; witness W1 shows why.

## Fold-back contract

- Fix before the window: host, peak and terminal width, the split and fold maps, domain D, old-task floors (A), acquired new skills (B), the C task and its *required* batch budget, the sensitive consumer set (the first batch, reader or norm statistic whose output can see the echo), U after the fold, optimizer, precision and RNG. C batches must be real C examples with their real labels, in an order a non-oracle scheduler could pick: no synthetic anti-gradients, no no-op inserts, no access to the partner's private gradients beyond what the declared protocol sends.
- Echo is the full difference between the wide state and the image of the narrow state that the fold would produce: weight differences, first and second moments, drift that comes from the same batch producing *different* gradients in the twin copies, bias-correction counters, clipping statistics and any mutable buffer. Track every component. The fold is admitted only when the parent's equality holds for every u in U, at the declared precision, and before the first sensitive consumer.
- The carried slot is the coarsest partition of wide states that every u in U cannot tell apart (parent card 02), computed for the *post-C* state set, not the pre-C one. Report its bytes.
- Controls, each at the same width-steps, same C examples, same retention floors and same information: (1) permanent split; (2) blind fold at the split boundary with slot reset; (3) function-only fold at τ; (4) exact lawful state transport at the earliest time; (5) blind decay (keep training C in the ordinary order and fold at τ); (6) separate C absorption, then refold; (7) ordinary merge-aware training (proximity/TIES-style); (8) the stack of (4)+(5)+(7) with exact recertification. Count released width only when its weights, optimizer state and readers are freed and a real later writer uses it. A merge claim has to beat (8).
- Check A, B and C at the split, at τ, after the first sensitive step, and through two later U steps. A fold that matches a wide reference that is forgetting is not a success.

## Three paper witnesses (not pilots)

All three use exact `Fraction` arithmetic. The model is f(x) = a₁(x−t₁)² + a₂(x−t₂)² (two "copies" of one quadratic unit), the narrow model is a(x−t)², and the fold is F(a₁,a₂,t₁,t₂) = (a₁+a₂, t₁), valid only when t₁ = t₂. A batch is one point x with output residual e = f(x) − y (squared loss/2, real target y). Wide SGD: aᵢ ← aᵢ − ηe(x−tᵢ)², tᵢ ← tᵢ + 2ηeaᵢ(x−tᵢ). Narrow SGD uses the lawful learning-rate conversion for tied copies (2η on a, η/2 on t). η = 1/4.

**W1 — The echo is invisible to the function, and it is the drift from different gradients.** Start at s₀ = (5/4, 3/4, 0, 0), which is the function 2x² and folds to (2, 0). The weights differ in a hidden direction: amplitude imbalance a₁ − a₂ = 1/2 with tied knots. Because the two knot gradients are proportional to aᵢ, one consumer batch (x = 1/2, e = 1) moves the knots by different amounts. The blind fold then differs from the wide model by 175/2048 at x = −1. The balanced start (1, 1, 0, 0) has gap 0, which checks the conversion. Truthful work can erase the echo exactly: the C pair (x = −2, e = −2), then (x = 0, e = 1/2) sends echo (t₁−t₂, a₁−a₂) from (0, 1/2) to (1, 1/2) to (0, 0), and afterward the fold matches every consumer exactly. Three findings matter:
- **The echo is not monotone.** The first C batch makes the knot echo *larger* (0 → 1) before the second removes both parts. A greedy rule that folds as soon as the echo shrinks would fold at the wrong time or never.
- **Order matters.** The same two batches in reverse order end at echo (1, 1/2). At x = t the first batch has zero gradient, so the echo is untouched. The second batch then splits the knots.
- **Retention is the binding cost.** On a grid (x in quarters in [−2, 2], e in eighths in [−2, 2]) exactly 8 C pairs drive the echo to (0, 0). The best one still moves the old outputs at x = ±1 by 10321/4096 ≈ 2.52, larger than their value 2. On a coarser grid (x in halves, e in quarters) no single C batch reduces max(|t₁−t₂|, |a₁−a₂|) below 1/2. In this toy, exact work-earned folding exists but costs the old task. The claim to test is a retention-constrained version, not a free one.

**W2 — The smallest sufficient slot depends on U, and some echo skips the first check.** Heavy-ball momentum m′ = βm + g, p′ = p − ηm′ with β = 1/2, η = 1/4, at the balanced state (1, 1, 0, 0). The narrow slots are the copy averages m_a = (m₁+m₂)/2 and m_t = (m₃+m₄)/2. Test on three batches (x, e) = (1/2, 1), (−1, −1/2), (2, 0); e = 0 isolates the slot.
- With U = read-out only (knots frozen), carrying m_a alone is exact even when the knot slots differ (m₃ = 1, m₄ = 0). The knot slot is unread under this U and can be deleted.
- With U = full and equal slots, carrying m_a and resetting m_t gives gaps 507/2048, 39/128, 231/1024. So the knot slot is required under this U.
- With U = full and knot slots differing (m₃ = 1, m₄ = 0), averaging still fails: gaps 13/2048, 1/128, 7/1024. The fold must refuse or wait.
- With U = full and read-out slots differing (m₁ = 3/2, m₂ = 1/2), the first-step gap is **0** on all three batches, but the step creates amplitude echo a₁ − a₂ = −1/8. On a second batch (x, e) = (−1, 1) the output gap is 2378895/134217728 ≈ 0.018, and the echo is knot drift 19/256 and amplitude −3/16. A first-sensitive-step check passes on a state that is not closed under U.

**W3 — "Before the first sensitive step" has to be defined by readers, not by time.** Combining W1 and W2: the read-out-slot echo in W2 is harmless to every reader that sees one step, and visible to a reader that sees two. The sensitive consumer is therefore the first *pair* of U steps. A certificate that names the first batch as the consumer gives a false pass. The fold boundary has to be computed from the closure condition F(Tᵤ(s)) = Sᵤ(F(s)) on the reachable set, which the parent already requires for reusable receipts.

## Idea cards

### When has ordinary work earned the fold?

#### 01. Fold only on a lumpability certificate computed after the C work (P)
- **Mechanism:** After each required C batch, test whether the reachable wide states are lumpable to the narrow image under every u in U. Fold at the first time the test passes and before the first consumer. Refuse at the consumer deadline.
- **Novelty vs nearest prior art:** Guarded compression tests one fixed state at restore; this test is applied along a training trajectory and its pass time is the output, so the width is released early or not at all.
- **Cheapest first test:** W1 with a list of C streams; compare against blind fold, function-only fold at the same time, and permanent split.
- **Old-task retention check:** A at x = ±1 at the split, the fold, and two U steps later; B as the consumer task itself.

#### 02. Track the echo as a vector, never as a norm (I)
- **Mechanism:** Keep the full echo (weights, each moment, counters, clip statistics) and the linearized map from each C batch to it. Admit a fold only on component-wise zero (or a certified bound for every reader), never on a falling norm.
- **Novelty vs nearest prior art:** The echo-absorbing sibling defines the recurrences; W1 shows the norm can rise before it vanishes and that one component can be near zero while another is large.
- **Cheapest first test:** W1 with the greedy rule "fold when ‖echo‖ falls" versus the vector certificate; count false passes and false refusals.
- **Old-task retention check:** Score A at every false-pass fold to show the cost of the norm rule.

#### 03. Schedule C batches so the echo dies on a deadline (P)
- **Mechanism:** Treat the order of the required C batches as the only control. Search orders, not data, for one that drives the echo to the admitted set before the consumer. Because the batches are the ones you had to train on anyway, the scheduler gets the fold for free in data.
- **Novelty vs nearest prior art:** Curriculum and data-ordering work optimize loss; none uses ordering to make a temporary split lumpable. W1's reverse-order failure shows the order alone decides the fold.
- **Cheapest first test:** Enumerate all orders of 2–4 fixed truthful C points in W1 and report the fraction that earns the fold, against the best order with blind decay.
- **Old-task retention check:** For each earning order, A drift at x = ±1; keep only orders under the floor.

#### 04. Retention-constrained echo annihilation (P)
- **Mechanism:** Solve for the C order and step sizes that zero the echo subject to an old-task floor, as one constrained problem. If the feasible set is empty, report a certified refusal with its dual (which A probe blocks the fold).
- **Novelty vs nearest prior art:** W1 shows unconstrained annihilation costs more than the old output's value. Proximity-regularized merging limits drift at merge; this limits drift during the work that makes the merge exact.
- **Cheapest first test:** W1 grid with a floor |Δf(±1)| ≤ 1/4; report feasible count and the cheapest refusal certificate.
- **Old-task retention check:** The floor is the check; also report A after two later U steps.

#### 05. Reach the closure set, not a zero-gap state (I)
- **Mechanism:** Replace "first-step gap is zero" by "the state is in the largest set closed under all u in U whose fold is exact". Compute that set by fixed-point iteration on the finite toy.
- **Novelty vs nearest prior art:** The parent requires closure for reusable receipts; W2's read-out-slot case shows a first-step test passes outside the closure set.
- **Cheapest first test:** W2 four cases; report which pass a one-step check and which are in the closure set.
- **Old-task retention check:** A probe after the second U step, where the hidden amplitude echo first shows.

#### 06. Find the first sensitive consumer from the reader graph (P)
- **Mechanism:** For each echo component, compute the earliest U step at which some output or norm reader depends on it. The fold deadline is the minimum over components. Components with no reader inside the horizon can be dropped, not absorbed.
- **Novelty vs nearest prior art:** MRS11 names "the first sensitive step"; W3 shows it must be per component and can be later than the first batch, which changes what work is required.
- **Cheapest first test:** W2 with full U: deadline 1 for knot slots, deadline 2 for read-out slots; check the predicted deadlines against exact gaps.
- **Old-task retention check:** A at each component's deadline.

#### 07. Count differing-gradient drift as forcing, not as noise (I)
- **Mechanism:** Write the echo recurrence with an explicit forcing term from the twins receiving different gradients on the same batch (W1: knot gradients ∝ aᵢ). Certify that the forcing is zero on the admitted set, or bounded below each reader's tolerance.
- **Novelty vs nearest prior art:** Moment-decay arguments assume equal gradients after the split; W1's echo is created by the forcing alone, from a zero knot echo.
- **Cheapest first test:** W1 consumer step: split the gap into decay and forcing parts exactly; repeat with momentum.
- **Old-task retention check:** A drift caused by the forcing part alone.

#### 08. Use bias-corrected Adam counters as part of the echo (I)
- **Mechanism:** For Adam, include the step counter and bias correction in the echo; a narrow learner restarted at counter 0 differs even with equal moments. Carry the counter or prove it is unread for U.
- **Novelty vs nearest prior art:** Guarded compression pins the operation model; this makes the counter an explicit slot whose sufficiency depends on U.
- **Cheapest first test:** Rational Adam version of W2 with counters 1 versus 5 and equal moments; report gap.
- **Old-task retention check:** A after the first post-fold Adam step.

#### 09. Certify clipping and norm readers at the fold, not only flags (I)
- **Mechanism:** If a global-norm clip or normalizer reads the wide state, the echo includes the norm statistic. Admit a fold only if the narrow norm equals the wide norm for every u in U, not just the clip branch.
- **Novelty vs nearest prior art:** The echo-absorbing sibling warns that equal flags are not enough; here a norm reader can make an otherwise closed fold fail one step later.
- **Cheapest first test:** W2 with a global clip threshold between the wide and narrow norms of the duplicated copies.
- **Old-task retention check:** A on the batch where the clip branch first differs.

### What is the smallest thing to carry?

#### 10. Recompute the minimal slot after work, and expect it to shrink (P)
- **Mechanism:** The parent's partition (card 02) is computed on the pre-C state set. Recompute it on the post-C reachable set. The certificate pays for bytes only of the post-C slot.
- **Novelty vs nearest prior art:** Parent card 02 treats the state set as fixed; here the training stream changes it, and the saving is the difference between the two partitions.
- **Cheapest first test:** W2 with a C stream that equalizes the knot slots; compare slot bytes before and after.
- **Old-task retention check:** A after one step of each slot choice.

#### 11. Delete slots U never reads, instead of absorbing them (P)
- **Mechanism:** Before scheduling C work, restrict to echo components that some reader in U sees. Unread components (W2: knot slots when knots are frozen) are deleted at no work cost.
- **Novelty vs nearest prior art:** Exact Network Surgery keeps unaffected state; this deletes affected state that the declared U cannot reach, and it is the cheapest control for every work-earned card.
- **Cheapest first test:** W2 read-out-only U; count C batches saved versus absorbing all components.
- **Old-task retention check:** A after U changes to include the deleted reader (must be refused, not silently wrong).

#### 12. Trade C work against carried bytes on one curve (P)
- **Mechanism:** For each budget of C batches, compute the smallest sufficient slot. Report the frontier of (C batches, carried bytes, width released, A drift). Pick a point by a preset price.
- **Novelty vs nearest prior art:** Optimizer-state compression trades bytes for update error; this trades training work for bytes at zero update error.
- **Cheapest first test:** W1 and W2 over 0–4 C batches; plot the exact frontier.
- **Old-task retention check:** A drift as the fourth axis; reject points over the floor.

#### 13. Carry a one-number slot that only distinguishes the remaining readers (P)
- **Mechanism:** When the post-C echo is in a known one-dimensional direction, carry its coordinate as a single scalar slot that the narrow learner feeds back into its update, instead of the full wide slot.
- **Novelty vs nearest prior art:** Low-rank optimizer state (e.g. factored moments) compresses for memory; this keeps exactly the coordinate that U can read, with an equality proof.
- **Cheapest first test:** W2 read-out echo: carry m₁ − m₂ as one scalar plus m_a; verify zero gap over two steps.
- **Old-task retention check:** A after the step where the scalar would matter.

#### 14. Prove a lower bound on the slot that work cannot remove (I)
- **Mechanism:** Find wide states that no truthful C stream inside the budget can make lumpable. Their distinguishing u sets a floor on carried bytes; report it as a non-refund.
- **Novelty vs nearest prior art:** Parent question 2 asks for the first unavoidable memory cost without work; this asks for the cost that survives work.
- **Cheapest first test:** W1 grid: echo states reachable but not annihilable with 1 batch (on the coarse grid none gets below 1/2).
- **Old-task retention check:** A on the refusal path (stay wide) to show the refusal costs nothing.

### Does the earned width pay for anything?

#### 15. Offer the earned width to a third learner, and charge the C order for it (P)
- **Mechanism:** After the fold, give the released slot to an independent writer D. Credit the scheduler only with D's gain, minus any A or C loss from reordering.
- **Novelty vs nearest prior art:** MRS11's offer to another blind pair; parent card 18 does it after an exact fold. This prices the reordered C stream.
- **Cheapest first test:** W1 plus one extra quadratic unit for D; compare D's loss with earned fold, blind decay fold and permanent split.
- **Old-task retention check:** A and C after D's first two writes.

#### 16. Earn the fold earlier than blind decay, not just eventually (I)
- **Mechanism:** Momentum echoes decay by β per step anyway. Credit the schedule only for the steps by which it beats blind decay on the same C data.
- **Novelty vs nearest prior art:** This is the falsifier against control (5): if decay alone reaches the closure set before the consumer, the scheduling primitive adds nothing.
- **Cheapest first test:** W2 with zero-gradient C batches (pure decay) versus truthful C batches; report steps to closure.
- **Old-task retention check:** A at both fold times.

#### 17. Beat the stacked control or stop (I)
- **Mechanism:** Compare against exact state transport at the earliest time + blind decay + merge-aware training + exact recertification, at equal width-steps, bytes, information and floors.
- **Novelty vs nearest prior art:** Ledger rule for merges; MRS11 must beat this union, not weight-only folding.
- **Cheapest first test:** W1/W2 with all eight contract controls; report the width-steps saved over the stack.
- **Old-task retention check:** A, B, C at the fold and two U steps later for every arm.

#### 18. Fold at a public time chosen before training (P)
- **Mechanism:** Fix τ and the C order from public information before the window, so the narrow learner and a partner can plan around the return. Refuse if the certificate fails at τ.
- **Novelty vs nearest prior art:** Adaptive pruning picks shrink time from the run; a public τ lets a third party book the width in advance, which an adaptive time cannot promise.
- **Cheapest first test:** W1 with τ = 2 fixed; measure refusal rate over random truthful C pairs.
- **Old-task retention check:** A at τ on accepted and refused runs.

#### 19. Make the earned fold safe for a second split (I)
- **Mechanism:** After folding, split again for a new task. Require that the second split's echo starts at zero, i.e. the carried slot holds everything a later split will read.
- **Novelty vs nearest prior art:** Parent question 4 asks receipts to survive reuse; here the risk is a slot deleted at the first fold that the second split needs.
- **Cheapest first test:** W2: fold with m_a only under read-out U, then split under full U; report gap.
- **Old-task retention check:** A after the second split's first step.

#### 20. Use C-batch gradients as the fold's proof transcript (P)
- **Mechanism:** The verifier replays only the required C batches and the fold map, so the proof costs one forward and backward per C batch, already paid by training. Publish the echo after each batch as the transcript.
- **Novelty vs nearest prior art:** Verifiable training replays whole runs; this proof covers only the fold claim and reuses the training's own computation.
- **Cheapest first test:** W1: transcript length and bytes versus re-running the wide reference over U.
- **Old-task retention check:** A recomputed from the transcript at the fold.

#### 21. Let two partners earn the fold together (P)
- **Mechanism:** Two blind partners each run their own required work. The pair folds when the sum of their echo contributions is zero, without revealing magnitudes, using the parent's sign certificates for the two forcing terms.
- **Novelty vs nearest prior art:** Paired counterweights cancel joint effects at merge time; this cancels the optimizer echo during the work, so the fold is exact for future updates too.
- **Cheapest first test:** Two W1 copies with opposite amplitude echoes; search over each side's own C order only.
- **Old-task retention check:** Each partner's A floor and the other's B after the joint fold.

#### 22. Refuse when the only earning orders are oracle orders (I)
- **Mechanism:** Measure how much of the earned fold comes from an order that needs future labels or the partner's private gradients. Count only orders a causal, non-oracle scheduler picks.
- **Novelty vs nearest prior art:** This is the ledger's oracle control applied to C ordering; W1's exact pairs were found by grid search over residuals, which is an oracle.
- **Cheapest first test:** W1: compare the grid oracle with a causal rule that sees only the current echo and the next candidate batch.
- **Old-task retention check:** A under the causal rule's chosen order.

#### 23. Stop forgetting during the wait (I)
- **Mechanism:** While waiting for the echo to die, the split is still wide and still training. Bound A drift during the wait and refuse if staying wide plus waiting costs more A than a permanent split.
- **Novelty vs nearest prior art:** Elastic-network pruning reports final size and accuracy; this charges the forgetting incurred while earning a fold.
- **Cheapest first test:** W1: A drift during the two C batches versus permanent split on the same batches.
- **Old-task retention check:** The A drift during the wait is the check.

## Ranked deeper questions

1. **Can a causal schedule of truthful C batches reach the closure set under an old-task floor, faster than blind decay?** Use 03, 04, 16 and 22. W1 shows exact earning exists but its best grid solution moves old outputs by about 2.52. If no causal order earns the fold under the floor before the consumer, MRS11 reduces to decay plus exact transport.
2. **What is the right definition of "first sensitive consumer"?** Use 05, 06 and W3. A first-step check passes on W2's read-out-slot echo. Find the weakest reader-graph condition that is equivalent to closure under U, and show it is cheaper to check than the closure fixed point.
3. **How much does work shrink the minimal slot, and what floor survives?** Use 10–14. Classify, for SGD, momentum and Adam, the slot that every reachable post-C state needs, and the slot that no truthful C budget can remove.
4. **Does the earned width buy a write that the stacked control cannot?** Use 15, 17 and 18. Hold width-steps, bytes, information and floors fixed. If exact transport at the earliest time plus decay plus merge-aware training ties, the work-earned fold is not a new learning primitive.

**Verdict:** Keep MRS11 as a conditional candidate. The witnesses show (a) the hidden echo is created by different gradients on the same batch, (b) truthful work can zero it exactly, but non-monotonically and order-dependently, (c) in the toy the exact solutions cost the old task more than its value, and (d) the smallest slot and the consumer deadline both depend on U, and a first-step check can pass on a state that is not closed. Count width as returned only on a closure certificate before every reader's deadline, with A under its floor, and only if it beats the stacked control.
