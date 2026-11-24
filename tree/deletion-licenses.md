# Deletion licenses: survive a price change, buy back only what matters

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Stopping proofs](stopping-proofs.md) ([PR #182](https://github.com/manojbajaj95/cl/pull/182)), cards 03 and 08. **Review seeds:** [Flood triage row 288](https://github.com/manojbajaj95/cl/blob/b3c4afed4dfd9e0b0085ce4cfa10594f6f4df038/reviews/flood-triage.md#L288). **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/b3c4afed4dfd9e0b0085ce4cfa10594f6f4df038/reviews/idea-ledger.md). The two seeds are starting points, not new contributions: compile stopping regret over prices, and reacquire just the frontier needed when scope breaks.

## What would make this a continual-learning primitive?

**Not computing a region or collecting a counterexample.** Parametric optimization already computes critical regions; [decision-focused learning](https://arxiv.org/abs/1809.05504) prices decision error; [counterexample-guided abstraction refinement](https://doi.org/10.1007/10722167_15) already localizes insufficient abstractions. The candidate is a **portable deletion license with a recovery interface**: a blind editor reuses a checked regret guarantee without access to erased evidence, or finds exactly what claim would need new lawful evidence. A failed scope check suspends reliance; it is not itself an example, proof of an unsafe model, or proof that the cheapest repair has changed.

### The price check and the scope check are different

- Freeze the edit payload, new-task utility, hard A/C obligations at every served prefix, scope of learner/optimizer/sampler states, legal observations and interventions, and the served horizon. A repricing changes only tariffs, not coverage, latency, availability, verification or utility unless separately checked. No price pays for a failed old task. Retain a checked refusal/fallback path; price lost new-task utility and report refusals separately.
- Let `X` be all admissible histories consistent with retained evidence, `a` a separately verified incumbent, and `C(π,x;p) = d(π,x) + p·u(π,x)` with quantities for acquisition and repair (including checks, fitting and repeat charges where relevant). Fix the comparator: for the price experiment use the cheapest lawful, timely decision policy with access to the otherwise deleted information at its declared acquisition price, including the incumbent. If recovering information can affect training, include those transitions too. For a stronger, free-information comparator, do not charge to reveal its free information; a tariff on that reveal cannot tighten that bound.
- For a finite model with fixed legality, use one half-space `C(a,x;p) − C(π,x;p) ≤ ε` per admitted history and comparator policy evaluated there. Their intersection inside a declared price domain is the exact region for this pointwise regret criterion **if** the costs are exact and all policies are represented. A relaxation may substitute independently certified lower bounds on comparator cost; retain only a proved inner region. Sampled prices, omitted competitors and a few locally tight facets are not evidence of coverage. Keep the proof and its declared inputs, not the original answer logs, repair tables or checkpoints (including hidden verifier access). An out-of-region price need not make the incumbent unsafe: it ends the regret claim, not its independent safety proof.

### What a recoverable frontier has to resolve

Let `H` be the histories still compatible with the retained state and new job. A frontier is a lawful observation **or adaptive bundle** with declared cost, source version and delivery guarantees. For **every** possible answer transcript, the residual set of histories must support a fresh, independently checked disposition (admit a repair or take the predeclared safe fallback). On admitted branches, require both hard A/C guarantees and the declared regret bound. To call the frontier useful, it must improve the declared admission/cost objective over going directly to fallback; otherwise a constant answer and universal refusal would qualify. Optimize total work or worst-case work explicitly; not every inclusion-minimal bundle is cheapest.

An ambiguity witness is two live histories compatible with the same retained evidence but requiring incompatible dispositions to meet the chosen contract. It explains why the proposed *common* disposition cannot work; for more than two repair choices, a minimal obstruction can require three or more histories. A real failing trace can seed the search, but proving it is separated is not enough: recheck coverage of the answer cells and every served prefix. If no useful lawful frontier can be certified in time, refuse the unsupported edit (or use a separately checked fallback); distinguish a proof of impossibility from an exhausted search. Do not rebuild from forbidden backups.

**Paper case.** Use one acquisition tariff `q`, one repair tariff `r`, a separately safe incumbent costing `4r`, and a checked probe-and-specialize policy costing `q+r` in every admissible history. With no other cheaper legal policies, regret is `max(0, 3r−q)`; a one-unit license passes at `(q,r)=(2.1,1)` and not at `(1.9,1)`. A cheap specialist that fails C in one history is not a lawful common competitor. Now add a new editor whose optimizer couples two deleted bits so the required specialist is keyed by parity, with every bit pair still possible. Neither bit alone resolves it. A current lawful parity check, or both current bit checks with a proof of the coupling, would be sufficient if their replies can be checked and applied in time. If only one bit is lawful and there is no common verified reply meeting the frozen offer, refuse; don't take an old bit value from a checkpoint. This case distinguishes a price miss, a structural miss, and a genuinely unavailable recovery.

### Controls and verdict

Give all arms the same frozen jobs, sources, fallback, deadlines, witness repertoire, independent verifier and memory cap. Compare exact parametric sensitivity plus a checked byte-matched cache; decision-focused optimization with the same training data; full lawful replanning; one-block reacquisition; optimal counterexample-guided recovery with the same source availability; and the strongest stack of those parts. Use exhaustive finite truth to score, not as a hidden deployed input. Check one in-region and one just-outside price, a pure scope shift at fixed prices, and a mixed shift; do not tune thresholds on blind editors. Count retained and peak bytes including proof dependencies, preparation and checking, source work, delay, repairs, utility, false approvals and refused feasible jobs. Evaluate independent ordinary A/C, including rare slices, before deletion and at every served prefix. Report admitted utility separately from safety.

**Conditional verdict:** Keep the primitive claim only if the same artifact saves total evidence or work at matched utility and retention under blind repricing **and** lawful recovery, versus the combined baseline. A cache hit, a cheaper sensitivity solver, or a refusal-heavy policy is not enough. A sound but expensive license is a negative result. **P** = conditional new reusable object or operation; **I** = improvement or audit, not a pilot recommendation. All tests below are paper or tiny CPU proposals, not results.

## Idea cards

### Price certificates without the source tables

#### 01. A held-out editor gets the facets, not the repair table (P; parent 03)
- **Mechanism:** Compile a regret region with a proof of coverage, and make a new editor supply just its tariff vector and independent scope evidence. Ship no source-table handle.
- **Novelty vs nearest prior art:** [Decision-focused learning](https://arxiv.org/abs/1809.05504) optimizes decisions under costs; exact parametric analysis plus a byte-matched cache is the real rival. The candidate is a portable authorization to rely on deletion.
- **Cheapest first test:** Enumerate three repair cost planes and one joint probe. Test an in-region price and a nearby crossing with the original table disabled; charge bytes for every proof dependency.
- **Old-task retention check:** Include a newly cheaper specialist that breaks C. Verify old A/C independently after the accepted price change and after fallback at the crossing.

#### 02. Certify a safe menu rather than yesterday's winner (P)
- **Mechanism:** Ship a few independently verified incumbents and a region with a selector whose every certified cell points to one of them. The blind editor can switch within the union without opening the deleted table.
- **Novelty vs nearest prior art:** [Multi-objective sequential decision making](https://arxiv.org/abs/1402.0590) already uses coverage sets; the candidate is a partial, checkable menu that remains usable after deletion and rejects an uncovered gap.
- **Cheapest first test:** Three competing affine policies with two exported witnesses; compare with the exact minimum regret over verified incumbents and a byte-matched policy cache. Place one offer outside both exported regions.
- **Old-task retention check:** Verify A/C through the witness switch, not just the two endpoints; plant an incumbent that would be safe from a reset but not from the live state.

#### 03. Pay to learn the tariff only near a proved boundary (I)
- **Mechanism:** Accept an interval quote if it lies entirely inside the license. If it straddles, compare the cost and deadline of refining the quote with the verified fallback; never use a midpoint for acceptance.
- **Novelty vs nearest prior art:** [Bayesian optimization with unknown constraints](https://arxiv.org/abs/1403.5607) prices information under uncertainty; robust sensitivity already checks whole intervals. This is an audit of tariff uncertainty, not a new value-of-information rule.
- **Cheapest first test:** Three interval quotes under the paper-case region: wholly in, straddling, and wholly out. Compare exact sequential quote acquisition at equal information costs.
- **Old-task retention check:** Check ordinary A/C throughout the waiting interval and after fallback when a decisive quote misses its deadline.

#### 04. Reprice in the editor's units without importing its budget (I)
- **Mechanism:** Bind quantities and units to the certificate, and check a conversion from local tariffs to those units including any fixed fees or nonlinear tariff tiers. Reject a conversion that silently changes the cost model.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) checks interface contracts and refinements. This is a portability audit; a unit conversion by itself is not a CL operation.
- **Cheapest first test:** Normalize two equivalent quotes, then send a third with the same per-unit rates but an extra minimum call fee that moves the boundary. Compare ordinary exact recosting.
- **Old-task retention check:** Use the same A/C suites in both units and a fit-cheap but C-unsafe option that must remain excluded under every conversion.

#### 05. Prove a facet has disappeared without relearning its hidden bit (P)
- **Mechanism:** Export which verified update would deactivate a binding regret constraint. When a later edit installs that update, require proof that the old competitor can no longer beat the incumbent under every compatible history; then widen the region without restoring the bit.
- **Novelty vs nearest prior art:** [Trajectory matching](https://arxiv.org/abs/2203.11932) teaches useful updates and parametric redundancy removes implied facets. The candidate is a witnessed state change that widens a deletion right, not just eliminating a redundant inequality.
- **Cheapest first test:** In a two-world gate model, compare teaching to remove the constraint, ordinary exact recompilation, and #182's common-reply witness with no price certificate. Include a matched-utility sham update.
- **Old-task retention check:** Protect A and a C capability that shares the gate. Reject the sham that makes the competitor disappear by removing that capability.

#### 06. Transfer only the proof clauses whose scope a new editor preserves (P)
- **Mechanism:** Annotate cost-bound clauses with verified semantic dependencies. Under a structural edit, keep only clauses with proved unchanged semantics and discharge the remaining obligations before issuing a new region, including completeness of any new cheap paths.
- **Novelty vs nearest prior art:** Incremental SAT and [Pacti](https://arxiv.org/abs/2303.17751) reuse reasoning under changed assumptions. The test is whether residual obligations can be checked without the original erased evidence.
- **Cheapest first test:** Change one block of a three-block learner. Compare incremental proof checking, full sensitivity recompilation, and a false dependency map omitting a shared optimizer slot.
- **Old-task retention check:** Run unaffected A plus C from the affected and nominally unaffected blocks; verify that clauses retained from the old proof never substitute for prefix safety.

#### 07. Safe for every quote, payable only if solvent (I)
- **Mechanism:** Keep the regret threshold and an absolute resource cap as separate predicates. A tariff change can preserve regret while making all usable policies unaffordable; check both before any commitment.
- **Novelty vs nearest prior art:** [Constrained policy optimization](https://arxiv.org/abs/1705.10528) already separates return and constraints. This is an orthogonality audit for portable licenses, not a new constrained optimizer.
- **Cheapest first test:** Enumerate a two-tariff case with both policies equally expensive after a fixed fee. Compare a regret-only region and exact joint feasibility.
- **Old-task retention check:** Maintain A/C on the solvency-triggered refusal path; disallow a cheap unverified shortcut that would avoid refusal.

### Recovery after the old evidence is gone

#### 08. Buy a frontier, not the disappeared table (P; parent 08)
- **Mechanism:** Reopen only the part of the proof invalidated by a new optimizer-mediated interaction. Accept a frontier only with covered answer cells and timely checked replies, otherwise fail closed.
- **Novelty vs nearest prior art:** [Counterexample-guided repair](https://arxiv.org/abs/2301.11342) already targets counterexamples. Here the observer must recover from actual deletion with no privileged access to the previous evidence.
- **Cheapest first test:** Use the parity paper case and test parity-only, independent full/one-block rebuild, and optimal counterexample-guided repair with identical source availability. Remove parity and then one of the bit sources.
- **Old-task retention check:** Check ordinary A/C at the attempted edit, during waiting, and on the C-sensitive parity branch after repair; verify the no-frontier refusal.

#### 09. Find the obstruction that cannot be expressed as a pair (P)
- **Mechanism:** Carry a separation proof for the smallest group of histories with no common low-regret reply. Search observations that break the group, but require a fresh proof for every resulting cell; no pairwise-completeness assumption.
- **Novelty vs nearest prior art:** Minimal unsatisfiable cores and [counterexample-guided repair](https://arxiv.org/abs/2301.11342) already use failures to constrain search. The candidate is a portable obstruction interface for buying lawful distinctions when the original reply tables no longer exist.
- **Cheapest first test:** Three histories allow replies `{a,b}, {b,c}, {a,c}`. Compare a pair-guided method, exact core-guided recovery and exhaustive diagnosis; include an apparent split leaving another obstruction.
- **Old-task retention check:** Give each forbidden reply a distinct old-task violation; check normal A/C for the common replies chosen in each answer cell.

#### 10. Keep a checked impossibility receipt, not a failure recording (P)
- **Mechanism:** When available lawful sources provably cannot distinguish an obstruction, retain a compact, versioned no-frontier proof. A later editor skips fruitless queries only while their action and source scope remains unchanged.
- **Novelty vs nearest prior art:** [CEGAR](https://doi.org/10.1007/10722167_15) finds abstraction failures, and [decision-directed active learning](https://arxiv.org/abs/1010.3091) works with decision-equivalence classes. The candidate is a versioned proof that no allowed observation policy separates a live obstruction, reusable without reconstructing deleted records or making refusal sticky.
- **Cheapest first test:** Two histories generate identical responses to all current probes and need different specialists. Test a second editor with the same sources and a third with a newly lawful joint check; compare memoized exact refusal.
- **Old-task retention check:** Check A/C while both early editors refuse, then independently verify A/C on the third editor's successful repair after invalidating the receipt.

#### 11. Audit a cheap answer from a replaced source (I)
- **Mechanism:** Bind the frontier to source and observation semantics, not merely to reply format. A replacement can be used only with a checked mapping whose possible answers cover the new source law.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) already checks assume–guarantee substitutions. This is a source-drift audit of card 08.
- **Cheapest first test:** Replace a truthful sign oracle with one reporting the sign from a stale optimizer snapshot. Compare semantic revalidation with ordinary source version invalidation.
- **Old-task retention check:** Put a protected C failure only on the mismatched sign; verify ordinary A/C for the checked replacement and during fallback on the unchecked one.

#### 12. Choose a frontier for two live edits with incompatible histories (P)
- **Mechanism:** Buy a joint answer only if its lawful observation can discharge scoped obligations for two already-frozen edits after deletion; preserve separate supports where transfer is not proved and account for both reply orders.
- **Novelty vs nearest prior art:** [Near-optimal Bayesian active learning with noisy observations](https://arxiv.org/abs/1010.3091) already aims to identify decision-equivalence classes. The candidate is a split receipt for safely spending acquired evidence on two independent editors.
- **Cheapest first test:** Two pending jobs share one potential parity check. Compare exact joint planning and independent recovery; add a version where only one editor sees a sampler-shifted parity cell.
- **Old-task retention check:** Check A/C for both orderings with the first edit still live, especially C in the false-sharing version.

#### 13. Prove the frontier does not reconstruct more than it needs (I)
- **Mechanism:** Compare frontiers by the residual partition they identify as well as price and availability, with an explicit disclosure limit where the source imposes one. Never treat observed limited disclosure as a privacy proof.
- **Novelty vs nearest prior art:** [The information bottleneck](https://arxiv.org/abs/physics/0004057) already formalizes retaining relevant information. This audit catches near-total reconstruction masquerading as local recovery.
- **Cheapest first test:** Compare a lawful parity bit and a source export containing two bits plus unused keys. Count peak bytes, fields obtained and whether proof checking requires the extra fields.
- **Old-task retention check:** Independently verify A/C under parity-only recovery and test a newly relevant C slice that would make the parity partition insufficient.

#### 14. Reacquire a relation between optimizer slots, not their values (P)
- **Mechanism:** Ask a lawful shadow checker for a certified coupling predicate about live slots. If enough to discharge the proof, save only the predicate and forbid access to the raw states; if ambiguous, use a safe fallback.
- **Novelty vs nearest prior art:** [CROWN](https://arxiv.org/abs/1811.00866) already uses affine bounds to certify properties without enumerating raw inputs. The candidate is a source-restricted observation usable at a second editor's proof boundary, not a more expressive abstract domain.
- **Cheapest first test:** A tiny momentum learner where the sign of a sum determines whether a second update lands safely. Compare a relation query with raw slot reacquisition, exact CEGAR and a stale-moment negative.
- **Old-task retention check:** Check A/C after both optimizer steps, including a held-out C point that fails while the current output and solo slot probes agree.

### Where the two rights interact

#### 15. Buy the cheapest proof that matches the active price failure (P)
- **Mechanism:** Use the offending regret obligation to ask only for facts that distinguish whether its rival policy can actually be cheaper. The same scope miss can need different evidence at different tariffs; never infer completeness from one repaired obligation.
- **Novelty vs nearest prior art:** [Decision-focused learning](https://arxiv.org/abs/1809.05504) identifies costly decision errors and [CEGAR](https://doi.org/10.1007/10722167_15) targets failed predicates. The integration is new only if the discharged proof remains reusable after reacquired evidence is deleted again.
- **Cheapest first test:** Set two rivals' cost planes so a different one binds in each tariff sector, then test both orders of crossing. Compare exact tariff-aware recovery plus an equal-byte cache, with one source inaccessible.
- **Old-task retention check:** Include a tariff at which a repaired rival is cheapest but violates C in a third history. Check A/C after every approved repair and after expiry.

#### 16. Reprice a frontier while its answer is on the way (P)
- **Mechanism:** Split sunk acquisition from remaining check/fit cost. Before applying the reply, verify that its certified branch remains timely and economic under the new quote; otherwise take the prechecked fallback, not a sunk-cost continuation.
- **Novelty vs nearest prior art:** [Shielding in reinforcement learning](https://arxiv.org/abs/1708.08611) already checks safe actions, and delayed belief-state planning can model repricing. The candidate is a residual license whose remaining obligations survive loss of the pre-query detail.
- **Cheapest first test:** In a three-turn game, reprice once after purchase but before delivery; compare exact delayed planning, restart on any drift, and no residual certificate. Test a smooth tariff ramp as well as a step.
- **Old-task retention check:** Check A/C at the repricing turn, under continued transient cover, and when a late answer is discarded.

#### 17. Spend once on a split that yields two smaller price regions (P)
- **Mechanism:** After crossing a boundary, use one lawful answer to partition the live histories and issue a compact child license in each answer cell. Before deleting the payload, prove the child regions and retain the current cell binding; count any answer information it still encodes.
- **Novelty vs nearest prior art:** [Near-optimal Bayesian active learning](https://arxiv.org/abs/1010.3091) buys class discriminators and parametric optimization recomputes regions. The candidate is renewable authorization after multiple actual erasures, not classification accuracy.
- **Cheapest first test:** Alternate tariffs across two boundaries over four jobs. Compare source-query caching, ordinary region recomputation and matched-byte child licenses with the response handle revoked.
- **Old-task retention check:** Check A/C at every child issuance and on a forged handoff with a valid price region but the wrong answer cell.

#### 18. Trade a larger license against source outage risk (I)
- **Mechanism:** Keep extra checked constraints or a broader menu when alternative frontiers are brittle, with availability treated as part of scope. Separate price robustness from outage scenarios rather than treating an unavailable source as expensive but callable.
- **Novelty vs nearest prior art:** [Robust dynamic programming](https://doi.org/10.1287/moor.1040.0127) already plans over uncertain transitions, and [robust counterexample-guided repair](https://arxiv.org/abs/2301.11342) incorporates adversarial uncertainty in repair. This is a cost and availability accounting test, not a new robust planner.
- **Cheapest first test:** Enumerate two source outage laws, including shared failures, at equal byte caps. Compare exact robust planning, extra retained evidence and opportunistic recovery.
- **Old-task retention check:** Keep A/C fixed across outage laws and check the no-source path without using either oracle or silently relaxing C.

#### 19. Two licenses share a query but not a source budget (P)
- **Mechanism:** Combine separately published recovery claims only with checked joint capacity and answer reuse; reserve query rights from one shared ledger and invalidate simultaneous uses that would double-spend them.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) already composes contracts. The candidate is a scoped joint recovery transaction in which both parties deleted their detail and neither may independently assure the other's answer.
- **Cheapest first test:** One source answers one request before expiry, two licensors budget it, and only one cross-job query is jointly legal. Compare exact joint scheduling and independent reservations with and without answer reuse.
- **Old-task retention check:** Check A/C under both scheduling orders and when only one editor receives a reply; verify safe refusal of the other editor's unsupported edit.

#### 20. Lower-bound the bytes plus recovered bits needed for blind repricing (I)
- **Mechanism:** Encode hidden repair identities so a new tariff direction makes one identity decisive. Show that online exact recovery with no available source needs distinct retained states for assignments giving different required dispositions; extend by bounding total written plus newly observed bits.
- **Novelty vs nearest prior art:** [Random access codes](https://arxiv.org/abs/quant-ph/9904093) give information lower bounds for indexed bits. This is a limit on the deletion claim under repricing, not another memory architecture.
- **Cheapest first test:** Four hidden binary identities and four tariff directions with fixed menus; enumerate kept codes and lawful one-bit observations. Include a cheap universal witness that should destroy the bound once it satisfies the regret cap.
- **Old-task retention check:** Wrong identities independently break A or C. Score refusals separately and verify that any universal witness actually passes both old tasks.

#### 21. Separate a real price crossing from a menu expansion (I)
- **Mechanism:** Demand two distinct receipts, one for price membership and one for structural scope. Run a factorial with in/out prices and old/new menus, so the system cannot spend on a probe just because the economic check failed.
- **Novelty vs nearest prior art:** Parametric sensitivity and [contract refinement](https://arxiv.org/abs/2303.17751) already separate parameters from assumptions. This is the negative control for claims that both failures need the same frontier.
- **Cheapest first test:** Four cases with the same original certificate; make the menu expansion add a previously unavailable cheaper safe witness, and use an unrelated tariff crossing. Compare with exact sensitivity plus full lawful replanning.
- **Old-task retention check:** Score A/C on each branch, including a new cheap option that passes the utility target and A but is blocked by C.

#### 22. Learn to leave cheap observations instead of predicting a recovery schedule (P)
- **Mechanism:** Choose among today’s equally useful, verified writes to make a *lawful future observation* discriminate a wider set of price-relevant obstructions. Carry a coverage proof of that observation for held-out editors; do not train or fit on their payloads.
- **Novelty vs nearest prior art:** Dual control improves future information and [trajectory matching](https://arxiv.org/abs/2203.11932) teaches adaptation. The candidate differs from #182's common-reply witness: future disagreement stays, but its recovery interface becomes cheaper and remains checkable after deletion.
- **Cheapest first test:** Two matched writes leave identical current outputs; one couples the decision bit to a permitted shadow check for a frozen family of later jobs. Compare exact dual control, #182's common-reply option, and an equal-byte hint cache on held-out jobs at the same teacher budget.
- **Old-task retention check:** Test ordinary A/C before and after the preparatory write and at every later repair prefix. Include a sham write that improves apparent observability by suppressing a rare C state.

## Ranked deeper questions

1. **Can a small certificate plus local recovery beat a parametric cache stacked with optimal lawful counterexample-guided repair after real deletion?** Start with 01, 08, 15 and 21. Use blind in/out prices, then the optimizer-mediated two-block cross-term with and without a lawful separating source. A win requires matched admitted utility and A/C, with lower total evidence or work even after charging issuance, fallback and recovery.
2. **What must survive deletion to separate recoverable from inherently unknowable scope changes?** Use 09, 10, 14 and 20. Seek an exact finite lower bound and a matching constructive scheme; distinguish missing source, non-separating source and no time to act. If the required artifacts approach the full repair table when tariffs vary, narrow the claim to structured menus.
3. **Can a license be renewed without turning repeated recovery into an expensive cache?** Use 06, 16, 17 and 19 under successive blind updates and shared-source limits. Require a proof that new clauses and child scopes remain valid without dead dependencies; compare cumulative work and peak bytes against full recertification and incremental exact planning.
4. **Can today's update make future recovery genuinely cheaper while retaining the disagreement and all old capabilities?** Use 05, 12 and 22. Compare against exact dual control and the parent's verified common-reply witness, holding today's utility and the future editor family fixed; distinguish a cheaper lawful observation from engineering away the hard old-task slice.
