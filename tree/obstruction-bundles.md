# Obstruction-carrying bundles: prove what works and what cannot be shorter

**Status:** Ideas only; no implementation, experiments, or GPU work. **Parent:** [Teaching bundles](teaching-bundles.md) ([PR #186](https://github.com/manojbajaj95/cl/pull/186)). **Review seeds:** [Flood triage, row 293](https://github.com/manojbajaj95/cl/blob/13e16236ec63452094161841f3c94a3df754b852/reviews/flood-triage.md#L293) kept parent **#01** (ship the winning bundle with a smallest set of hidden histories that defeats every shorter sequence-and-reply pair; transfer both bounds without fresh search) and **#08** (certify a common next reply in each fixed-probe bin after a shared reply, without recovering hidden optimizer state) at score 3. **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/13e16236ec63452094161841f3c94a3df754b852/reviews/idea-ledger.md).

## What would count as a new object?

**Not an optimal curriculum plus a log, or a belief policy serialized as a table.** [Iterative Machine Teaching](https://proceedings.mlr.press/v70/liu17b.html), [Nonparametric Teaching for Multiple Learners](https://arxiv.org/abs/2311.10318), and [Matching Training Trajectories (MTT)](https://arxiv.org/abs/2203.11932) already shape learner trajectories. Minimal unsatisfiable subsets and proof-producing SAT already explain infeasibility. [Partial-observation games](https://arxiv.org/abs/0706.2619) and [Causal Belief Decomposition](https://arxiv.org/abs/1909.13778) already handle actions over sets of possible states; [FLEX](https://arxiv.org/abs/2304.13426) already designs informative actions. The candidate object is a **portable, independently invalidatable certificate** coupling a shortest truthful lesson to a decision that remains safe after that lesson, even when the importing learner cannot identify its history. If a generic proof cache and policy verifier give the same held-out service for the same total cost, there is no new primitive.

### Three promises, three validity conditions

- **Upper bound (a winning bundle).** Freeze a truthful example pool, presentation order and repeat rules, update law, hidden-history envelope, free transcript class, reply menu, and old A/C and new-utility floors. Export an ordered length-`k` bundle and one nominated first reply. A universal proof over the import's compatible histories must cover the entire serving path, including every live prefix. The receiver need not know which history occurred.
- **Lower bound (an obstruction).** For each lawful pair `(ordered sequence of length < k, first reply)`, including length zero, at least one compatible counter-history must force a floor violation along its trace. Export a minimum-cardinality set of such histories together with checked coverage of the shorter-pair domain. Deletion witnesses show inclusion-minimality, not minimum cardinality; prove the latter separately on the declared source domain. To transport `k` as a lower bound, an import must establish that its ambiguity class *contains* witnesses with the required failures and that the cover still accounts for every lawful shorter pair. Counter-histories are legal alternatives, not claims about the realized history. A replacement witness needs proof of legality, transcript compatibility, and the same covered failures. If the import admits new shorter pairs, a cover for the old pool does not suffice. If it drops a witness, the lower bound is unknown unless the remaining cover is independently sufficient; the actual optimum need not change. Do not infer that the source witness set is still smallest on import.
- **Next-reply certificate (a decision, not a decoder).** Freeze the first shared reply, subsequent lawful continuations, the fixed probe's timing and quantization, and the next menu. For every reachable bin `b`, export one lawful next reply in the intersection of the safe reply sets of **all** compatible post-reply histories in `b`. If next offers vary publicly, certify each `(offer, b)` using only information available by the decision deadline. Bins can retain substantial hidden variation, and different histories in a bin can have different safe sets. A probed routing claim needs an equal-cost first-reply control for which at least one reachable bin's intersection is empty; if an unprobed policy already serves all bins at equal cost, the probe buys nothing.

**Blind import and shared controls.** Commit the bundle, replies, and proofs before opening held-out editor families. The importer sees only a public family interface, the declared transcript, and the scheduled read; an offline exact referee can see all legal histories after commitment. Neither generating local counterexamples nor recovering optimizer slots is a free import check. Report upper bound, lower bound, and next reply separately as proved or unknown, and never turn an unknown into admission. Compare against cached exact search with routine re-verification, counterexample-guided repair, and MTT on the same truthful pool; for the next decision, use dynamics-fit excitation, FLEX, exact belief-state planning, causal belief decomposition, and the strongest stack of teaching, sensing, and proof caching. Include direct slot access only as a priced ceiling. Match immediate service, A/C headroom, reply work, and scheduled/optional reads. Charge source search, artifact bytes, verification, delay, and failed imports; log refusals and later paid splits. Audit ordinary old A/C evaluations and worst slices independently of the teaching data and probe, at every live prefix and after later writes. A tiny paper fixture validates quantifiers, not novelty or an amortization claim.

### Two paper fixtures, not results

**The upper bound can survive a missing obstruction.** Reuse the parent's two-example fixture: the gate-then-regress bundle sets `q=1/4`, allowing the split `+1/4` repair per lane to meet the A floor `1/2` in both opposite-lane histories `L,R`. Every shorter sequence leaves `q≤3/16`, so the split fails. Every left-only repair fails in `R`, and every right-only repair fails in `L`. The length-zero specialist pairs have disjoint failure supports on this two-world source, establishing a two-history minimum as well as coverage. Keep the source menu and examples but import only `L`: the published winner still works, yet the left specialist meets the floor without any lesson (`1−(1−1/8−1/2)=5/8`). Conversely, adding a same-transcript world where the full bundle fails C can preserve the shorter-pair obstruction while invalidating this winner. The referee, not the importer, observes which world actually occurs.

**A common action without a unique state.** In the parent's momentum fixture choose `h=1/2` and allow initial `v` in `{−1/4,−1/8,1/8,1/4}`. Take only the sign of the same `P(w)=w` read after the two steps, fixed for both arms. Since `w₂=−v/2`, each bin still contains two different momenta. Assign the next specialist obligation by initial sign. Use independent C margin `1−max(1/8, |w|)` with floor `7/8`: both pulses have the same C margin on every allowed step, but larger excursions would fail. The silent `h=3/2` control puts all four histories in the zero bin at the same read budget. Adding a lawful same-sign alias that needs the opposite specialist destroys the certificate for that bin even though readout of the sign is unchanged. That is a decision failure, not a dynamics-fit failure.

## Idea cards

**P** = candidate primitive, conditional on beating the stacked control; **I** = improvement or falsification test. All first tests are paper or small CPU designs, not results.

### Carry the shortestness claim

#### 01. Import a winning bundle and an obstruction together (P)
- **Mechanism:** Address the winning proof by an envelope predicate and the lower proof by checked membership of a minimal set of protected counter-histories. Bind both to one pool, update law, cost and menu version, but permit either proof to survive alone.
- **Novelty vs nearest prior art:** Minimal unsatisfiable subsets and cached exact teaching can already certify the source instance. The bet is that the two opposite scope checks can be reused together across editor families, more cheaply than a generic proof cache plus re-verification.
- **Cheapest first test:** Freeze the paper bundle and cover; hold out a private-output family with both obstruction types, a family with one missing type, and a family with a larger damage envelope. Compare both-bound certifications and total costs with the cached exact and counterexample-guided arms on the same pool as MTT.
- **Old-task retention check:** Score independent A slices, C, and new utility on every published admission, including the upper-only import; the lower-bound flag must never license an unsafe write.

#### 02. Prove a small witness set really is the smallest (I)
- **Mechanism:** View each history as covering the shorter pairs it defeats. Export the cover and a cardinality lower certificate, such as disjoint failure supports of rival pairs in the entire declared source family. If the supports overlap, use an exact integer set-cover proof rather than assuming a packing is tight.
- **Novelty vs nearest prior art:** Set cover and minimum unsatisfiable subsets supply the mathematics. This audits the difference between a minimal justification and a smallest portable payload.
- **Cheapest first test:** Use three rival pairs with failure-support sets `{a,b}`, `{b,c}`, and `{a,c}`. Compare greedy deletion, disjoint-support packing, and exact cardinality; then add `d` that defeats all three and check that an inclusion-minimal old cover need not be smallest.
- **Old-task retention check:** Derive every cover edge from an independently checked A/C or new-utility violation, not a surrogate loss; verify the full winner on `d` too.

#### 03. Keep the dual valid when literal counter-histories cannot travel (P)
- **Mechanism:** Export a map from abstract witness obligations to target realizations, with a local proof that each realization is reachable, free-transcript compatible, and preserves its claimed failure edges. The realized deployment history is never supplied.
- **Novelty vs nearest prior art:** Predicate abstraction and counterexample-guided abstraction refinement already distinguish real from spurious witnesses. The bet is a reusable realization interface for defeating *teaching alternatives* across different learner parameterizations without local witness search.
- **Cheapest first test:** Change gate coordinates and private outputs in the paper fixture. Compare symbolic witnesses against cached concrete counterexamples and a generic abstract checker; add a shape-compatible but unreachable opposite-lane witness.
- **Old-task retention check:** Check exact A/C margins on target traces, including a reparameterization that preserves nominal A but moves a protected C slice.

#### 04. Invalidate a lower bound by menu difference, not by editor reset (I)
- **Mechanism:** Hash the lawful pair domain separately from the dynamics and retain a coverage proof for unchanged pairs. A public menu edit yields a delta obligation for all newly legal short pairs, never just for the published reply.
- **Novelty vs nearest prior art:** Incremental SAT and assumption-based solving already reuse obligations. This is a test of whether the claimed portability is merely solver incrementality.
- **Cheapest first test:** Add a short decoy that enables an alternate balanced reply and remove an irrelevant specialist in separate imports; time a delta check against a generic incremental solver. An uncovered pair means unknown, not a new search-free optimum.
- **Old-task retention check:** Make the decoy match A and new utility in both variants, but violate C in only one; adjudicate both independently so a changed label is not mistaken for a changed feasible menu.

#### 05. Carry a shorter bound that degrades gracefully (P)
- **Mechanism:** Index obstruction obligations by budget. If some witnesses disappear, report the largest still-certified lower bound `ℓ` and the unchanged upper `k`, not an assertion that the optimum fell to `ℓ`.
- **Novelty vs nearest prior art:** Anytime branch-and-bound already maintains intervals. The bet is a budget-indexed obstruction object that can cross scopes and lose only the affected tiers without re-running search.
- **Cheapest first test:** Construct a family with minimum `3` where removing one witness leaves the certificate for length `<2` intact. Compare interval quality and bytes against an assumption-indexed SAT proof under both removals and admissions.
- **Old-task retention check:** Recheck the length-`3` deployed lesson and its stage-by-stage A/C floors even when the retained interval has widened.

#### 06. Partition short pairs by proofs, not by observed failures (P)
- **Mechanism:** Export checked trace invariants grouping many short pairs into a single failure obligation, with a complete cover of grammar nodes including repeats and the empty sequence. Use separate summaries for each reply class when their effects differ.
- **Novelty vs nearest prior art:** Antichain model checking and IC3 already compress state-space certificates. The added bet is stable proof groups for counterfactual curricula on legal pool expansions, beyond what a generic reachability proof can reuse.
- **Cheapest first test:** Add gate-inert decoys that agree for one update but differ after a repeat. Compare a proof grammar with an antichain verifier and a table; insert the first legal repeat that invalidates a grouping premise.
- **Old-task retention check:** Require componentwise C bounds for each group, including decoys that leave A unchanged but transiently violate C at a live prefix.

#### 07. Compose two lower bounds without assuming their costs add (P)
- **Mechanism:** Assign checked resource demands to two protected skills and prove a bound on how much any single truthful presentation can discharge across both. Only sum lower bounds when the joint discharge proof warrants it.
- **Novelty vs nearest prior art:** Additive pattern databases already require cost partitioning. The bet is an independently checkable exchange rule for teaching obstructions across changing old-task contracts, including cases where one shared example meets both demands.
- **Cheapest first test:** Cross two three-example gated toys, first with disjoint steps, then with one lawful joint step. Compare the composed bound to exact joint enumeration and a generic cost-partitioned planner.
- **Old-task retention check:** Check the original A/C tasks on both skills jointly, including a third shared slice that can be damaged by the combined write despite each local check passing.

#### 08. Put a cap on what any finite obstruction can compress (I)
- **Mechanism:** Use a fooling family in which each short pair requires its own counter-history, then vary structural redundancy without changing the optimum. Separate irreducible history count from compressibility of the proof encoding.
- **Novelty vs nearest prior art:** Teaching dimension and set-cover lower bounds already relate witnesses to distinguishable alternatives. This is the impossibility control for portable minimum certificates, not a new complexity measure.
- **Cheapest first test:** On eight short pairs, plant either singleton failure supports or two broad groups; compare cover size, exact proof bytes and checking work against the cached exhaustive baseline. Reveal no planted partition to the search arm.
- **Old-task retention check:** Plant failures on independent old rare slices and check that the full winner also retains ordinary A/C; don't achieve sparsity by weakening what failure means.

### Carry the next decision without hidden-state recovery

#### 09. Attach a next-reply partition to a shared reply (P)
- **Mechanism:** Ship a reachable-bin certificate and one next action per bin, justified by universal safety after the bundle, shared reply and all declared continuations. Keep multiple plausible momenta in each bin by design.
- **Novelty vs nearest prior art:** Belief planning already supplies the table; FLEX can select an informative reply. The bet is that the certified partition imports across hidden families at lower cost than dynamics-fit excitation plus exact or factored belief re-verification.
- **Cheapest first test:** Use the four-momentum fixture and hold out new magnitudes. Compare with the silent reply, FLEX and causal belief decomposition on the same timing; add both a benign alias with the same required reply and an adversarial alias that needs its opposite.
- **Old-task retention check:** Match first-reply A/C slack and new utility; verify worst A/C over every allowed pulse and next write, including the alias added to the occupied bin.

#### 10. Certify jointly safe bins that pass no state decoder (P)
- **Mechanism:** Encode each history's excluded next replies and certify that their union does not exhaust the menu in each bin. With safe sets `{x,y}`, `{y,z}` and `{x,z}`, pairwise tests pass although the bin is unsafe; a countercertificate records the three-way conflict.
- **Novelty vs nearest prior art:** Minimal conflicts in model-based diagnosis already expose such intersections. The bet is an importable conflict witness checked against an unchanged probe, rather than a fitted predictor of hidden states or pairwise clustering score.
- **Cheapest first test:** Use the three safe sets above in one bin and remove one history to produce a safe bin. Compare a conflict payload, exact belief recheck, and a pairwise action-agreement heuristic at the same read budget.
- **Old-task retention check:** Ground the excluded actions in distinct A/C safety failures and exercise all three histories separately; pairwise accuracy cannot excuse a wrong admission.

#### 11. Keep the action fixed even as the bin geometry moves (P)
- **Mechanism:** Prove that all outcomes in a bounded read/calibration drift map to bins using a common lawful action; merge bins only after checking their combined safe-reply intersection. Permit splitting in the verifier's proof, not extra runtime reads.
- **Novelty vs nearest prior art:** Robust abstract interpretation and approximate bisimulation already reason about uncertain observations. The bet is an importable action-preserving boundary certificate that can be cheaper than recomputing a partition or refitting observation dynamics.
- **Cheapest first test:** Move the fixed probe's quantization boundary across two bins with identical selected replies, then across an opposite-action boundary. Compare a cached policy with ordinary robust re-verification and a boundary-checking import.
- **Old-task retention check:** Hold A/C acquisition margins fixed and verify every allowed sensor rounding outcome; include a rare C lane that makes an apparently interchangeable response unsafe.

#### 12. Certify a smaller observation without decoding the larger one (P)
- **Mechanism:** Specify a coarsening of a fixed probe output and certify that its bins preserve a next action while leaving ambiguity among histories with different private outputs and optimizer variables. Disallow raw readings and metadata at decision time.
- **Novelty vs nearest prior art:** Blackwell comparison and decision-theoretic sensor abstraction already study sufficient signals. The bet is a proof of safe coarsening reusable across imports, priced against a generic belief-policy quotient rather than rewarded for low mutual information alone.
- **Cheapest first test:** Replace magnitude with sign on the paper read; permute histories and private outputs inside sign bins, then add a same-bin opposite action. Compare with a tabular policy built from all probe digits at the same service deadline.
- **Old-task retention check:** Before and after coarsening, verify both specialists on the original A lanes and a C subpopulation whose safety flips with a hidden magnitude in one bin.

#### 13. Share one reply proof across many public next offers (P)
- **Mechanism:** Factor per-bin guarantees into a post-reply envelope and a proof over a public offer parameter, allowing the next reply to depend on that offer if it is revealed on time. Never take a union of actions valid for different hidden histories as a common reply.
- **Novelty vs nearest prior art:** Parametric model checking and factored contingent planning already reuse analyses of related instances. The claim is an offer-relative proof that reuses the same certified lesson and probe partitions without reopening hidden trajectories.
- **Cheapest first test:** Sweep three demand amplitudes with the same sign bins. Put retirement of one specialist exactly at the middle amplitude and reveal it too late in a control arm. Compare with separate cached policies and a factored belief solver.
- **Old-task retention check:** On the held-out amplitude, enforce both A lane floors and an independent C repair cap; late offers may trigger fallback but cannot be routed as if observed.

#### 14. Export a precise last safe use for the partition (I)
- **Mechanism:** Bind validity to public continuation events, not elapsed rounds alone. If an allowed reset can join two opposing obligations in one bin, retract the affected decision even if the first reply is still safe.
- **Novelty vs nearest prior art:** Belief monitoring and the parent node's reveal expiry already cover this mechanism. The stricter audit is whether the action intersection expires before or after hidden-state recoverability does.
- **Cheapest first test:** Insert either a nuisance reset or the parent's `w` reset between the reply and read, then replace the round-count timeout with a public event guard. Compare claim expiry with exact continuation enumeration.
- **Old-task retention check:** Check A/C around the reset and any fallback write, including the case where forgetting nuisance state is harmless and no fallback is needed.

#### 15. Separate the next safe decision from the next winning decision (P)
- **Mechanism:** Strengthen selected bins with a small terminal continuation guarantee: the nominated reply preserves a certified path to a later feasible action, not just the immediate floor. Leave the two-step certificate scoped separately.
- **Novelty vs nearest prior art:** Winning kernels in partial-observation games and receding-horizon safety already represent spare options. The bet is a compact, importable continuation proof keyed by the lesson and the unchanged probe, at a lower cost than a cached winning-policy graph.
- **Cheapest first test:** Extend the paper game by one offer. Put a myopic repair and a reserve-preserving repair in the same bin at equal immediate utility, then vary the legal final offer on import. Compare with the exact three-step belief oracle and an ordinary cached envelope.
- **Old-task retention check:** Match immediate A/C margins across the replies, then check both rare slices and normal old tasks under every allowed final offer.

### Couple the proofs only where reuse pays

#### 16. Reuse a semantic trace proof in opposite directions (P)
- **Mechanism:** Share checked trace identities across the upper proof, shorter-pair failures, and post-reply bin safety. Cache the statement about transitions, not the truth of the final claims, whose quantifiers and scopes differ.
- **Novelty vs nearest prior art:** Proof DAGs and incremental model checking already deduplicate syntax and subproofs. The bet is that a lesson-conditioned transition lemma can be reused after pool or family edits that invalidate a generic instance cache.
- **Cheapest first test:** In both fixtures introduce a public gate-coordinate change preserving transitions under a checked map. Compare proof reuse against a generic shared DAG plus ordinary re-verification; include a single altered continuation where only the bin proof should fail.
- **Old-task retention check:** Bind each reused identity to the actual A/C readouts; a correct transition mapping with a changed old-task head must invalidate dependent safety claims.

#### 17. Prove that any shorter winning policy must buy a split (P)
- **Mechanism:** Give each rival shorter pair a witness to no-split failure and publish a same-demand policy using a priced split that actually restores service. Keep intrinsic infeasibility distinct from a shortage of observation.
- **Novelty vs nearest prior art:** Active diagnosis and contingent planning already calculate value of information. The extra claim is a transportable teaching-budget versus sensing trade-off certified on both sides, not just a lookup of the winning arm.
- **Cheapest first test:** In the paper game compare the taught no-split winner, cached exact probe-only policy, and split with an ambiguous probe; on held-out worlds verify whether the same first-reply obstruction and split feasibility both transfer.
- **Old-task retention check:** Require the same new utility, A/C floors and live deadlines for the taught and paid-split outcomes. A split that merely explains a failure does not count as serving it.

#### 18. Certify next-decision shortestness without claiming first-decision shortestness (P)
- **Mechanism:** For each shorter pair either exhibit a first-reply failure or carry a compatible set of continuations in one reachable probe bin whose safe next replies have empty intersection. Bind the lower proof to the declared two-round objective.
- **Novelty vs nearest prior art:** Bounded synthesis and adversarial game counterstrategies already certify horizon infeasibility. The bet is a compact two-kind obstruction that transfers its lower bound separately from a first-round optimum, at lower cost than a generic counterstrategy cache.
- **Cheapest first test:** Add a singleton that enables a silent shared first reply, then compare its one-round win with a two-example winning route after the fixed read. Freeze first-reply work and enumerate all short pairs; compare transported certificates to exact belief planning plus a generic proof cache.
- **Old-task retention check:** Hold first-round A/C floors and utility fixed and locate the failure in a specific next-round old-task slice rather than penalizing hidden-state ambiguity itself.

#### 19. Revoke each bound on the right dependency (P)
- **Mechanism:** Publish separate validity checks for winner safety, obstruction membership/coverage, and fixed-probe routing, tied together only by explicit dependencies. A failed downstream check need not erase a still-valid upstream bound, but routing cannot use an uncertified installation.
- **Novelty vs nearest prior art:** Assume-guarantee contracts and truth-maintenance systems already support dependency-scoped invalidation. The bet is a CL-specific split that preserves usable decisions under staggered changes without redoing search or recovering state.
- **Cheapest first test:** Change one of pool grammar, A/C interface, hidden envelope, or probe timing per import. Compare correct partial certifications and work to a generic dependency-aware cache, not just full restart. Include simultaneous changes that change the dependency map itself.
- **Old-task retention check:** Independently check every still-served prefix and fallback; a surviving numeric bound must not be treated as permission to apply an uncertified bundle.

#### 20. Make counter-histories useful without disclosing who could realize them (P)
- **Mechanism:** Carry publicly checkable existential proofs of compatible failure traces instead of raw optimizer slots or private examples. Scope the claim to representation hiding; witness count and public predicates can still leak information about the family.
- **Novelty vs nearest prior art:** Zero-knowledge proofs can already hide SAT witnesses. The bet is an interface for reusing the same obstruction under private family extensions with cheaper checking than a fresh proof for every import; privacy alone is not proof of transfer.
- **Cheapest first test:** On a six-history Boolean fixture, compare raw traces, a public abstract reachability proof and an existing proof system for the corresponding existential statement. Price proof generation per family and check that two different realized histories receive the same artifact and route.
- **Old-task retention check:** Verify that the public statement binds the full independent A/C obligations, including rare slices, and that concealing the witness does not permit accepting uncheckable margins.

#### 21. Amortize an obstruction across deadlines, not just repeated editor IDs (I)
- **Mechanism:** Track the cost of looking up and verifying certificates when offers recur, charging unused source proofs, expiry, and ordinary fallbacks. Compare against cache eviction and priced direct sensing, and report the minimum reuse count for equal service if it exists.
- **Novelty vs nearest prior art:** Ski-rental models and proof caches already price buy-versus-rent. This is the accounting test for a dual artifact whose lower and routing proofs might expire at different rates.
- **Cheapest first test:** Enumerate six-offer streams with independently changing scope and hit rate, including adversarial blocks of expired certificates. Compare proof caching, cached exact plans and paid splits, with identical reads and deadlines.
- **Old-task retention check:** Evaluate ordinary A/C tasks and worst slices over the whole stream without resetting the retention anchor after each accepted offer or replay.

#### 22. Compile the bundle away before calling it a primitive (I)
- **Mechanism:** Compare the whole artifact to a frozen plan, an assumption-indexed proof cache and a cached belief policy with shared generic subproofs. Measure the marginal benefit of either proof alone and of their combination on the same held-out stream.
- **Novelty vs nearest prior art:** This is exactly the combination of proof-carrying code, cached exact teaching and factored belief planning; if it compiles away without cost, the proposed object is only packaging.
- **Cheapest first test:** Run a paper factorial (winner only, winner plus obstruction, winner plus partition, both), with the strongest generic stack allowed the same proof sharing. Include an import with less ambiguity, one with more, and one with a same-bin opposite-action alias. Account for checked shortestness separately from safe admission.
- **Old-task retention check:** Match certified service and independent A/C and utility floors at every live prefix; no apparent cost win from quietly omitting either later-task checks or lost service on fallbacks.

## Ranked deeper questions

1. **Can the same frozen artifact prove both bounds on genuinely unseen editor families at lower cost than cached exact search plus re-verification?** Start with #01–#03 and #08: check import containment for the upper bound and legal witness membership for the lower bound, deliberately dropping one obstruction. A two-world calibration fixture is necessary but not sufficient; vary proof reuse beyond identity changes and price failed imports.
2. **What is the smallest reusable evidence for a shared next action when the hidden state remains ambiguous?** Start with #09–#13 and compare with exact belief planning, causal belief decomposition and matched excitation. Require success under benign aliases, failure under an opposite-action alias, and a gain over a no-read policy when routing is claimed to matter. Compare all arms on the same A/C slack.
3. **Can a two-round obstruction reuse first-round proofs without inheriting a false shortestness claim?** Cross #16, #18 and #19: introduce a shorter silent winner, then change only the legal continuation. Demand that the right promises survive and that reuse beats a generic dependency-aware proof cache with the same policy and read budget.
4. **When do both proofs belong in continual memory rather than in a solver log?** Use #17, #21 and #22 to vary frequency, expiry and split prices independently. At matched service and retention, include source search, proof bytes and failures in the break-even. If a generic cache ties, keep the strongest negative result and discard the new primitive label.

**Verdict:** Keep both score-3 directions conditional: ship both bounds only where the winning proof covers the import and enough obstructing histories remain legal there; ship the next-reply proof only where every reachable bin admits a common action. Call the bundle a new primitive only if blind reuse beats the stacked proof-and-policy cache at matched service and old-task retention.
