# Relation parks: keep the old read, move both weights

**Status:** Ideas and paper fixtures only; no learner runs, implementation, or GPU work. **Parent:** [Order-free parked replacements](parked-replacements.md) ([PR #244][parent-pr]). **Seeds:** Parent cards 05 and 09, the two score-3 ideas in [flood-triage row 358][triage]. **Read first:** [Idea ledger][ledger].

## What would count

**Park a read relation, not a dormant weight.** Name two coordinates x,y used by real serving readers, a public relation R(x,y)=r, and the fixed interface that reads it. Check that neither coordinate can be removed without affecting a live read, and that both change on useful ordinary B training updates. Old normal A and rare C may depend on more than R; their independent floors still apply. A model can be in a relation park without all old-task outputs being functions of R. R, r, entry/clear, and data membership are public; none can depend on an unobserved history. Certify all carried slots, clocks, and other live state compatible with entry, not just one lucky initial value.

**Repair the worst reachable transition, not the gradient at entry.** Use only truthful records available before the cutoff. Exchange one record from each of two equal-size batches, preserving all IDs and multiplicities; for a non-additive objective swap only whole legal units. Rebuild the candidate's own reachable prefixes, using the actual optimizer and batch loss. A specific previously failing prefix/read must now pass, and **every** legal prefix must pass before issuing the partition. The original offending order is replayed by batch IDs after changing their contents; it is not imposed on the loader. Swaps are compiler moves before membership freezes, never actions during the build. Include every required B read at its deadline, a frozen final B witness, one public clear, and a real held-out continuation. No optimizer projection, label edits, skipped reads, or hidden order fences in the candidate.

**Proof handle.** Let `T_i` be the ordinary update on full state, `E_P(U)` a sound joint envelope for partition P after the completed IDs U, and `q_j` each reader's fixed violation score (positive means failure). Check that `T_i(E_P(U)) ⊆ E_P(U ∪ {i})` and bound all due readers there. For an affine read with normal n and plain SGD, the one-step relation displacement is `−η nᵀg_i(w)`. Its variation from an anchor to a reached state w is the integral of `−η nᵀH_i v` along their connecting segment (v is the displacement). A derivative sketch therefore needs a valid segment bound or exact discrete transition check. For a nonlinear R this is not enough: check the finite change `R(T_i(s))−R(s)`, which also includes the read's own curvature. With momentum, preconditioning, kinks, or rounding, bound the actual finite map on reachable weight/slot pairs, splitting only where needed. A sound but loose bound can say **unknown**, not that every partition fails. A smaller Hessian norm or a safer endpoint proves neither relation closure nor prefix retention.

**The comparison that can kill it.** [Preview rebatching][rebatch] already proposes gradient/cross-curvature balancing (#14), joint Adam slots (#15), and a proof-carrying swap that repairs the worst arrival (#20). Calling that compiler with a new reader is not a primitive. [Commuting writebacks][commute] already checks reachable live reads under both orders; [GraB][grab] chooses an order rather than accepting every order of a frozen partition. [OGD][ogd], [ONG][ong], and [control minimization][control] can protect old behavior by changing the learning step or its dynamics. Compare against the best independent live park + strongest curvature-aware rebatching + reachable verification, and against a **joint exact** search over the same allowed relations and partitions on tiny instances. The exact oracle defines the feasible set; a reusable operation can match it more cheaply or exploit a legitimate larger action language that is also given to the setup controls, but cannot beat it on the identical feasibility problem. Also compare inactive-unit parking, freezing either coordinate, exact finite-step constrained updates (not just a stale-gradient projection), random swaps, GraB, a strong fixed order, and tuned accumulation. Match useful B progress, old floors, sample exposure, wall-clock/read deadlines, width, slots, preview/checking cost, and peak bytes, including receipts. Require an interaction with the live relation that disappears on an appropriate flat, inactive, or conventional-park control.

## Two paper fixtures (feasibility and falsifiers, not wins)

Use `e=(x+y)/2−2` and `z=(x−y)/2`, so x=2+e+z and y=2+e−z. Start at (e,z)=(0,0). SGD in x,y at step size 2h induces a step of size h in e,z. Batch loss is the mean of its records' losses. In both fixtures A's normal read is `2+e` with error tolerance 1/8. Hold out C reads that separately use x and y with accepted values in [1,3], and a rare read `(x+y−4)²` with maximum 1/16. These are specified serving checks, not B training losses. Both coordinates stay live and change, but this does not prove a reusable entry, a useful clear, or an advantage over the strongest stack.

### W1. The pair moves; the affine relation does not

Four records, one for each `σ∈{−1,+1}` and `r∈{1/2,1}`, have squared losses `(e+σ(z−r))²/2`. The two sign inputs read different coordinates (e+z=x−2 and e−z=y−2), with corresponding fixed targets. Use h=1/2. Match opposite signs with common r in each size-two batch. Its loss is `(e²+(z−r)²)/2`, so from e=0 the ordinary step leaves e=0 and sends `z→(z+r)/2`. The two orders visit z=(1/4,5/8) and z=(1/2,1/2), respectively. A/C pass every read; B can require z≥1/4 after the first batch and z≥1/2 at completion. A held-out ordinary follow-up with loss `(z−1/2)²/2` leaves e=0 and z between 1/2 and 9/16. Pairing opposite signs at **different** r moves e by ±1/8 on the first step (breaking exact R even at the old floors); grouping the signs separately moves e by ±3/8 and fails old reads. Freezing either coordinate while maintaining the exact relation fixes the other and prevents B progress. Exact projection onto the affine relation, however, leaves the good updates unchanged. W1 does not distinguish a park from exact constrained training at matched progress.

### W2. Same entry gradient and Hessian, different second read

Four lawful record IDs have input signs k=(+1,+1,−1,−1). Use the continuously differentiable, piecewise polynomial feature `φ(z)=max(z−1/2,0)²`. A record's genuine two-output squared loss is `[(z−1)²+(e+kφ(z))²]/2`: the second output can equivalently be `1+k e+φ(z)` with target 1. Use h=1. At entry all records have gradient (0,−1) and Hessian I in (e,z); the first batch always reaches (0,1). Here `φ=1/4`, `φ′=1` and the mixed curvature `∂z∂eL=k`. At the second batch,

| Partition | Both first reads | Final (e,z), by order | Result |
|---|---|---|---|
| Same signs together | (0,1) | (−1/4,3/4) or (+1/4,3/4) | Both orders fail A and the rare squared read |
| Swap one + and one − | (0,1) | (0,3/4) in both orders | R and A/C pass, with identical B progress |

B can require z≥3/4 at both ticks. One held-out ordinary update with loss `(z−7/8)²/2` moves the successful endpoints to (0,7/8), still passing A/C; this is not a capacity or clear test. Even entry Hessian matching cannot distinguish the partitions. Fixing one bad order would not help; setting φ≡0 makes every partition safe and removes the need for the swap (use the same minimum B requirement, not an exact final z equality across worlds). W2 is also a negative for novelty: a relation-blind compiler with perfect reachable curvature checking and access to these fixed reads finds the exact same swap.

## Idea cards

**P** = conditional primitive candidate (the new operation is named in the mechanism); **I** = improvement or falsifier, not a primitive. Each first test is a paper or CPU-sized proposal, not a result. Run readers on every requested prefix (including before entry, through clear and after one lawful follow-up), and price every refusal or stall separately rather than counting preserved A/C on a no-build arm as successful replacement.

### Keep a relation live without freezing its participants

#### 01. Let a live pair carry its own old-read constraint (P)
- **Mechanism:** Publish a two-coordinate park and attach an admissible family of ordinary batch memberships that maps it into itself while preserving directed motion on B. Reuse the data-only contract without any post-start projection.
- **Novelty vs nearest prior art:** Parent #05 proposes the relation and [OGD][ogd] enforces a tangent condition by changing updates. The reusable operation here is a fixed reader/loader interface with a lawful membership class, not writing `x+y=constant`.
- **Cheapest first test:** Extend W1 with a new residual level chosen after registration; use the same loader rule, then compare frozen coordinates, exact constrained SGD, and an inactive park with exact batch search.
- **Old-task retention check:** Keep both independent C readers in scope; harden one interval into a tight target to expose an overly broad registration.

#### 02. Teach finite chords of a curved relation (P)
- **Mechanism:** Use truthful record pairs that induce finite, ordinary endpoints on a curved level set even though the resulting chord is not tangent at its start. The park witness says when a batch is an on-manifold transition, not when a directional derivative vanishes.
- **Novelty vs nearest prior art:** [ONG][ong] and retraction-based constrained optimization alter the update geometry. The candidate is realizing the chord through unmodified finite batch updates at lower total cost than an exact retraction or a change of variables.
- **Cheapest first test:** Search small rational pairs on `xy=1`, first for a truthful least-squares realization of two reachable transitions, then for closure over both batch orders. Use exact retraction and tangent SGD as controls; do not hand-code arbitrary state transitions and call them gradients.
- **Old-task retention check:** Read the product and both old single-coordinate outputs; add a third order-conditioned start where a first-order certificate misses finite-step drift.

#### 03. Use a two-sided slot fiber instead of a reset (P)
- **Mechanism:** Bind the relation to a **set** of complementary carried velocities. All slot aliases sharing the public view must map into admissible fibers under each unused batch, with no motion erased at entry.
- **Novelty vs nearest prior art:** [Sealed gates][seal] already certify activation/slot closure and reset is a strong simpler alternative. The new use is keeping a nonzero antisymmetric slot as immediately useful B credit without using it as private park state.
- **Cheapest first test:** In W1 add heavy-ball with symmetric uncertainty in tangential velocity. Cross matched-total-budget no-reset, zero-slot and exact projection of the joint update; add one normal-velocity alias to force refusal.
- **Old-task retention check:** Read A/C on the first update, after the worst tangential overshoot, and on a zero-gradient coast where the carried normal component would wake.

#### 04. Teach a lawful reader to use the pairing before B is known (P)
- **Mechanism:** During normal old-task work, fit a receiver that uses the same public combination under both coordinate directions. Freeze its API before B appears; later verify that raw B batches preserve the receiver and that competing old uses of either donor survive.
- **Novelty vs nearest prior art:** [Commuting writebacks][commute] learns a shared C receiver and [control minimization][control] changes how preservation enters learning. The candidate pays for future all-order batching by changing a real deployed read dependency, not by replacing its tests.
- **Cheapest first test:** Train a two-feature linear receiver on truthful old examples, then compare independently fitted receivers and a behavior-matched reparameterization across two unseen equal-size build pools.
- **Old-task retention check:** Match normal A and rare C before registration; perturb each donor on held-out inputs to prove neither is merely decorative.

#### 05. Make two overlapping relation parks expose their shared cost (P)
- **Mechanism:** Register local pair relations on a shared graph. An ordinary batch either moves in their joint feasible directions, or returns a witness of which pair consumed the last useful degree of freedom. Do not add the pairs' individually available motion budgets.
- **Novelty vs nearest prior art:** [OGD][ogd] already intersects linear restrictions as a nullspace. A candidate requires pair certificates that can be bound or withdrawn locally with lower checking cost than full projection/verification while recognizing incompatible cycles.
- **Cheapest first test:** Use x+y and y+z on a three-coordinate path, then activate x+z to kill its last degree of freedom. Compare exact joint nullspace and incremental factorization, not separate weak projections.
- **Old-task retention check:** Keep readers for every active edge and a held-out cycle-sensitive C reader; refusal must leave the first registrations serving.

#### 06. Hand the park from one live pair to another (P)
- **Mechanism:** Issue a public handoff only if a normal batch lands in the overlap of two relations over all reachable histories. Then retire the first pairing and use its released direction for a second build, with prior B already serving.
- **Novelty vs nearest prior art:** Parent #18 reuses released capacity and [RCU][rcu] versions or waits for readers; here the transition trades a constraint carried by live shared weights rather than reclaiming a parked unit.
- **Cheapest first test:** Use two intersecting strips on x,y,z with a genuine overlapping B deadline, then make the intersection one tick too late. Compare continuing both relations, exact joint scheduling and a temporary extra channel.
- **Old-task retention check:** Run the original A, both rare donor reads, and the first B on handoff and after the second build; do not count a handoff that drops the reader of the retired pair.

#### 07. Preserve a signed relation through a branch change (P)
- **Mechanism:** Certify a controlled crossing of a ReLU/normalizer branch where different finite expressions represent the same public old read. Batch membership, not a post-step correction, has to reach the common value on all incoming states.
- **Novelty vs nearest prior art:** [Sealed gates][seal] keeps a branch shut. The candidate lawfully **changes** branches while retaining a fixed reader contract and a live B transition, distinct from cheaply avoiding the branch.
- **Cheapest first test:** Enumerate sorted endpoints in a two-ReLU model with one order crossing early and another crossing late. Compare exact piecewise constrained SGD and a static no-crossing park at equal useful B target.
- **Old-task retention check:** Place independent C inputs just to both sides of the kink, not just in the cell seen by the training batches.

#### 08. Distinguish a useful live pair from a basis rotation (I)
- **Mechanism:** Use two counterfactuals: perturb each donor without disturbing the other to reveal live read dependence, then transform weights, the optimizer **and** every reader by an invertible chart to test whether the entire scheme is just freezing one transformed coordinate.
- **Novelty vs nearest prior art:** [ONG][ong] and [commuting writebacks][commute] already motivate coordinate controls. This is a falsifier; the mere fact that both raw numbers moved is not novelty.
- **Cheapest first test:** Apply the exact e,z transformation to W1, preserving the optimizer and exposure. Add a nonlinear chart and charge the induced optimizer rather than silently substituting Euclidean SGD.
- **Old-task retention check:** Compare pulled-back normal A and independently perturbed C on the same inputs and times; a different definition of an old task invalidates the comparison.

### Swap for reachable effects, not for an anchor statistic

#### 09. Aim a swap at the first bad reached curvature branch (P)
- **Mechanism:** Return the offending prefix, reader and signed cross-derivative on the region entered by that prefix. Seek candidate exchange partners that cancel the coupling there and verify the changed partition globally.
- **Novelty vs nearest prior art:** [Preview rebatching][rebatch] #14/#20 already combines curvature and witness-directed repair. A distinct result needs the **live relation** to expose a cheap, correct repair sign that joint checking with an otherwise matched conventional park cannot exploit.
- **Cheapest first test:** Extend W2 to three batches and two thresholds, including a change that repairs the first old branch but exposes a second. Compare entry gradients, entry Hessians, ordinary reachable-curvature rebatching, random swaps and full enumeration.
- **Old-task retention check:** Check off-training C at both thresholds under the newly worst order, not only on the repaired relation's first failure.

#### 10. Require a crossed park-by-swap advantage (P)
- **Mechanism:** Keep two usable public relations and two legal candidate exchanges. Issue a pair only when its own reached directions make the exchange safe and a conventional selection order (choose park, then swap) would spend more to find it or miss it under the same budget.
- **Novelty vs nearest prior art:** Parent co-design and [preview rebatching][rebatch] already permit search. The operation to earn is a small **compatibility test** between a relation and an exchange, with predictive value on a new pool, not the existence of a 2×2 interaction.
- **Cheapest first test:** Construct two old read normals and mirrored W2 couplings. Fill the full 2×2 table with exact reachable margins; compare returning all feasible pairs to the best joint exact oracle and timed heuristics.
- **Old-task retention check:** Both parks must serve the same ordinary A and rare C, and all four cells must use the same B deadlines and held-out continuation.

#### 11. Carry old proofs across a membership exchange (P)
- **Mechanism:** Invalidate proof edges depending on the swapped IDs, then replay changed incoming envelopes. Reuse an unaffected suffix only when the changed envelope is included in its certified input and its reader/clock promises remain unchanged.
- **Novelty vs nearest prior art:** Incremental model checking and [preview rebatching][rebatch] already supply counterexamples. An exchange receipt is interesting if a learned pair relation makes reusable subproofs strictly smaller than generic incremental checking at the same admissions.
- **Cheapest first test:** Exhaust four batches; swap two records so an unchanged third batch starts on a different branch. Compare cold enumeration, generic cached reachability and relation-indexed proof reuse. Charge invalidations and cache bytes.
- **Old-task retention check:** Recompute A/C on all orders as an audit of reused edges, especially the first unchanged batch reached by a changed prefix.

#### 12. Repair a cycle of exchanges without ever serving an unsafe intermediate partition (P)
- **Mechanism:** Allow a bounded cycle of equal-size pair exchanges inside the compiler; materialize only the final partition. Certify why each one-swap safe repair is impossible in a declared local neighborhood while the combined exchange repairs the named witness.
- **Novelty vs nearest prior art:** Local search escape and [preview rebatching][rebatch] #20 already motivate multi-swap search. A conditional object is a small witness of a joint exchange across different live reader relations, cheaper than searching all neighborhoods.
- **Cheapest first test:** Enumerate three batches with A and C violations on different edges. Plant a length-three record cycle and compare random multi-swaps, constrained matching and full exact search.
- **Old-task retention check:** No intermediate plan is served; check every A/C read on the final plan and keep old service live during compiler time.

#### 13. Certify the signed directional remainder instead of shrinking the step (P)
- **Mechanism:** Carry opposite signed reader-normal effects along reached tangents jointly, with an explicit bound on the omitted remainder. Prefer exchange partners whose relation-specific cancellation leaves a large lawful B step.
- **Novelty vs nearest prior art:** [Preview rebatching][rebatch] #14 already sketches cross-curvature. The extra claim is a **joint paired bound** with cross-record correlations that beats independent norm bounds and a retuned step size, even with identical retained derivatives at entry.
- **Cheapest first test:** Make two records have identical individual curvature bounds but opposite slope on the same reachable segment; shuffle their segment alignment while preserving entry statistics. Compare interval arithmetic, exact piecewise bounds, and tuned small steps.
- **Old-task retention check:** Query A and C at both extremal reachable states and at the first missed B deadline under the smaller-step control.

#### 14. Exchange for adaptive step curvature, not raw loss curvature (P)
- **Mechanism:** Score an exchange by its finite effect through correlated numerator/denominator slots and the park's old read. Cancel only after applying the legal optimizer, not by averaging squared record gradients or treating the diagonal preconditioner as fixed.
- **Novelty vs nearest prior art:** [Preview rebatching][rebatch] #15 already shapes joint Adam slots. The conditional advance is one transferable two-coordinate cancellation rule covering multiple warm-slot aliases without extra resets or wider generic certificates.
- **Cheapest first test:** Enumerate warmed Adam states in which a raw-gradient-balanced pair has unequal denominators; cross cold/warm states against exact full-state verification, warm-slot reset and an optimizer-aware conventional park.
- **Old-task retention check:** Probe immediately after the exchange's candidate batch and on the same next lawful update; include a rare C reader sensitive to the lower denominator.

#### 15. Learn which old read vetoes exchanging a record (P)
- **Mechanism:** Keep a small public bank of signed counterexamples from old A/C reader types. A witness proposes a swap; a *different* fixed old reader may veto it. Freeze the veto representation before an unseen pool.
- **Novelty vs nearest prior art:** Counterexample-guided verification and [OGD][ogd] already collect old constraints. A candidate must transfer vetoes that remain tied to the two-coordinate relation and cover the real rare reads better per byte than old-example replay or a generic witness bank.
- **Cheapest first test:** Cross W2 with a second old read that fails for exactly one initially promising exchange. Hide a later pool and compare same-byte old replay, exact verification and a random witness-bank ablation.
- **Old-task retention check:** Score withheld old C slices under both accepted and vetoed partitions; a false accept is worse than missing a candidate.

#### 16. Break a fake curvature win with a flat reachable control (I)
- **Mechanism:** Hold entry derivatives and directions fixed while removing the nonlinear coupling on **every** reached state, not only at an anchor. Test whether a simple entry-gradient rule now ties.
- **Novelty vs nearest prior art:** This is a necessary negative, not a new compiler; [GraB][grab] and [preview rebatching][rebatch] should suffice when the claimed curvature term is absent.
- **Cheapest first test:** Use W2 with φ identically zero, plus a twin whose φ is flat at the first tick but activates at the third. Check actual reachable states rather than labeling both flat from entry derivatives.
- **Old-task retention check:** Match A/C floors and minimum B targets across both worlds; examine old loss at the late tick where the deceptive twin actually changes risk.

### Ask what the combined operation buys

#### 17. Prevent a swap from buying safety by suppressing learning (I)
- **Mechanism:** Require each accepted all-order plan to preserve a real tangential B milestone. Compare at matched B progress or across the whole old/new frontier, not at equal step count alone.
- **Novelty vs nearest prior art:** [Preview rebatching][rebatch] #19 already preserves a useful B spectrum. This is a falsifier for apparent curvature gains caused by smaller updates or systematically easy records.
- **Cheapest first test:** Add a low-curvature no-progress exchange and a high-curvature useful one to W2. Match effective B movement with tuned LR, stratification and accumulation; require a real early B read.
- **Old-task retention check:** Keep A/C per-reader loss and worst-prefix margins at each matched B threshold; refuse to compare an old-only trajectory to a building one.

#### 18. Put the exchange at the unit that creates the mixed curvature (P)
- **Mechanism:** For contrastive or normalized learning, pair whole lawful coupled units to make the denominator or group term support the relation. Derive from the full batch loss; separate this effect from additive cancellation of individual gradients.
- **Novelty vs nearest prior art:** Parent #10 already keeps non-additive units intact. The added candidate is a relation-preserving exchange that works **because of** a group-level interaction absent in its additive twin.
- **Cheapest first test:** Use four intact two-record contrast units; replace joint normalization with a frozen denominator while matching the entry derivative. Compare exact lawful rebatching and an illegal split as a diagnostic only.
- **Old-task retention check:** Use deployed old normalization and measure normal/rare old groups whose running statistics the contrast units can disturb.

#### 19. Carry a frozen relation certificate into an unseen pool (P)
- **Mechanism:** Ship a public map from *observable* record signatures and slot bounds to a small set of legal exchanges. On the next lawful visible pool, verify its premises and refuse unmatched types; do not learn a new relation from the identities of unseen histories.
- **Novelty vs nearest prior art:** [Preview rebatching][rebatch] asks for proof reuse across unseen windows. A result needs a relation-induced sufficient signature that reduces new-pool verification or exposure compared with generic cached rebatching.
- **Cheapest first test:** Register a W2-like signature on one threshold family, hold out a second and a sign-matched counterfeit with different curvature, then compare fresh exact checking, identical cached bytes and the borrowed certificate.
- **Old-task retention check:** Check the old readers at both thresholds and on a second window; the counterfeit must be refused or correctly repaired rather than falling outside a post-hoc scope.

#### 20. Borrow a directional degree of freedom only until an old deadline (P)
- **Mechanism:** Reserve one degree of freedom inside the relation for a pending rare old reader. A swap may use it only if all orders replenish its admissible range before that reader is due, without a receipt-dependent flush.
- **Novelty vs nearest prior art:** [Route budgets][routes] and the parent already account for route expiry and service slack. Here the obligation being spent and returned is a reachable direction of two actively serving weights, not an extra carrier or generic margin.
- **Cheapest first test:** Give C a fixed external deadline and B a real earlier two-batch use. Move C one tick earlier as a no-go twin. Compare exact contingent scheduling, a wider park and a best fixed order under the same arrival rights.
- **Old-task retention check:** A must always pass; C must pass at every read promised by its fixed external schedule, including the crossed-deadline refusal and the next replacement.

#### 21. Refuse a complementarity claim when the same swap transfers (I)
- **Mechanism:** Perform a relation- and membership-swap factorial test. Keep the same ordinary update law and readers; test whether the purported relation-specific exchange admits exactly the same useful orders under an inactive or independent park.
- **Novelty vs nearest prior art:** The [ledger][ledger] already rejects stacked-baseline ties. This ablation specifically tests whether changed live coupling caused a better curvature repair or merely changed the vocabulary of its proof.
- **Cheapest first test:** Compare W2's same successful exchange on the relation, a conventional park where access is matched, and a flat twin. W2 by itself should lose this novelty test.
- **Old-task retention check:** Keep A/C and B read schedules fixed across the factorial, report the worst retained margin for each reader, and include clear and the carried-slot wake.

#### 22. Return a bounded obstruction rather than an arbitrary refusal (I)
- **Mechanism:** On a tiny exact action language, separate “every legal pair freezes B,” “every reachable swap leaves a violating permutation,” and “a good build has no common clear.” Commit to the search space before looking at the failed witness.
- **Novelty vs nearest prior art:** [Preview rebatching][rebatch] and the parent already type refusals. This diagnostic separates absence of joint geometry from insufficient records or an inconclusive verifier.
- **Cheapest first test:** Compare a saturated relation graph, W2 with like signs inseparable, and a build whose final slots defeat a public clear. Give a sound over-approximation one valid but refused partition as an unknown control.
- **Old-task retention check:** Serve normal A and rare C on the actual refusal/fallback timeline; do not report untouched weights as a successful old-service outcome if requests were stalled.

## Ranked deeper questions

1. **Can co-design do better than the best lawful park-plus-curvature stack?** Start with 09–11 and 21. Find a crossed instance with the *same* old readers, B deadline, and legally available records where coupling yields a cheaper check or more useful certified windows at a fixed budget. The exact joint oracle must agree on feasibility; discard any result explained by its search space or by W2's obvious mirror match.
2. **Is there a genuine finite-update relation beyond freezing in another basis?** Use 01–04, 07 and 08. Require both coordinates to do independently observable work, with curved or piecewise closure under actual finite batches and carried slots. Stop if the transformed frozen-coordinate or exact retraction control ties in useful progress and total cost.
3. **How much changed reachability must an exchange receipt re-prove?** Use 11–15 and 19. Look for reusable input coverage that survives genuinely new pools and both order signs, including Adam and branch changes. Reject a cheap receipt that checks only the old counterexample, and compare against generic incremental verification at equal proof bytes.
4. **Can the park clear and return capacity without leaving an old-task bill?** Use 05, 06, 17 and 20. Require independent old readers, early useful B service, a public clear, and a second build with a common lawful next update. Kill if the gain is an uncharged deadline, a versioned donor, reduced B work, or an old reader that no longer runs.

**Research call:** First derive a crossed park/exchange instance with exact all-order verification and a real service deadline. W1 only shows that unprojected batches can preserve a live affine pair; W2 only shows that entry gradients **and** Hessians can miss the harmful reached branch. If exact constrained training and the strongest reachable rebalancing stack explain both, keep the two ideas as improvements to the parent, not a new primitive.

[parent-pr]: https://github.com/manojbajaj95/cl/pull/244
[triage]: https://github.com/manojbajaj95/cl/blob/5fec005cdc2b6962a4989be02228c98e46ce50f1/reviews/flood-triage.md#L358
[ledger]: https://github.com/manojbajaj95/cl/blob/5fec005cdc2b6962a4989be02228c98e46ce50f1/reviews/idea-ledger.md
[rebatch]: https://github.com/manojbajaj95/cl/pull/225
[commute]: https://github.com/manojbajaj95/cl/pull/217
[seal]: https://github.com/manojbajaj95/cl/pull/234
[routes]: https://github.com/manojbajaj95/cl/pull/230
[grab]: https://arxiv.org/abs/2205.10733
[ogd]: https://arxiv.org/abs/1910.07104
[ong]: https://arxiv.org/abs/2508.17169
[control]: https://arxiv.org/abs/2602.04542
[rcu]: https://www.kernel.org/doc/html/latest/RCU/whatisRCU.html
