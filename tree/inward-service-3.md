# Inward service III: move the blocker, keep the old work payable

**Status:** Ideas and exact paper examples only; no learner runs or GPU. **Parent:** [Inward service next](inward-service-next.md) ([PR #292][parent]). **Read first:** [Idea ledger][ledger]. **Review seeds:** [Flood triage, PR #292 row][triage] scores **#292#12** and **#292#02** at 3. The first moves the identity of the suffix blocker without raising the minimum old gap, then uses a genuinely later record from the opener's own queue to remove it. The second reassigns already available old-service records along an alternating path so one can recover a swap right without leaving another obligation uncovered. [PR #281][grandparent] distinguishes recovering a suspended right from settling a revoked one; this node keeps them distinct.

## Contract and controls

- Freeze truthful record eligibility, arrival order, indivisible execution units, old slices and deadlines, full optimizer and serving state, tolerances, and suffix menus before selection. Count a record once, even if it can cover several jobs. Check held-out old A/C slices at every exposed prefix, including waits and aborts, by their original deadlines, and under each claimed suffix. Check both B queues separately; a no-show arm gets no record or label from the missing queue. Charge previews, metadata, work, waits and coverage debt. Give comparators the same observations and arrival support, not future arrivals.
- **Blocker handoff:** record signed gaps per reader under the *same* proposed suffix. Service alone and later B alone must not suffice; match minimum gap and, where possible, the full sorted gap vector. Require useful B learning while retaining the opener's gain. Compare with #281#17 residual movement, same-cost slack raising, fixed service order, GEM on all readers, and a fresh exact vector check. Include a handoff to a reader no eligible B record can improve. A lower-dimensional gap summary is useful only if it preserves the refusal, not if it hides a reader.
- **Obligation exchange:** show the live, precision-buffered swap entrance on the full landing tube, an active opposite tail, and feasible payment of every displaced commitment after the actual update. Compare with #281#07 local substitution, deadline-aware matching without a swap predicate, [GradMatch][gradmatch], and exact stateful scheduling on the same available pool. Include a graph with no alternating path. An expired ticket never comes back: a late partner needs fresh admission.
- **Combined claims:** beat the best equal-budget stack of these controls, not two weak controls in isolation. Keep the ledger's [gradient-accumulation null][smooth] for bounded-delay stability scheduling: an order effect alone is not a primitive. Report false admits, refusals, delayed or missed old work, and useful B gains alongside safe on-time suffixes. An exact planner is the decision-quality oracle on small instances; the proposed reusable objects need to save checks/bytes, tolerate partial observations, or expose a usable guarantee the separate controls cannot give at matched cost. A constructed example only separates controls, not prevalence or novelty.

## Two exact paper checks

**B1 — Same sorted gaps, different useful continuation.** Use shared coordinates `(x,y,z)`, native SGD with step `1/2` and fixed losses given by half the sum of squared residuals on the named coordinates. Start after revocation at `(0,1,0)`. A/C gaps without the candidate suffix are `(x,y)`; the candidate subtracts `1/2` from each. An old-service read on separate held-out inputs has error `|z−2|` and is due to reach at most `1`. Record `S` has targets `(2,−1,2)`; comparison `T` trains only `z` toward `2`. Thus `S` yields `(1,0,1)`, and `T` yields `(0,1,1)`. Both pay the declared old job and leave sorted A/C gaps `(0,1)`, but only `S` makes C the blocker. The later own-queue `D` trains only `y` toward `2`; `S→D` gives suffix gaps `(1/2,1/2)`. `D` alone and `T→D` still fail A by `1/2`; `D→S` leaves `y=1/4` and fails C by `1/4`. A slack-raising old record with targets `(1/2,3/2,2)` raises both gaps by `1/4` but still fails A by `1/4` after `D`. Replace `D` with a truthful `z`-only B view and C stays blocked. Unshifted A/C gaps stay nonnegative in every arm, and `D` lowers its own loss after `S` from `2` to `1/2`. An independent opener coordinate is unchanged; this toy does not establish retention of a coupled opener or availability of such old records in a natural stream.

**E1 — The only swap-opening record needs a three-job exchange.** Use the parent's post-drift states `(1,5/4),(−3/2,3/2),(0,0)`, the same `L: y←min(y,1)` and gaps `A=2−x−d`, `C=2−y+d`. Three distinct truthful old records `T,S,U` are already available. They train squared parent residuals toward `y` targets `15/16,5/8,7/8`, respectively, applying `y←(y+t)/2` with `x` fixed. For the coverage toy, each also trains its own independent read `q_j` from `0` to `1` toward target `2` in one step; an obligation observes the maximum of the `q_j` for its eligible records and requires a value of at least `1` at its deadline. Formal payment additionally consumes a unique eligible record; the read alone does not count as payment. The job eligibility sets are `O₀:{T,S}`, `O₁:{S,U}`, `O₂:{U,T}`, with jobs due in that order. The partner can exercise only in the slot after `O₀` and before `O₁`. Default payment `(T,S,U)` puts the repaired landing at `35/32` in that slot, still outside the fixed set; the default uses `S` too late. Instead reassign to `(S,U,T)`. `S` puts that landing at `15/16` and the untreated tail at `17/16`, so lawful `L` fixes the first and repairs the second. `U,T` then pay their jobs and preserve `max y≤1`; both suffix signs are individually safe after `L`, including after all debt is paid. Removing the `O₂–T` edge leaves the default schedule feasible but prevents using `S` first. The swap must be refused even though the state after `S` would be suitable. All executed no-suffix prefixes retain A/C. This is an engineered matching witness, not a win over exact scheduling or evidence that such eligibility sets occur naturally.

## Idea cards

**P** = candidate primitive (a reusable object or operation); **I** = improvement or audit. Nearest-art contrasts are testable claims, not novelty clearances.

### Which reader needs to move? (#292#12)

#### 01. Match the whole margin histogram, not just its minimum — I
- **Mechanism.** Stratify preparations by the sorted suffix-gap vector, and within a stratum test whether the signed gap paired with the later B response predicts safe settlement. This is a stronger diagnostic for the parent handoff, not a different learner update.
- **Novelty / control.** #292#12 matches the minimum. Compare the histogram-only decision against the identity-aware vector check and matched slack-raising A/C service.
- **Cheapest first test.** Use B1 and permute A/C and the B response independently; a symmetric B update that lifts both deficits is the negative control.
- **Old-task retention.** Evaluate each named held-out reader before service, after B, and under the suffix; do not average over the permutation.

#### 02. Compile suffix obstruction sets against realized B responses — P
- **Mechanism.** Represent each suffix by the minimum set of readers it needs improved and index predeclared B record classes by certified response bounds. After the actual record arrives, reuse only the bounds for its executed update; certify the whole vector, including readers it can hurt.
- **Novelty / control.** [GEM][gem] constrains gradients against all old tasks. The proposed object answers multiple subsequent suffix queries from one realized B response, not whether to project the B update; compare with caching full vectors and fresh exact checks.
- **Cheapest first test.** Enumerate three readers, four suffixes sharing two obstruction sets and two B classes; add a B class that repairs the named blocker but creates a new one.
- **Old-task retention.** Check the newly harmed reader as well as each named blocker at every prefix and on every returned suffix.

#### 03. Choose a handoff that survives one intervening old job — P
- **Mechanism.** Compute the set of binding readers that an owed intervening job can expose from each proposed preparation. Accept a preparation only when every such reader can be cleared by the *same* declared B continuation rule using the record actually received.
- **Novelty / control.** #292#13 varies queue order; robust predecessor sets already handle uncertainty. Test whether a reader-response abstraction merges multiple queue traces without unsafe admissions or more checking than full-state predecessors.
- **Cheapest first test.** Enumerate two legal intervening jobs that expose different blockers with identical minimum gaps; exclude the first preparation when one blocker cannot be repaired.
- **Old-task retention.** Check all slices also in the branch where the intervening job exposes the unsupported reader and no B suffix executes.

#### 04. A reader can cease to block without ceasing to be owed — P
- **Mechanism.** Certify a handoff between two independently specified reads of the same old routine: expose which read limits the new suffix without substituting it for the other read's ordinary-input obligation.
- **Novelty / control.** Active-set methods track tight inequalities; #292#12 moves between named readers. Test reuse of a split witness across suffixes when one reader has two modes; compare with treating the modes as unrelated full checks and with aggregation by task ID.
- **Cheapest first test.** Make two held-out subgroups of one routine with opposite response to `D`; vary suffix exposure without changing the normal old tasks. The pooled mean must be able to miss one subgroup.
- **Old-task retention.** Both subgroups must pass normal execution and any admitted suffix; keep the nonbinding subgroup in the audit.

#### 05. Prepare for a B response with a collateral debit — P
- **Mechanism.** Bind clearance and harm in the same certificate. A due A/C record transfers the deficit to a reader B helps while moving an *unrelated* reader into a buffer large enough for B's unavoidable debit.
- **Novelty / control.** #292#12 leaves other gaps safe; GEM and #233 margin repayment already handle interference or debt. Test a joint signed-response envelope against each control and their stack, with identical B gain.
- **Cheapest first test.** Add reader E to B1 and make `D` debit E by `1/4`; a preparation with E slack `1/8` must refuse despite clearing A and C.
- **Old-task retention.** Check E after the debit and the suffix, not just immediately after the preparatory old record.

#### 06. A handoff witnessed by a disagreement pair — P
- **Mechanism.** From two available preparations with matched old progress and sorted gaps, retain a witness that one fixed later B record clears only one of them. Use that pair to test whether a compressed admission statistic preserves the consequential distinction.
- **Novelty / control.** Counterexample-guided abstraction refinement already separates states; #292#21 minimizes evidence for a joint decision. The proposed refinement unit is a matched *executed old-work pair* with a shared truthful B continuation; compare with arbitrary-state counterexamples.
- **Cheapest first test.** On a small record pool enumerate matched pairs and hold out one preparation family; test whether witness-driven refinement eliminates its false admit with fewer probes than full vectors.
- **Old-task retention.** Independently check the old job and the unsupported reader in both members, including the held-out family.

#### 07. Cover a menu without promising every suffix at once — P
- **Mechanism.** Prepare a single state with a declared mapping from realized B arrival classes to different independently safe one-use suffixes. A class outside support yields no option; exercising one option consumes that settlement decision.
- **Novelty / control.** #292#10 prepares for two types and #292#11 reports useful support. Here the conditional object has different output suffixes and explicit mutually exclusive consumption; compare with a robust common suffix or independent certificates for each branch.
- **Cheapest first test.** Two suffix signs and two B types clear different readers; design the concatenation of the two signs to fail although each sign separately succeeds in its own branch.
- **Old-task retention.** Test the realized suffix and an attempted second spend; monitor the reader that fails on that second execution.

#### 08. Certify a reader handoff through quantization — P
- **Mechanism.** Attach a predeclared rounding envelope to the reader-gap vector and executed B response. An admitted handoff can allow ambiguous ties, but every tied candidate must clear under the realized record or the certificate fails closed.
- **Novelty / control.** Interval analysis provides the bounds; the test against #292#12 and full exact-dtype execution is whether a small, reader-local proof avoids checking the many unaffected readers individually.
- **Cheapest first test.** Sweep two gaps separated by less than one representable step with a rational arithmetic oracle; compare exact rounding, a conservative global pad, and reader-local envelopes.
- **Old-task retention.** Run held-out probes at the serving dtype, including the tie case and the least-buffered prefix.

#### 09. Charge for leaving an old reader ready for the *next* job — P
- **Mechanism.** Require the cleared reader to stay usable through the next owed service record without relying on the just-used B record again. Return a suffix together with a one-job forward obligation and the boundary that invalidates it.
- **Novelty / control.** Bounded model checking already handles two-step safety. Relative to #292#12 this certifies *renewability after spend*; compare with a fresh two-step check and with a one-shot handoff plus best independent renewal check.
- **Cheapest first test.** In B1 add two alternative next due jobs, one of which reopens A only after the suffix; verify whether the certificate refuses this option before spending it.
- **Old-task retention.** Check A/C and the next job's held-out read after the suffix and again by that job's original deadline.

### Which old record can be used now? (#292#02)

#### 10. Return the cut that forbids spending a record — P
- **Mechanism.** For each swap-opening candidate, temporarily consume it in the legal matching graph and return a Hall-deficient job set when no schedule remains. Cache that negative witness only until an incident eligibility, availability or deadline edge changes.
- **Novelty / control.** [Hall's theorem][hall] already gives the cut; the candidate is a refusal witness keyed to an otherwise valid learner-state admission. Compare with matching warm starts and fresh exact scheduling, charging cache checks.
- **Cheapest first test.** Use E1 with the missing edge; add an unrelated arrival, then an eligible replacement that invalidates the witness.
- **Old-task retention.** At refusal, execute the feasible ordinary path and check the threatened job and the post-wait A/C floor.

#### 11. Certify a time-expanded alternating path — P
- **Mechanism.** Put job deadlines and available record lifetimes into the residual graph; a reassignment must have an executable timed witness after the one old step that opens the swap, not just a static eligible matching.
- **Novelty / control.** Time-expanded matching is known. Tie the witness to the real fixed/active landing window and pay for its verification; compare with deadline matching followed by fresh state checks and exact stateful scheduling.
- **Cheapest first test.** Shorten `T`'s usable lifetime in E1 so the static path survives but its last payment is impossible; include a deadline extension that restores it.
- **Old-task retention.** Probe A/C while waiting and every rescheduled slice at its original deadline, including the one losing `T` in the negative case.

#### 12. Move a whole commit batch without splitting its grammar — P
- **Mechanism.** Treat an indivisible batch as an assignment hyperedge; a proposed exchange consumes that batch once, only against the commitments its native reduction actually pays, with a witness for all remaining jobs.
- **Novelty / control.** Set packing and batch scheduling are prior art; #292#02 uses single records. Test a small hyperedge witness tied to a native averaged update versus flattened matching, fresh exact scheduling and gradient accumulation.
- **Cheapest first test.** Enumerate two legal pairs and a singleton. Construct a flattened path that reaches the right only by splitting a mandatory pair; include a different legal pair that really opens it.
- **Old-task retention.** Check retention at each actual commit and measure both obligation reads; do not claim service from unexecuted singleton previews.

#### 13. Give two pending rights one budget, not two matchings — P
- **Mechanism.** Maintain a common payment plan for two rights competing for one old record. Consume its assignment when the service executes and revalidate the winning right at exercise; defer the other unless a disjoint continuation remains feasible.
- **Novelty / control.** Resource locking avoids double spend. The candidate supports overlapping *unexercised* rights with state-dependent feasibility and no permanent reservation; compare with locks, first-come, and exact joint scheduling.
- **Cheapest first test.** Build two opens whose individual matching witnesses both spend `S`; add a second truthful record that only one right can use and test both exercise orders.
- **Old-task retention.** Check the job assigned to the shared record exactly once and the previously learned B task of the right that waits.

#### 14. Preserve the option to drop a queued view, not an old slice — P
- **Mechanism.** Require that after spending the opener, the remaining matching can tolerate deletion of any one declared redundant view without missing a mandatory old job. Precompute only the allowed deletion family and make actual loss of a view public before replanning.
- **Novelty / control.** Fault-tolerant matching already models record loss. The proposed certificate discounts a fragile swap opening whose future service needs every redundant view, without reserving a universal spare; compare with exact recourse and fixed-spare reservation.
- **Cheapest first test.** Add two partial replacements to E1 and enumerate single deletions; include a two-deletion trace with no feasible swap-opening payment plan, which must refuse rather than silently drop coverage.
- **Old-task retention.** Execute the contingent payment plan on each allowed deletion and probe the least-redundant slice by its old deadline.

#### 15. Validate an exchange against the trace where the partner never comes — P
- **Mechanism.** Spend a swap-opening old record only when the same remaining old commitments can be met after either timely exercise or no-show. The two continuation witnesses may differ; neither can depend on borrowing work from the absent B queue.
- **Novelty / control.** #292#05 allows outcome-contingent exchanges; here the partner's executed update changes which future records really satisfy old jobs. Compare with contingent matching on static edges and full two-branch exact planning.
- **Cheapest first test.** Use a future A record that restores its held-out read only after `L`, plus a separate record admissible on no-show. Delete the latter and test whether a valid timely path is refused before spending.
- **Old-task retention.** Check both branches, including all A/C debt when the ticket is revoked without settlement.

#### 16. Join proofs at a service-equivalent frontier — P
- **Mechanism.** After different early exchanges, merge search branches only if they have the same remaining obligations and a dominance witness for the *responses* of the still-available old records and live suffixes, not merely the same graph.
- **Novelty / control.** Dynamic programming and simulation preorders merge equivalent search states. The proposed relation includes real old-service and optimizer effects; compare with full-state memoization and graph-only merging.
- **Cheapest first test.** Construct two schedules with the same remaining graph and visible weights but different momentum; one must fail on the next due record. Add a pair genuinely equivalent on all declared continuations.
- **Old-task retention.** Check the momentum-sensitive rare slice when the next record executes and count false merges even when the swap endpoint agrees.

#### 17. Can coverage edges be justified without probing every record–job pair? — I
- **Mechanism.** Audit a small collection of transfer rules for multi-eligible views. Admit an edge only with an independent held-out lower bound on service, and fall back to direct checks where the bound is inconclusive.
- **Novelty / control.** This improves matching inputs, not the matching primitive. Compare with #292#02 using a frozen exact graph, cheap features alone and direct equal-budget probes.
- **Cheapest first test.** Mask one old subgroup from edge construction; test whether a view reported interchangeable by training progress fails that subgroup after its assigned update.
- **Old-task retention.** Check the held-out subgroup at the claimed payment deadline and under the suffix; a spurious edge counts as missed service.

### Interaction tests: exchange work to place a blocker, not to spend it twice

#### 18. A preparation is payable on both sides of the deadline — P
- **Mechanism.** Choose the spendable first record together with two forward witnesses: timely swap plus reassigned old work, or expiry followed by blocker handoff and later own-queue B. Both witnesses pay the same old jobs, each on its own trace.
- **Novelty / control.** #292#17 has two contingent completions; #292#02 has matching. The added operation certifies the coupling where the identical remaining record pool both pays debts and makes the no-show blocker reachable. Compare with the best independently stacked controls and a joint exact oracle.
- **Cheapest first test.** Extend E1 with two post-deadline A/C orders paying the same jobs; only one exposes the reader a later B can clear. Compare records with identical timely landing effects but different matchings on no-show.
- **Old-task retention.** Execute timely and no-show separately, including outstanding old service and retained opener B gain after each completion.

#### 19. A future payment can invalidate a satisfied suffix — P
- **Mechanism.** Mark each repair certificate with the remaining assignments under which its resulting suffix stays safe. Reassigning a job invalidates exactly those live suffix proofs whose protected readers its new payment can reopen.
- **Novelty / control.** Incremental verification tracks dependencies; #292#02 alone checks coverage. Test whether dependency-scoped invalidation avoids full rechecking while catching debts that a static vector check misses.
- **Cheapest first test.** Give E1 two feasible remaining assignments and make one payment reopen C only after a B completion. Replay the same assignment change on an unaffected suffix.
- **Old-task retention.** Check C on the actual payment prefix and on the suffix after reassignment, whether or not it had already passed once.

#### 20. Certify a suffix that readies the displaced old job — P
- **Mechanism.** Allow the useful B completion to improve eligibility of a remaining *already available* old record, but count that edge only after the actual B update and a certified eligibility check. Until then keep a fallback old schedule independent of B.
- **Novelty / control.** #292#14 moves a settlement region using reader state; here B changes the legal payment graph. Compare with fixed-edge recourse, separate reader repair plus matching, and fresh stateful planning.
- **Cheapest first test.** Two candidate records stay available; one can meet a held-out old progress threshold only after B changes its starting residual. Withhold or replace B and ensure the fallback pays on time.
- **Old-task retention.** Check the newly eligible edge on independent old inputs after the record runs, not on the B training loss or the predicted eligibility label.

#### 21. Separate shortage of old work from shortage of B response — P
- **Mechanism.** Over a bounded record pool return paired failure witnesses: a coverage cut after each useful opening, or a remaining reader deficit under each complete old assignment and allowable B response. If neither witness suffices alone, return the smallest joint counterexample set found.
- **Novelty / control.** Infeasibility explanations and active-set certificates are standard; the proposed output separates which *truthful arrivals* would repair a learning-opportunity deficit. Compare with exact enumeration and separate Hall and blocker summaries.
- **Cheapest first test.** Enumerate three streams differing only in removal of an old eligible view, removal of a capable B record, or a conflict between otherwise feasible choices. See whether the witnesses identify the single changed assumption without relaxing old work.
- **Old-task retention.** On every refusal run the normal old-service plan if feasible; distinguish pre-existing old lateness from harm introduced by pursuit of the right.

#### 22. Measure when the stack already buys everything — I
- **Mechanism.** Enumerate a small stream product over record eligibility and reader response while holding deadlines, sorted gaps, old progress and B opportunity fixed. Compare coupled and separately optimized controls at the same budget.
- **Novelty / control.** This is a falsifier, not a new primitive. Include fresh exact recertification, normal SGD on the same records and the best stack of matching plus blocker-aware checks; report no interaction if the stack ties.
- **Cheapest first test.** Cross the E1 edge-deletion arm with matched B1 response permutations and a smooth quadratic arm with no change in safe suffixes. Count only on-time qualified completions.
- **Old-task retention.** Use the same held-out A/C/deadline matrix in all cells, including successful no-show branches and streams with no earned completion.

## Ranked deeper questions

1. **Can a naturally due, deadline-feasible exchange expose exactly the reader a genuinely later own-queue B record can clear, without buying slack or sacrificing old coverage?** First compare #18 and #22 with the best stacked controls on held-out CPU streams; if the interaction only exists on engineered pools or the exact same separate choices suffice at the same cost, keep the two seeds separate.
2. **What is the smallest sound representation of a blocker handoff?** Test #02/#06/#08 on held-out suffixes with matched gap histograms, collateral effects and optimizer aliases. A lossy summary is valuable only if it cuts checking cost without introducing false admits or refusing away the useful cases.
3. **When do service exchanges survive time and execution rather than just matching on paper?** Start with #11/#15/#16: hold eligibility fixed while varying deadlines, partner arrival and momentum. If graph feasibility carries little information about executable debt, prefer stateful verification to a new interface.
4. **Can the learner explain refusal without requesting an old-task waiver?** Use #10/#21 to distinguish missing eligible old work from missing own-queue B response while preserving normal service. If full enumeration is required to produce the explanation anyway, treat it as a diagnostic rather than a scheduling primitive.

[parent]: https://github.com/manojbajaj95/cl/pull/292
[grandparent]: https://github.com/manojbajaj95/cl/pull/281
[triage]: https://github.com/manojbajaj95/cl/blob/6f83d4875382f875fdffcb5a3b2c4f05524658d3/reviews/flood-triage.md#L410
[ledger]: https://github.com/manojbajaj95/cl/blob/6f83d4875382f875fdffcb5a3b2c4f05524658d3/reviews/idea-ledger.md
[gem]: https://arxiv.org/abs/1706.08840
[hall]: https://doi.org/10.1112/jlms/s1-10.37.26
[gradmatch]: https://proceedings.mlr.press/v139/killamsetty21a.html
[smooth]: https://github.com/manojbajaj95/cl/pull/113
