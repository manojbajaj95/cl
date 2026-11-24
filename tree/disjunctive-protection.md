# Disjunctive protection: keep one working route, not every old channel

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Forbidden update combinations](forbidden-combinations.md) ([PR #154](https://github.com/manojbajaj95/cl/pull/154)), especially cards 1 and 18. **Review seed:** [flood-triage row 247](https://github.com/manojbajaj95/cl/blob/c253f20d197ab840812729602ca0ca7811c7267a/reviews/flood-triage.md#L247), score 3: choose the cheapest set of live backups to preserve at each step, and spend replay where only one backup is left. The reviewer made the real-host census and break-even against GPM required gates, not positive results.

## What would be new?

For an old input on which both channels of `y = OR(a,b)` work, the conservative rule is **leave a alone OR leave b alone**. In the binary erasure toy its exact safe set is the two coordinate axes in update space. Both axes together span the plane. A single GPM/OGD subspace can keep one safe branch or a subset of it, or admit both axes and with them unsafe updates; it cannot admit exactly the union. For a smooth OR, `1 − (1 − s_a)(1 − s_b)`, both first derivatives vanish at `(1,1)`, while a joint decrease reduces the output by the product of the decreases. A local Fisher/EWC score and intact-singleton ablation can therefore see neither backup; even a general positive-semidefinite quadratic cannot have the union of two axes as its zero set. This is a representational separation, not a claim that tuned quadratic penalties always lose at a nonzero tolerance. On inputs with just one live channel the rule reduces to a singleton and must protect it. In a real network a route can also fail through its gate, shared trunk, normalization, or downstream consumer even if its named channel is unchanged.

**Candidate object: a registry of live sufficiency certificates.** For each protected input slice, store alternative *sets* of groups that suffice for the old decision on that slice, a reference and tolerance for each set, and the consumer/routing assumptions. The next realized state must satisfy at least one complete certificate per slice; across slices/tasks these requirements are conjoined. A lost route doesn't become live simply because the current step leaves it alone: its original reference must still hold or a replacement must be independently validated. Unknown coverage or invalidated assumptions are abstentions, not certificates. The same registry can expose the last independent route for replay even when current old loss is flat. Replay on saturated old labels alone may still have zero gradient: test whether masked survivor replay adds anything beyond simply prioritizing inputs, and charge its extra forwards.

**Cheapest live-backup set.** For disjoint orthogonal coordinate groups, a proposed optimizer step `u` and a mask that zeroes protected groups, the Euclidean projection toll for keeping groups `H` is `Σ_{g∈H} ||u_g||²`. With singleton alternatives this is weighted hitting set (equivalently weighted vertex cover for pair clauses); with multi-group alternatives, choose `H` containing one full certificate per slice. Pay for shared groups once. This formula does not extend to overlapping/nonorthogonal groups or adaptive-state effects: measure the cost of the actual projected step and check the post-step state, including any permitted optimizer or consumer changes. Across many tasks the union can have exponentially many branches; even finding the cheapest mask for arbitrary pair clauses subsumes minimum vertex cover. Report tractable structure and abstention costs, not an all-host scaling guarantee.

## Prior-art screen and common CPU controls

- **Geometry and optimization:** [EWC](https://arxiv.org/abs/1612.00796), [OGD](https://arxiv.org/abs/1910.07104), [GPM](https://arxiv.org/abs/2103.09762), [Adam-NSCL](https://arxiv.org/abs/2103.07113), [TRGP](https://arxiv.org/abs/2202.02931), [SGP](https://arxiv.org/abs/2302.01386) and [SPACE-LoRA](https://arxiv.org/abs/2609.34453) are importance/subspace or selective-protection controls, not evidence that every implementation uses a single fixed projector. [Pathway Protection](https://proceedings.mlr.press/v267/chen25bt.html) and [PackNet](https://arxiv.org/abs/1711.05769) are route and mask controls. [Optimal CL](https://arxiv.org/abs/2006.05188) already treats CL as intersecting feasible sets, [CABA](https://arxiv.org/abs/2610.40740) provides a behavioral certification control, and [PR #152](https://github.com/manojbajaj95/cl/pull/152) studies finite safe regions. Disjunctive programming, reliability cut sets and hitting set are not new. Neither is preserving a last complete carrier: [recovery witnesses, PR #139 card 13](https://github.com/manojbajaj95/cl/pull/139) already proposes it for recoverability, including optimizer slots. The narrower bet here is *continuously served* old behavior, with one stateful object for step selection and pre-failure replay that beats those ingredients and their combination.
- **Finding and using backups:** [Hydra](https://arxiv.org/abs/2307.15771), [Conditional Co-Ablation](https://arxiv.org/abs/2607.01940) and [backup/counterweight analysis](https://arxiv.org/abs/2610.02173) motivate measuring replacements, not assuming independent or deployable routes. [Dropout](https://jmlr.org/papers/v15/srivastava14a.html) and pruning robustness are controls for generic redundancy. [MIR](https://arxiv.org/abs/1908.04742) selects by predicted loss increase, [GSS](https://arxiv.org/abs/1903.08671) by gradient diversity; both must be tested, not presumed blind, especially on prospective writes that already break the last route. This is a targeted literature screen, not a priority claim.
- **Ledger:** The [idea ledger](https://github.com/manojbajaj95/cl/blob/c253f20d197ab840812729602ca0ca7811c7267a/reviews/idea-ledger.md) requires retention, equal-budget simple controls, and a real interaction for a merge. Don't revive sparse-damage syndromes: write damage may be dense. Don't confuse larger initial margin with redundancy: margin-match the census and forecasts. Don't count a planted OR as evidence of prevalence, or a frozen producer as protection if its consumer can move. Labels below are hypotheses: **P** = candidate primitive (a reusable object or operation if the separation holds), **I** = improvement, audit, or known tool transferred. These are proposed screens, not pilot commitments.
- **Shared protocol:** Start with enumerable fallback, vote, and nonredundant series circuits, then unmodified, small CPU-trained MLPs on split digits and, only as a spot check, a frozen CPU GPT-2-small with candidate head/MLP interventions. A denotes ordinary old test data held out from discovery and replay, plus a separately reported single-support or route-specific panel; B is the new stream, and C is an untouched control skill. Use held-out B suffixes and match *attained* B loss or accuracy (report no common point if needed). Report A/C before B, after each committed step in the small tests, worst prefix, first break, and worst old task; keep ordinary inputs separate from ablation stress tests. Compare exact oracle, static cheapest cover, tuned subspace/regularization controls, and uniform/MIR/GSS replay at equal memory and compute; include projection plus the strongest plain replay and survivor replay without projection. Count queries/forwards, registry and replay bytes, vetoes, time, and false-safe admissions, including discovery and validation. Don't give the oracle credit as a deployable method.

## Idea cards

### The object and the optimizer

#### 1. Nearest live branch (I)
- **Mechanism:** Enumerate the live branches, project the proposed B step onto the least-cost one, and validate the realized endpoint before commit. Track custody against the original reference as B's pressure rotates.
- **Novelty vs nearest prior art:** Parent card 1 and PR #139 already supply the rule; this is the oracle for its incremental value over static masks, GPM, TRGP, SGP and EWC, not a new optimizer family claim.
- **Cheapest first test:** Two-coordinate erasure and repair, alternating B demand, and one 2-of-3 vote. Compare an exact oracle, fixed cover and per-step cheapest cover at matched attained B.
- **Old-task retention check:** Exhaust ordinary A and its singleton-support slices after every step; log false hand-offs and C.

#### 2. Atomic make-before-break certificates (P)
- **Mechanism:** Allow a transaction that creates a newly validated route before relinquishing the current route. Keep a journal of which intermediate states can be exposed; require the old certificate until a replacement is demonstrably serving.
- **Novelty vs nearest prior art:** Parent custody hand-offs and PR #152's mergeable writes cover verified switching and order in general; the candidate operation is minting a route during the write with an independently checked activation condition, not just selecting an existing route.
- **Cheapest first test:** A three-gate circuit with a two-step route creation and forced interleavings. Compare atomic endpoint repair, parent-style switching among available routes, and per-prefix replay at equal checks.
- **Old-task retention check:** Query held-out A and C at every exposed prefix, including aborted writes and a slice on which the new route's gate never opens.

#### 3. Same subspace, different write rights (I)
- **Mechanism:** Match two models' old margins and stored activation-subspace projectors, then change only the redundancy topology from parallel to series. Present the same finite B candidates to both.
- **Novelty vs nearest prior art:** Stronger controlled separation than the parent's geometry illustration; identifies when GPM/SPACE-LoRA summaries or a simple margin control suffice despite the toy proof.
- **Cheapest first test:** Enumerate binary gates with parallel versus series consumers, identical starting activations, and equal forward margins. Compare admissions against an exhaustive A-output oracle and CABA-style endpoint validation.
- **Old-task retention check:** Execute candidate sequences and check ordinary A/C at each prefix, not just which single moves the rules classify correctly.

#### 4. Spendable route slack, not resettable proximity (P)
- **Mechanism:** Give each alternative a remaining reference-relative tolerance; carry it over across steps and credit a restoration only when the signed effect is verified. Spend from another branch rather than silently resetting the reference.
- **Novelty vs nearest prior art:** [Stored slack, PR #151](https://github.com/manojbajaj95/cl/pull/151) budgets consumer slack; the proposed extra operation is branch-indexed spends and refunds when the safe set is disconnected or nonconvex.
- **Cheapest first test:** Repeated subthreshold same-sign writes versus true cancellations on a smooth OR, compared with per-step recentering, static radii and direct endpoint checks.
- **Old-task retention check:** Test unchanged A/C after every micro-write and when one final route crosses its cumulative tolerance.

#### 5. Optimizer-state lease (P)
- **Mechanism:** Issue a short lease for a route only if the projected current write *and* a declared set of slot-induced follow-on writes preserve it; alternatively freeze the relevant slot update until hand-off.
- **Novelty vs nearest prior art:** Adam-NSCL and PR #139 already address optimizer state. The candidate distinction is a time-limited certificate for *live service* under a declared optimizer continuation, not recovering A later.
- **Cheapest first test:** Two scalar paths under momentum with identical visible weights and opposing stored velocities. Compare weight-only projection and full slot freezing at equal B progress.
- **Old-task retention check:** Evaluate A/C through the first unprojected follow-on step and through a custody switch; a guarantee ends at lease expiry.

#### 6. Future-flexibility exchange rate (P)
- **Mechanism:** Price branches by how many cheap B continuations they leave feasible, not just the immediate projection toll. Prefer a slightly dearer branch if it avoids stranding every other cheap path later.
- **Novelty vs nearest prior art:** The parent's cheapest cover is myopic; the ledger's forecast-weighted readiness failed against readiness alone. The candidate quantity is the future feasible-write frontier at equal immediate cost and equal current A.
- **Cheapest first test:** Exact depth-two enumeration where ties today have different legal suffixes. Compare myopic and static covers, a count-only forecast, and equal-lookahead endpoint rejection.
- **Old-task retention check:** Check A/C on unseen B suffixes and report worst prefix, not just the projected future score.

### Is usable redundancy common?

#### 7. Denominator-first redundancy census (I)
- **Mechanism:** Predeclare old slices, layers, eligible group types, intervention budgets, and B writer families. Track the funnel from jointly necessary combinations to individually sufficient, live, writer-reachable alternatives, to cases where the cheaper safe branch improves B.
- **Novelty vs nearest prior art:** Hydra and CoAx establish examples; the parent's census is a required audit. Report prevalence on the declared denominator rather than a collection of dramatic co-ablations.
- **Cheapest first test:** Two ordinary CPU MLP architectures on split digits, seeds and slices selected before ablations. Use effect-matched random groups, margin/width matching, and count unidentified cases separately with uncertainty by seed/task.
- **Old-task retention check:** Run held-out B writes on census-positive and census-negative slices; measure A/C throughout, including uncatalogued ordinary inputs.

#### 8. Ablation-to-write transfer (I)
- **Mechanism:** Infer candidate alternate routes using conditional ablation, then test the signed finite perturbations that the actual B optimizer produces. Reject backups that exist only for zeroing or mean ablation.
- **Novelty vs nearest prior art:** CoAx discovers conditional importance, not transfer across intervention families. Parent writer-relative clauses motivate the strong comparator: direct B-write screening at equal queries.
- **Cheapest first test:** Compare zero/mean masking, signed steps and projected reachable B steps on a CPU split-digits MLP; report precision and coverage for safe-update predictions.
- **Old-task retention check:** Audit every false-safe write on A, and ensure selection by one intervention type doesn't damage C under a different type.

#### 9. Route identity after a change of basis (P)
- **Mechanism:** Represent a route by its input-conditioned effect and consumer rather than its neuron index; transport that functional certificate through a known invertible hidden-basis reparameterization and abstain when a proposed writer makes it untrackable.
- **Novelty vs nearest prior art:** PR #152 transports safe regions and the parent suggests learned-subspace clauses. The candidate unit of transport here is *alternative identity*, preserving the last-route count under reparameterization without full rediscovery.
- **Cheapest first test:** Exact rotation of a linear bottleneck in a small MLP; compare transported effects, named units, GPM and full rediscovery under rotated and unrotated writer maps.
- **Old-task retention check:** Check A/C invariance before training and preservation afterwards, including deliberately non-equivalent transforms on which transport must abstain.

#### 10. Failure-domain census (I)
- **Mechanism:** Use observed write effects to cluster routes that fail together and contract their shared bottlenecks. Count independent survival opportunities under a declared writer rather than counting individually sufficient masks.
- **Novelty vs nearest prior art:** Known common-cause reliability and parent card 20; ties the failure domain to writer effects rather than output similarity. Compare with [slack-based backup independence, row 244](https://github.com/manojbajaj95/cl/blob/c253f20d197ab840812729602ca0ca7811c7267a/reviews/flood-triage.md#L244).
- **Cheapest first test:** Two parallel heads with either separate trunks or one shared gate; vary only B's ability to edit that gate, with matched A margin and head count.
- **Old-task retention check:** Replay held-out B writes that hit the common gate; score worst-prefix A/C and any false declaration of independent backups.

#### 11. Direct-service versus recovery witness (P)
- **Mechanism:** Classify apparently redundant routes as serving immediately, serving after input-dependent rerouting, or serving only after a weight/slot continuation. Only the first two may qualify for a live guarantee and rerouting must finish inside the serving budget.
- **Novelty vs nearest prior art:** Hydra self-repair and PR #139's recovery witnesses already provide mechanisms for rerouting or recovery. The proposed operation is an explicit conversion test from recoverability to a serving-time certificate, not relabeling buried skills as live.
- **Cheapest first test:** Equip a tiny gated MLP with a dormant route requiring one extra optimization step and one requiring only a forward gate. Compare restoration after one update with live admission on identical B sequences.
- **Old-task retention check:** Score A/C before intervention, after the next B commit without recovery, and after waking; report the results separately.

### Replay on the last live route

#### 12. Last-route replay trigger (I)
- **Mechanism:** Retrieve old examples whose slice is down to one certified live alternative, prioritizing exposure to the proposed B write. First use ordinary supervised replay so selection is the only change.
- **Novelty vs nearest prior art:** Implements parent card 18, not a new replay family; MIR can already detect a predicted breach and GSS can favor diverse gradients. The relevant comparison is one step *before* such a breach at matched margin and B pressure.
- **Cheapest first test:** Pair intact and eroded-but-correct A slices with equal current loss, comparing uniform, MIR and GSS at equal bytes/forwards on alternating B writes.
- **Old-task retention check:** Measure ordinary A, singleton slices, and C (including high-redundancy slices starved by the trigger), at matched attained B.

#### 13. Survivor-conditioned target (I)
- **Mechanism:** On last-route items, replay an acquisition target with other candidate routes masked, so a survivor must retain its conditional margin; use ordinary targets on a separate sentinel panel.
- **Novelty vs nearest prior art:** Conditional co-ablation plus distillation is not itself a primitive; the claim is that a route-conditioned target outperforms the combination of plain replay and route-based selection when ordinary old gradients are flat.
- **Cheapest first test:** Compare selector × target in a 2×2 CPU test, charging masked forwards; add a random-mask distillation arm to control regularization.
- **Old-task retention check:** Evaluate ordinary A/C without masks, and report conditional margins separately so success on artificial inputs cannot hide regression.

#### 14. Route-to-zero hazard (I)
- **Mechanism:** Forecast which currently correct slices will lose the last live route within a fixed horizon, using certified change history and proposed writer exposure, rather than using route count alone.
- **Novelty vs nearest prior art:** [Slack erosion, PR #153](https://github.com/manojbajaj95/cl/pull/153), MIR and forgetting-event history are strong controls. Any added value must survive current and historical margin matching, not just correlate with tiny margins.
- **Cheapest first test:** Fit simple hazards on early B streams and rank next-break risk on held-out suffixes; compare margin history, prospective MIR, constant hazard and raw backup count with identical observations.
- **Old-task retention check:** Spend identical replay budgets by each ranking and check A/C worst prefix at matched B; prediction lift alone doesn't count.

#### 15. Replay that buys a second route (I)
- **Mechanism:** When ordinary old probes are correct but a slice is at one live route, spend replay to reinstate an independent alternative; keep the survivor until the replacement passes a conditional audit.
- **Novelty vs nearest prior art:** Parent card 22 already proposes re-replication. The incremental question is whether targeted replay buys actual independent capacity rather than a larger margin on the same one.
- **Cheapest first test:** A tiny two-trunk MLP; compare survivor strengthening, random re-replication and targeted repair at identical extra parameters and old samples, followed by a held-out write at the original survivor.
- **Old-task retention check:** Verify A/C while the second route is installed and after either route is lost; keep ordinary unmasked tests separate.

#### 16. Cross-task replay coverage (P)
- **Mechanism:** Treat a vulnerable route plus consumer/slice as a replay obligation. Select a batch covering several obligations only where a sample's replay update measurably supports each, and reserve coverage for isolated obligations.
- **Novelty vs nearest prior art:** MIR/GSS and set cover already select useful diverse examples. The candidate object is a replay-to-survival incidence matrix measured by realized masked retests, not example similarity or average loss.
- **Cheapest first test:** Four tasks share one trunk and have mixed heads; compare exact coverage, task-balanced MIR/GSS, and coverage predicted from gradient similarity with equal probes and replay steps.
- **Old-task retention check:** Check each task's worst prefix including the task with a private route, and untouched C; aggregate retention cannot erase a starved task.

### Scaling the conjunction across tasks

#### 17. A treewidth budget for exact choice (I)
- **Mechanism:** Factor the task–route graph over shared groups; solve min-cost choices by dynamic programming when separator width is small and charge the cost of maintaining the decomposition as new tasks arrive.
- **Novelty vs nearest prior art:** Standard graphical-model optimization, not new CL math; tests whether reusable modules give the graph structure needed to beat generic hitting-set solvers.
- **Cheapest first test:** Stream equal-degree chains, trees and expander-like clause graphs; compare exact enumeration on small cases, integer programming and greedy/static masks as task count grows.
- **Old-task retention check:** Run admitted Boolean-host B writes and check every earlier A and C after each commit; timeouts cannot silently relax the rule.

#### 18. A cheap certificate when the solver times out (P)
- **Mechanism:** Maintain an incumbent valid cover and a lower bound on projection toll. On deadline, serve the incumbent or abstain when it can't be revalidated; carry the bound into a decision about whether more search is worth it.
- **Novelty vs nearest prior art:** Branch and bound and approximation certificates are standard. The candidate interface couples a bounded plasticity loss to an independently checkable *old-service* witness, rather than allowing approximate feasibility.
- **Cheapest first test:** Online weighted vertex-cover instances with random timeouts plus dropped routes; compare anytime greedy repair, frozen incumbent and complete solve at equal deadline.
- **Old-task retention check:** Execute fallback writes and verify old tasks/C after timeouts and route deletions, including cases with no feasible current certificate.

#### 19. Lossless clause compaction with receipts (I)
- **Mechanism:** Remove a task obligation from the active solver only with an implication proof from retained obligations under the declared writer. Keep enough provenance to reverse compaction when writer or domains change.
- **Novelty vs nearest prior art:** SAT subsumption and PR #152's implication-proof deletion are direct precedents. Here the question is which task-arrival overlaps actually repay proof and revalidation costs.
- **Cheapest first test:** Nested vs overlapping slice obligations in a stream of Boolean hosts; compare exact subsumption, unconditional deduplication, and no compaction at equal memory.
- **Old-task retention check:** Re-evaluate every compacted task and C after a writer change; no credit for correct behavior only on retained slices.

#### 20. The price of protecting one more task (P)
- **Mechanism:** Extract small conflict cores from a set of old obligations plus a required B progress threshold; distinguish a genuine joint bottleneck from simple solver timeout or a poor named-group basis.
- **Novelty vs nearest prior art:** [PR #150](https://github.com/manojbajaj95/cl/pull/150) and PR #152 already cover impossibility witnesses and conflict cores. The candidate diagnostic attributes the lost plasticity to *combinations* of otherwise cheap route-choice obligations and suggests which obligation needs a new alternative.
- **Cheapest first test:** Construct streams where every old task is cheap alone but accumulating them removes all B moves at the threshold. Compare per-task prices, direct finite-region cores and exact enumeration.
- **Old-task retention check:** Give only a core member a certified extra route; check every old task and C during retraining, and test whether the B frontier recovers without dropping a task.

#### 21. Lease budgets for shared backup bottlenecks (P)
- **Mechanism:** Reserve some independent live routes for tasks whose alternatives are about to disappear from the feasible cover. Release reservations as branches are restored; charge joint reservations for a common failure domain once, not once per task.
- **Novelty vs nearest prior art:** Escrow/reliability and PR #151's slack budgets are direct analogues; the proposed policy reasons about future contention among alternative certifying sets rather than splitting a scalar reserve across consumers.
- **Cheapest first test:** Burst B streams in which myopic covers converge on one vulnerable trunk. Compare min-cost cover, reserve-by-count, and exact online/lookahead oracles with the same live channels.
- **Old-task retention check:** Track worst-task A/C through a shared-trunk write and the reservation hand-off; fixed reservation cannot get a free pass by preventing all B learning.

#### 22. Merge replicas without losing the last global route (P)
- **Mechanism:** Compose route certificates from two separately trained B branches as a condition on the combined realized write, rejecting merges that destroy every live route although each branch kept a different one.
- **Novelty vs nearest prior art:** PR #152 already asks for mergeable writes, and the ledger rejects coded pairwise surrogates. The candidate operation is a compact, provenance-bearing witness for the *same surviving route* across branches, including shared consumers, not a learned pairwise risk score.
- **Cheapest first test:** Enumerate paired branch writes on a three-route host, then introduce a shared gate; compare direct merged endpoint validation, projected replay and conservative mask union at equal old probes.
- **Old-task retention check:** Check A/C after each branch and committed merge on a held-out panel, including a control merge where both branches protect the same route but jointly shift its consumer.

## Ranked deeper questions

1. **Is OR-structured protection a distinct, useful CL object, or just finite feasibility with a combinatorial encoding?** Start with the oracle live-branch frontier. Compare against tuned GPM/TRGP/SGP and EWC, static/PR #139-style protection, direct CABA-style endpoint checks, and the strongest matched replay stack. Require a gain in worst-prefix A at matched attained B with no C loss; if the oracle ties on reachable redundant hosts, stop. If direct checks tie after total costs, the registry is an explanation, not a new primitive.
2. **How common are independently live alternatives in real learned networks, under actual write pressure?** On predeclared slices and writer families, distinguish dormant recoverability, common-mode backups, and true single-route sufficiency. Measure coverage, uncertainty, and the fraction with cheaper safe writes; if the gain only survives planted axes or selected IOI examples, don't generalize.
3. **How does the conjunction scale across many old tasks?** Measure graph width, repeated clauses, worst-task service, abstentions, bytes and solver cost as overlap rises. Does compaction or bounded-width solving keep the break-even point ahead of tuned SPACE-LoRA/GPM and replay, or do obligations converge to a union mask?
4. **Does last-route replay act before conventional selectors, and can it help without a new target?** Factor selector, masking target and projection in the same test, at matched A margin, old bytes and total compute. If projection plus plain MIR or random-mask distillation explains the whole gain, don't claim a joint protection–replay mechanism.
5. **Can certificates survive shifts in the writer, consumer, or serving distribution?** Compare transport and make-before-break against fresh validation. If dynamic revalidation costs as much as checking ordinary old inputs or creates false-safe writes, limit the claim to fixed writer/consumer regimes.
