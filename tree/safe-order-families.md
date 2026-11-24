# Safe order families: one frozen bridge, many update orders

**Status:** Ideas only; no experiments, implementation, or GPU work.

**Parent:** [Two-clock examples](two-clock-examples.md) ([PR #187](https://github.com/manojbajaj95/cl/pull/187)).

**Review seeds:** [Flood triage, row 294](https://github.com/manojbajaj95/cl/blob/13e16236ec63452094161841f3c94a3df754b852/reviews/flood-triage.md#L294) keeps two ideas at score 3: **#187.13**, certify all linear extensions of a must-come-before relation for the same frozen bridge; **#187.02**, admit one truthful teaching example only if it works for every optimizer history indistinguishable under the declared probes.

**Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/13e16236ec63452094161841f3c94a3df754b852/reviews/idea-ledger.md). Bounded-delay scheduling died against gradient accumulation; the [replay-deadline null (PR #113)](https://github.com/manojbajaj95/cl/pull/113) requires a smooth no-cliff control. A hybrid must beat the best baselines stacked at equal budget, not their individual parts.

## What the certificate would buy

The candidate primitive is a **reusable right to choose an update order without reopening the proof for a particular bridge**. The exporter certifies a family rather than a schedule; an independent learner can choose a member late using only the permitted transcript. The teaching companion is a certificate that one truthful update makes that right safe over an entire hidden optimizer class, not a claim the update identifies or erases that class. Partial orders, belief-state safety, machine teaching and proof carrying are established ideas. If ordinary contract checking plus a cache matches the result, this is an improvement at best.

- **Order:** Fix the bridge, suffix proof and entry set, named batch instances, legal precedence, optimizer law (including step index, schedules and randomness scope), certified start envelope, and allowed continuations. Publish an acyclic relation `D` containing the hard legal edges. For **every** linear extension of `D`, every compatible initial history and every legal continuation of that execution, check the bridge starts with a valid entry route and reaches its frozen entry set; the lease must cover every lease-sensitive bridge step, and A/C must stay above their floors on every live prefix and after the unchanged suffix. Any continuation not covered by the declared contract is refused, not silently pruned. The bridge uses its frozen public launch rule; do not pick a launch in hindsight. Bind the receipt to the accepted family and validity envelope, not to a single witness run. Require at least two genuinely different orders of B batches.
- **Teaching:** For a fixed transcript `z`, let `H(z)` contain **all** legal optimizer histories with that transcript (or a sound overapproximation). Choose one independently truthful example `e(z)` from the frozen pool, to be applied at its declared teaching event under the ordinary optimizer. The claim is `∃ e ∀ h ∈ H(z) ∀ admitted orders ∀ legal continuations: safe(e,h,order,continuation)`, not `∀ h ∃ e`. Both clocks must work together on the same trajectory. No free slot reads, hidden-state-dependent labels, per-history execution choices, or extra probe from the example unless separately declared and charged. A class can be safely taught even when its successor slots remain unequal. Failure to prove safety is different from a proved empty common-example set.
- **Two clocks:** Entry is about **when a launch can still reach** the frozen entry set, not the last step of that crossing. The lease ends before the first uncovered carry from the omitted slots into a proof-visible read; the boundary convention and covered reads must be explicit. Keep a joint launch predicate (which can close and reopen), rather than combining best-case times from different histories or assuming a single deadline. The admission right may expire; the suffix theorem does not.
- **Compare at equal resources:** Fix the example and batch pools, B utility bands (loss and accuracy), old-task floors, external queue constraints and read precision. Report useful safe imports, missed safe imports, false admissions, covered orders, receipt bytes, issuance and marginal checking work, probes, updates and buffer delay. Charge failures and amortization over blind importers, including their public premise checks. A/C means ordinary held-out old-task performance plus worst protected slices, at prefixes, through bridge execution, and after the common suffix; refusals also get evaluated on their default path. No choice or proof uses these held-out tests. Use exhaustive finite enumeration as an offline oracle, not as a baseline we can claim higher coverage than.

**Nearest controls:** [Pacti](https://arxiv.org/abs/2303.17751) with the same precedence and start envelope; property-aware partial-order reduction (Flanagan and Godefroid, POPL 2005) or exhaustive replay with a whitelist; [reach-avoid](https://arxiv.org/abs/1410.6445) and [partial-observation safety games](https://arxiv.org/abs/0706.2619) with a checked-result cache. For teaching, include same-pool iterative machine teaching, [MTT](https://arxiv.org/abs/2203.11932) restricted to the same truthful pool and update budget, point-estimate teaching, charged slot sensing, separate per-history teaching as a privileged ceiling, and [revealing replies (PR #179)](https://github.com/manojbajaj95/cl/pull/179). The hardest deployable control stacks robust teaching, checked order families, and ordinary cached verification. The [teaching-bundles node (PR #186)](https://github.com/manojbajaj95/cl/pull/186) already considers partial orders that preserve a shared reply; here that order must independently protect both clocks for a frozen import.

## Paper fixtures (sanity checks, not evidence)

**Six updates and one shared example.** Queue `E,T,G,M,X,Y`. `E` sets a reservation to 1 from an initial 0; `M` revokes the route for *new* launches. The fixed launch test is immediately before `G`: the route must be unrevoked and the reservation must be 1. If launched, the bridge latches that reservation and crosses `G` plus one more update; `M` cannot revoke an in-progress crossing. `G` is the only lease-sensitive read before entry. It would expose an omitted masked slot if `|v| ≥ 3/2`; that would end the lease before `G`. The slot is otherwise unchanged except by `T`. `X,Y` are different unit SGD steps on independent B heads with truthful target 1 and initial outputs 0. Their order changes which head is learned first, but the final B outputs match. The other updates do not change these B heads.

Let the free transcript show a masked weight `w = 0` in both histories, with private slots `v ∈ {2,4}`. `T` is one truthful unit-rate step on half-squared error with slot rule `v' = v/2 − g`, leaving `w` masked. Freeze the pool to features `(x₁,x₂) ∈ {(1,1),(−1,1),(0,0)}` with teacher `y = −x₂`; the learner predicts `w x₁`, so the gradients `g` at zero are `1,−1,0`. With `g = 1`, `T` produces `{0,1}`, so the lease covers `G` without coalescence. The relation `E ≺ G, T ≺ G, G ≺ M` has `C(6,4) × 2! × 2! = 60` extensions. Every one has a live reservation at launch, a safe `G`, and at least one following update; `E,T,G,M,X,Y` and `T,E,G,Y,X,M` learn the two B heads in different orders. Dropping any one edge permits an adversarial extension: `T,G,E,M,X,Y` has no reservation; `E,G,T,M,X,Y` carries the unmodified slot; `E,T,M,G,X,Y` misses launch. Bind ordinary A/C outputs to untouched coordinates for this arithmetic check; then let `M` set a rare C output to `1 − w_X`, where `w_X` is the B head learned by `X`. From an initial C output of 1 and with floor `1/2`, this requires the extra edge `M ≺ X`; the original clock check alone is unsound for retention.

**An indistinguishable class with no common example.** Keep the same bridge, six jobs and truthful pool, now with private `v ∈ {−4,4}`. With `g = 1` the successor slots are `−3,1`; with `g = −1` they are `−1,3`. Neither passes for both histories, and the null item gives `−2,2`. Each history has a safe specialist, but the unprobed class does not. A pre-`T` sign probe can buy a good choice only if its time/evidence cost fits before `G`. Moving `T` earlier cannot fix the empty intersection in this fixture. As a separate order counterexample, if either `a` or `b` before `c` suffices, four orders are safe and two are not. Every pairwise orientation occurs in a safe order, so no single conjunction of hard-before edges describes all and only those safe orders.

## Idea cards

**P** = candidate primitive, conditional on beating the strongest stacked control; **I** = improvement or falsification control. All first tests are proposed CPU-scale checks.

### Order families: issue, challenge, and reuse

#### 01. Export the partial order, not the winning permutation (P; inherits #187.13)
- **Mechanism:** Carry `D` with a prefix invariant over every enabled transition, pinning the lease and entry guard to one frozen bridge. Let a second learner pick any admitted extension to fit its queue without building a new proof.
- **Novelty vs nearest prior art:** Pacti and partial-order reduction already handle order constraints. The bet is cheaper independent reuse of a two-clock proof without shrinking to a canonical schedule.
- **Cheapest first test:** Enumerate the six-job oracle; make two blind queues prefer different orders and seed an adversarial extension per edge. Compare safe coverage at matched checker time and bytes with a whitelist, cached singleton, Pacti and replay.
- **Old-task retention check:** Evaluate A/C at each certified prefix and suffix, then plant the rare C slice that removes some clock-safe orders.

#### 02. Make every hard edge earn its place (I)
- **Mechanism:** Attach to each nonlegal edge a history and order that fail when that edge alone is removed; generate edge candidates from the first entry, lease or retention failure rather than from observed co-occurrence.
- **Novelty vs nearest prior art:** CEGIS and constraint minimization already use counterexamples; this distinguishes necessary proof constraints from convenient scheduling restrictions, not global minimum size.
- **Cheapest first test:** Add redundant edges and a planted late carry on six jobs. Compare with transitive reduction plus greedy edge deletion, and with exact maximum-coverage search. Look for wider coverage at the same total search cost.
- **Old-task retention check:** Validate an edge needed only by rare A and a decoy implied by other edges; test A/C on all retained extensions.

#### 03. Certify frontiers, not just endpoint states (P)
- **Mechanism:** Map each order ideal to a reachable envelope relating reservation and remaining lease usage. Use an inductive transition check on the frontier, with a special bound at the launch and each bridge read.
- **Novelty vs nearest prior art:** Abstract interpretation and model checking over order ideals are known. The candidate is a frontier interface small enough to reuse without re-expanding source prefixes, not the dynamic program itself.
- **Cheapest first test:** Add two delayed carry updates to the six jobs and compare relational frontier proofs to exact ideal-state memoization and interval reachability at equal bytes; reject if a cheap cache ties.
- **Old-task retention check:** Track rare C between consecutive frontiers so equal endpoint weights cannot mask a transient retention breach.

#### 04. Swap only where a later lease read cannot tell (I)
- **Mechanism:** Guard adjacent swaps by reachable state and future read set, preserving safety during both serializations and at the joined downstream envelope. Do not infer global commutation from an equal pair endpoint.
- **Novelty vs nearest prior art:** Conditional independence in partial-order reduction and parent #07 already cover local swap witnesses. The audit is whether current-output commutation systematically misses future optimizer reads.
- **Cheapest first test:** Compare state-dependent reduction, full-state commutation and logit-only commutation on four jobs with a delayed moment read; count invalid extensions and the proof cost of recovering safe swaps.
- **Old-task retention check:** Read rare A between swapped steps and C after the delayed read; a harmless endpoint alone must not pass.

#### 05. Know when one DAG is the wrong receipt (I)
- **Mechanism:** When safe orders are not closed under the pairwise relation inferred from them, issue a small union of separately checked DAGs or use a stronger schedule language; never merge them into an unchecked superset.
- **Novelty vs nearest prior art:** Disjunctive scheduling and event structures already express alternative precedences. The point is to put a measured ceiling on the hard-before seed's usefulness.
- **Cheapest first test:** Plant the `a or b before c` example and one plain DAG at the same size. Compare the best single DAG, bounded DAG union, exact whitelist and temporal automaton under matched encoded bytes.
- **Old-task retention check:** Independently add a prefix C failure in one disjunct; verify it is not inherited from the other branch or hidden by alternate coverage.

#### 06. Bind entry and lease to the same cut (I)
- **Mechanism:** Store a joint relation between feasible launch, bridge duration and lease-sensitive reads conditioned on the same branch; rule out receipt checking by two independent best-case deadline summaries.
- **Novelty vs nearest prior art:** Time-varying reach-avoid already preserves correlations and nonmonotonic windows. This is a counterexample suite for clock arithmetic, not a new reachability method.
- **Cheapest first test:** Make two probe-matched prefixes whose only valid launch boundaries are 1 and 2 respectively, with no intervening lawful read. Compare a joint product checker to scalar clocks and to a conservative shared-window checker. It must refuse a common launch.
- **Old-task retention check:** Attach different threatened slices of A/C to the two wrong launches and also verify the safe default path.

#### 07. Hand off a partially executed order (P)
- **Mechanism:** Serialize the current down-set, public state check, incurred budget and a conditional suffix proof. Allow another learner to choose any residual extension, without source activations or a reset of the lease.
- **Novelty vs nearest prior art:** Pacti and [certificate entry ports (PR #171)](https://github.com/manojbajaj95/cl/pull/171) support contracts and entry checks. The candidate is transfer of real scheduling freedom after spending some of it, with no uncharged private state.
- **Cheapest first test:** Retire the first learner after two jobs; give a blind importer two allowed B orders and one hidden-slot near miss. Compare full recheck, a checkpoint, and residual replay plus cache at equal transfer bytes.
- **Old-task retention check:** Check ordinary A/C before and after handoff, with a slice that only fails when the recipient resets the spent budget.

#### 08. Check adversarial release times without assuming future arrivals (I)
- **Mechanism:** Couple the order certificate to a public causal dispatch rule under release windows. Prove it can still launch and finish under all allowed arrivals; a legal full order is not proof a live scheduler can realize it.
- **Novelty vs nearest prior art:** Dynamic controllability of temporal networks and online scheduling already address this distinction. The improvement is a quantified cost for offering a CL proof import before the queue resolves.
- **Cheapest first test:** Reveal two of six batches late in opposite orders; construct a feasible clairvoyant extension in each world but no single safe causal dispatch. Compare an exact game oracle, temporal-network checker and earliest-deadline dispatch with equal slack.
- **Old-task retention check:** Measure A/C during the longest idle prefix, during fallback and after the suffix, not just for timely arrivals.

#### 09. Reopen only the obligations touched by a new batch (P)
- **Mechanism:** Certify a newly arrived B batch as a conservative extension of `D` by proving its allowed insertion cuts preserve prior invariants and lease reads. Tombstone the receipt if the batch changes the frozen bridge or if no certified cut exists.
- **Novelty vs nearest prior art:** Incremental model checking already repairs proofs. The candidate is a localized admission operation retaining more safe schedule freedom than append-only reuse without reopening source evidence.
- **Cheapest first test:** Insert one disjoint job and then one job that changes the bias-correction counter without changing logits. Compare append-only, incremental generic checking and full rebuild; the second must not be silently admitted.
- **Old-task retention check:** Test normal A/C at every new insertion cut and an old rare slice sensitive to the delayed slot effect after import.

#### 10. Compose two certified batches of work without double-spending the lease (P)
- **Mechanism:** Compose two independently certified order families using a shared lease ledger plus proved mixed-interaction bounds. Export cross-family edges only where interleaving would permit an early carry or close entry.
- **Novelty vs nearest prior art:** Assume-guarantee reasoning and [leakage leases (PR #176)](https://github.com/manojbajaj95/cl/pull/176) already compose contracts and budget. The extra bet is recovering interleavings between two blind editors, not adding two scalar budgets.
- **Cheapest first test:** Use two two-job families, each safe alone and an unsafe `u,v` adjacency across families. Compare serial composition, Pacti with the same shared resource and exact shuffle checking; measure safe extensions retained per proof byte.
- **Old-task retention check:** Give A/C separate solo floors and a C slice affected only by the mixed adjacency; certify the merged path against both.

#### 11. Publish a proof the optimizer-version change can revoke locally (P)
- **Mechanism:** Identify which edges and invariant clauses rely on each read, learning-rate rule, or slot update. On a version change, recheck that dependency slice before reissuing the receipt; unknown dependencies revoke coverage.
- **Novelty vs nearest prior art:** Proof carry and incremental program verification are generic. The CL claim needs blind revalidation after an optimizer change that cannot be justified by output agreement or a stored replay alone.
- **Cheapest first test:** Swap the exponent in bias correction with weights and probe logits matched at entry; include a version change to an unused group. Compare a full rebuild, byte-matched dependency cache and a version hash requiring full refusal.
- **Old-task retention check:** Independently check later A/C when the changed slot is first read, plus unchanged protected tasks on a version-only sham change.

### Universal teaching: avoid identifying the history when agreement is enough

#### 12. Certify an example for the whole transcript class (P; inherits #187.02)
- **Mechanism:** Issue a single-example receipt whose claim is that the same frozen bridge survives all compatible optimizer histories, including noncoalescing successor slots. Choose the item before the hidden history is revealed.
- **Novelty vs nearest prior art:** Conformant planning and robust teaching already choose common actions. The candidate is a portable training receipt for many hidden histories and independently chosen safe schedules, not a new universal quantifier.
- **Cheapest first test:** Use the positive and opposed-sign classes in the fixtures. Compare point-estimate teaching, same-pool belief search with cache, separately taught histories, and a charged sign probe. Demand exactly the correct accept/refuse verdicts before any blind reuse claim.
- **Old-task retention check:** Check normal A/C separately for each history, then add a B-equivalent teaching item whose later carry damages a rare A slice in only one history.

#### 13. Carry a small certificate that unanimous teaching is impossible (P)
- **Mechanism:** Export a set of probe-equivalent counterhistories covering the whole truthful menu: for every item (and every proposed order class if selectable), a named legal execution refutes it. Carry the obstruction separately from the fallback.
- **Novelty vs nearest prior art:** Unsatisfiable cores, set cover and partial-observation safety games already produce obstructions. Count this only if the obstruction reuses across blind admissions without re-enumerating histories or the unchanged part of the truthful pool.
- **Cheapest first test:** In the opposed-sign class, add two redundant decoys, then add one valid dual-effect item. Compare a cached exact solver, refusal based on slot spread, and a core that must explicitly reopen when the pool grows.
- **Old-task retention check:** Include a truthful item that protects both clocks but fails rare C; the obstruction must account for that item, and refusal must preserve ordinary A/C on fallback.

#### 14. Forget the slot directions this bridge cannot read (P)
- **Mechanism:** Project the transcript class onto a bridge-specific quotient only after proving the omitted directions cannot reach a lease, entry or protected-task read through any admitted suffix. No requirement to make complete optimizer states agree.
- **Novelty vs nearest prior art:** Observability quotients and [optimizer-slot splits (PR #178)](https://github.com/manojbajaj95/cl/pull/178) cover unobserved state. The candidate is a scoped right to ignore it across a schedule family even after a live teaching update.
- **Cheapest first test:** Add an unbounded nuisance slot to a two-coordinate masked optimizer; allow one extra B step to rotate it into a read coordinate in one extension. Compare with exact belief checking and an ordinary backward dependency slice.
- **Old-task retention check:** Put one A and one rare C read outside the bridge's own outputs; reject the projection if either can see an omitted direction later.

#### 15. Keep hidden histories correlated without learning which is real (I)
- **Mechanism:** Use a relational envelope over moments, counters and reservations from the same legal histories. Admit the shared item when the true relation is safe even though a product of marginal ranges includes unsafe, unreachable combinations.
- **Novelty vs nearest prior art:** Relational abstract interpretation and belief set representations already avoid interval blowup. The improvement is measured by restored safe admissions, not a new teaching operator.
- **Cheapest first test:** Build two histories with correlated moment and slot age, then swap the pairing to turn one spurious danger into a real one. Compare a box, polyhedral reachability and exact enumeration at matched verification cost.
- **Old-task retention check:** Check A/C on both genuine history pairs and include one spurious box corner with low C to distinguish conservatism from a real failure.

#### 16. Link receipts for successive teachers without laundering uncertainty (P)
- **Mechanism:** Carry a proved image of the whole class through the first admitted example and schedule; compose the next receipt only when that image fits its premise. If no lawful public observation refines the class, the second teacher cannot select a hidden branch.
- **Novelty vs nearest prior art:** Belief-state filtering and sequential assume-guarantee proofs are prior art, as is the source-free entry port in PR #171. The claim is independently issued teaching receipts can compose without replaying the first learning history.
- **Cheapest first test:** Chain two single-example offers; hold out a path that satisfies both receipts at their original centers but violates the second at one reachable successor. Compare conjunction, cached belief planning and checked image inclusion.
- **Old-task retention check:** Require A/C at both teaching events and bridges; include a C failure caused only by the first example interacting with the second suffix.

#### 17. Price the smallest lawful refinement when the class has no common item (I)
- **Mechanism:** Buy a read only if its partition has a safe item for every branch the policy promises to serve and the read leaves enough time for both clocks. Otherwise retain the refusal or certified fallback, rather than guess the hidden history.
- **Novelty vs nearest prior art:** Value of information and contingent planning already price sensing; PR #179 supplies the closest CL comparison. The audit asks how much of the teaching gain disappears when usable reads are honestly priced.
- **Cheapest first test:** Offer a sign read, a cheaper irrelevant bit and a delayed sign read after `G`. Compare fixed sensing, exact costed belief search and teaching-only under the same binned evidence and queue budget.
- **Old-task retention check:** Verify A/C on both sign decisions, on a noisy/ambiguous outcome that must refuse, and across the delay of the paid read.

#### 18. Widen a teaching class by certified slack, not sampled agreement (P)
- **Mechanism:** Cover a held-out learner family with verified local tubes around legal history sets. Lift the receipt using worst-case propagation of entry, carry and retention slack through the admitted order family; reject boundary-straddling tubes unless refined soundly.
- **Novelty vs nearest prior art:** Interval verification and reachability funnels already lift margins. The possible new use is validating unseen installers with only public membership checks when their private optimizer intervals differ from the source.
- **Cheapest first test:** Move from discrete slots to rational intervals in a masked momentum toy with finite Lipschitz bounds between discrete guards. Compare a sound tube, interval branch-and-bound and exact interval endpoints where monotonicity is proved; include one tube straddling carry.
- **Old-task retention check:** Hold out interval extremes and an interior old-task degradation induced by a nonlinear read; worst-slice bounds, not sampled accuracy, determine acceptance.

### Joint tests: isolate a mechanism that the parts cannot reproduce

#### 19. Search for an example that unlocks several orders, not a better favorite order (P)
- **Mechanism:** Select a common truthful item for the full history-by-order product so the importer still has at least two genuinely different B schedules to choose from. Prefer the item whose proved family fits an unseen queue, not the one that maximizes source-schedule slack.
- **Novelty vs nearest prior art:** Conformant planning can encode the product; parent #11 already unlocks an individual swap. The candidate is reusable multi-order choice whose gain requires verifying cross-history/order combinations jointly.
- **Cheapest first test:** Build a small reward table from an enumerated quadratic or quantized momentum toy: one item safe across all histories for a singleton order, one safe across several orders on a point estimate, and a candidate safe across both axes. Compare against a joint generic solver and the best separate teaching + schedule + cache stack at matched B utility.
- **Old-task retention check:** Audit every cross-pair, including the counterhistory crossed with a legal but adversarial extension that neither single-axis ablation evaluated.

#### 20. Let the importer choose a public mode without reading the hidden slots (P)
- **Mechanism:** Issue a pair of receipts for the same bridge, each binding one fixed example and nonempty order family to a public queue condition. Selecting a mode can use arrivals or a disclosed time budget, never a privately inferred slot value.
- **Novelty vs nearest prior art:** Conditional planning and parametric contracts already branch on observations. The candidate is late selection between reusable evidence packages that each independently satisfy universal teaching, rather than a one-off conditional policy.
- **Cheapest first test:** Give two importers different irrevocable public precedence requirements, each served by a different pair; also give one importer an outside-contract queue. Compare a single robust certificate, an exact policy and Pacti plus a keyed cache at equal bytes and costs.
- **Old-task retention check:** Require old A/C floors for each mode on all compatible histories and after the refused importer's default continuation.

#### 21. Find the amortization point when nobody keeps the source trajectory (I)
- **Mechanism:** Freeze the compiled receipt and retire the issuing teacher; account for successful checks, rejected checks, policy construction and search across a sequence of independent importers with new queues and history envelopes.
- **Novelty vs nearest prior art:** Proof-carrying code and witness caching already exchange issuance cost for marginal verification. This is the economic falsifier for proposed new CL receipt types, not a novelty claim about proof checking.
- **Cheapest first test:** Sweep reuse count and fraction outside scope on held-out tiny streams. Compare a complete whitelist, a reviewed hard-before contract, a semantic proof cache and fresh generic verification. Require a break-even at realistic reuse and no lower coverage or B utility.
- **Old-task retention check:** Independently check A/C for every live admission and refusal path and count violations by scope miss versus actual proof failure.

#### 22. Try to make the two-clock advantage disappear (I)
- **Mechanism:** Ablate the lease-sensitive read, smooth the carry and launch conditions at matched safety tolerances, and try an accumulated update at the same B examples, update latency and public launch opportunities wherever legally comparable.
- **Novelty vs nearest prior art:** The ledger's bounded-delay kill, PR #113 and parent's #17/#19 already predict these nulls. A planted clock cliff or ordinary margin protection is not evidence of a new operation.
- **Cheapest first test:** Compare the hard fixture with smooth loss/margin worlds from independent pools, including a no-request arm. Match prefix task utility, and report when accumulation changes legal launch opportunities rather than giving it an uncharged timing advantage. Kill the proof-specific story if smooth worlds tie the stacked baseline.
- **Old-task retention check:** Match pre-intervention A/C margins, evaluate vulnerable examples throughout delay and bridge, and compare ordinary retained skill with and without any import request.

## Ranked deeper questions

1. **Can sparse must-come-before constraints give independent learners useful freedom at lower verification cost?** Start with 01–03 and 05: enumerate all six-job extensions, try removal of every edge, then test on blind queues. Require coverage beyond one schedule, no false admissions, and a held-out work/bytes win over Pacti plus a checked whitelist or cache.
2. **Can one truthful example certify both clocks without diagnosing or collapsing hidden optimizer histories?** Start with 12–15: count distinct successors and stress the opposed-sign negative control. Compare at equal B and A/C against exact belief search with a cache and a priced slot probe; class agreement, not single-history teacher quality, is the result.
3. **Is there an interaction that separate robust teaching and order verification cannot buy at the same cost?** Use 19–20 with a held-out history-by-order product, plus a deliberately unsafe cross-pair. The generic joint solver is the logical ceiling; the possible win is transferred coverage at lower total cost or higher coverage at a fixed budget, not beating the exact oracle.
4. **Does the claim survive when the clocks are not planted cliffs and the source is gone?** Cross blind revalidation (07, 11, 18, 21) with the smooth, no-carry and accumulated-update nulls (22). If the gain is only a transient toy order effect, ordinary retention protection, or cheaper syntax for a cached candidate, keep the failure cases and stop calling it a primitive.

**Verdict:** Keep the order-family and universal-teaching seeds separate until each passes its own oracle and stacked control. The joint receipt earns primitive status only if it buys reusable safe choice for the same frozen bridge without surrendering B utility or ordinary old-task performance.
