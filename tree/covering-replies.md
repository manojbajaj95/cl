# Covering replies: change the action set before buying information

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Group obstructions](group-obstructions.md) ([PR #200](https://github.com/manojbajaj95/cl/pull/200)), cards 08 and 19. **Review seeds:** The [PR #200 flood-triage row](https://github.com/manojbajaj95/cl/blob/5878c212655d5cf023e9b3e1d46b2618cc462b92/reviews/flood-triage.md#L309) gives both cards score 3: construct one admissible reply for the whole group rather than buying a split; use truthful training to shape optimizer-slot couplings so future obstructions stay small. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/f3dbc1cf3d7dc26e99fc657d0f2d19079e521dd6/reviews/idea-ledger.md).

## What would make this a continual-learning primitive?

The parent changes what the editor **knows**. This node changes what the editor can **do**, or what couplings it will inherit. For a frozen public transcript, let `H` be all compatible, reachable histories, `M` the incumbent reply menu, and `L` the lawful reply language (including permitted parameters, work and intermediate writes). `R(h)` contains the replies that meet the regret bound and hard old-task floors on `h`, through every served prefix and over the declared continuation scope. A group `G ⊆ H` with `M ∩ ⋂_{h∈G} R(h) = ∅` might still admit a reply in `L`. A covering reply is one executable `r* ∈ L` with a proof of membership in `R(h)` for **every** `h ∈ G`, using no new splitting observation or hidden-state branch. If `G` is only one core, verify `r*` over all of `H` before serving it blindly; piercings of overlapping cores need not compose. A certificate is not permission to inspect the deleted histories. An offline full-state oracle is a diagnostic ceiling, not a deployable arm.

For a fixed reply menu, a **k-bound** means every empty intersection of reply sets for a compatible cell has an empty subintersection of size at most `k` (equivalently, every inclusion-minimal obstruction has size at most `k`). Finding one small core in a cell, observing a low average core size, shrinking the set of held-out edits, or making every history refuse does not establish a useful bound. A training proposal must specify its future edit family and optimizer/continuation scope before training, preserve B gain, and distinguish a theorem under declared premises from an empirical tail estimate. Use same-weight, same-clock slot swaps only in shadow to separate slot mediation from changes in weights, margins or reachable histories. Training examples must be truthful, permitted and selected without held-out payloads.

**Prior-art floor.** [Syntax-guided synthesis][sygus], [counterexample-guided neural repair][repair], [shared replies (PR #173)][shared], [teaching instead of probing (PR #179)][teaching] and [conformant planning][conformant] already search for actions or plans that satisfy multiple cases. [Orthogonal Gradient Descent][ogd], [FOGO][fogo], [Continuous Subspace Optimization][cso] and [partner-aware folds (PR #193, card 02)][fold] already shape interference or compatibility. The candidate isn't generic robust synthesis, slot reset, gradient orthogonalization, or a nice geometric fit. It is a reusable way to **buy a verified action instead of information after deletion**, or to **train a checkable bound on the arity of future blind conflicts**. A result that reduces only verifier runtime, needs extra authority, or ties the strongest matched controls is an improvement, not a new primitive. `P` denotes a conditional candidate primitive; `I` is an improvement or audit.

**Common test rules.** Freeze legal reads, reply language, trainable slots, edit family, A/C floors (including rare slices), B utility target, tariffs and deadlines. Check ordinary old A and disjoint old C independently of the construction's witnesses, before the intervention, at each served prefix and after a held-out continuation. Compare construction against the parent's query-to-split and hitting-set strategies, #173 shared replies, #179 teaching bundles, generic synthesis/repair, the strongest lawful combination of these, and exact joint reply/observation search as an offline ceiling. Compare shaping against unshaped training, a posteriori exact core search, #193#02 partner-aware shaping and ordinary gradient/projection controls at matched B gain, steps, data and initial margins. Charge retained and peak bytes, proof generation/checking, rejected candidates, extra training, inference and fallback; report admitted utility, false approvals, refusals and observation/disclosure costs separately. Include both a group with no lawful covering reply and a planted `(k+1)`-obstruction. Matching outputs is not evidence of retained update behavior (ledger's effect-class distillation); a geometry score is not a plasticity reserve (ledger's falsified Gramian line). All tests below are proposals.

### Paper fixture: expanding a menu is not splitting a cell

Let `M = {e₁,e₂,e₃}` be the three unit vectors. A single committed reply writes a deterministic vector `x` in the simplex; history `hᵢ` has a protected C slice requiring `xᵢ ≤ 1/2`. Ordinary A is unchanged and B accepts any simplex write. Every pair of histories shares a unit-vector reply, but the triple shares none. If the frozen language allows a fractional write, `x = (1/3,1/3,1/3)` serves all three with no query. If only unit writes are lawful, no covering reply exists. A random unit write still damages some C slice with positive probability and is not a substitute for the deterministic write. A fourth compatible history requiring `x₁ ≥ 2/5` independently rejects the proposed `x` even though it covers the original core; `(2/5,3/10,3/10)` covers all four if lawful. This fixture demonstrates scope and the need to recheck overlapping obligations, not a win over convex optimization or a claim about natural incidence.

## Idea cards

### Construct one reply without splitting the group

#### 01. Carry a construction interface with the obstruction (P; parent 08)
- **Mechanism:** Before deleting histories, compile each obstruction witness into a checked constraint on the *holes of a lawful reply template*. Keep those constraints and their coverage proof, not histories or replies for individual cases. After deletion, solve the conjunction and bind the result to the entire public cell; if constraints are only sufficient, `UNSAT` means this template failed, not that all legal replies failed.
- **Novelty vs nearest prior art:** [SyGuS][sygus] and [CEG repair][repair] already synthesize against scenarios. The candidate object is a reusable, deletion-safe interface from an obstruction proof to a new actuator, rather than reacquisition of scenarios or a retained table of fixes.
- **Cheapest first test:** Use the simplex fixture plus the fourth history; compare equally sized cached witness/repair state, #173 shared replies, query-to-split and exact joint search. Charge template compilation across a sequence of held-out coefficient changes.
- **Old-task retention check:** Check A and every C inequality on new coefficient variants; reject any reply justified only for the original triple.

#### 02. Glue common fragments, not complete specialist replies (P)
- **Mechanism:** Export obligations on entry, intermediate states and exit for fragments of rejected specialist replies. Unify holes and synthesize a new ordering whose cross-fragment guarantees discharge all cases without dispatching on the hidden history.
- **Novelty vs nearest prior art:** [Pacti][pacti] composes assume–guarantee contracts; #173 compares shared replies. The extra operation is to extract composable fragments from *incompatible* full replies after deletion and prove that a new sequence, not a choice between specialists, covers the cell.
- **Cheapest first test:** Three two-coordinate toy edits, each specialist unnecessarily clobbering one protected coordinate; test bounded grammar search with and without fragment contracts, plus generic contract composition and the best specialist chooser.
- **Old-task retention check:** Check A/C after every fragment, including a fixture with safe endpoints but no safe ordering in the declared language.

#### 03. Produce a separating witness against an entire actuator family (P)
- **Mechanism:** If construction fails, export a scope-bound obstruction against all parameter values of a template (for linear replies, an infeasibility dual), and attach the exact excluded capability. Route to a split or fallback only after distinguishing this proof from timeout or grammar search failure.
- **Novelty vs nearest prior art:** [Unrealizability for SyGuS][unreal] already supplies language-relative impossibility. Here the exported proof changes which information the blind editor buys, and expires if the lawful reply interface changes.
- **Cheapest first test:** Alternate unit-write-only and fractional-write scopes on a tiny simplex stream; compare generic infeasibility caching plus exact core-guided queries against capability-indexed reuse. Offline exhaustive checks should verify every claimed exclusion.
- **Old-task retention check:** Check A/C on both fallback and late fractional admission; plant a stale exclusion that would wrongly skip a now-safe useful reply.

#### 04. Buy actuation slack before buying observation bits (I)
- **Mechanism:** Search a small preauthorized ladder of reply work (one coordinate, two coordinates, two ticks) and certify the cheapest covering reply; switch to a query only when it is cheaper under the same deadline and admissible utility.
- **Novelty vs nearest prior art:** [Equivalence-class active learning][ec2] and bounded SyGuS already search over information or actuator work respectively. The distinct measurement is a break-even schedule for legal actuator work vs split bits, not a claim to a new search algorithm.
- **Cheapest first test:** Enumerate both axes on a four-history finite menu with nonuniform costs; compare query-first, always-synthesize and exact joint search, including the no-cover fixture.
- **Old-task retention check:** Score the same A/C floors at each tick; extra work that crosses a retention floor is not an actuation option.

#### 05. Certify a reply that never reads the discriminator (P)
- **Mechanism:** Type the reply with a read/write effect manifest that excludes deleted or discriminating slots, and separately certify the same reply across reachable histories. A normal public input is allowed; a live slot statistic that identifies the history is a split and must be charged as one.
- **Novelty vs nearest prior art:** [Information-flow typing][flow] and conformant planning already separate blind and contingent actions. The reusable object here pairs an enforceable no-read boundary with a post-deletion retention obligation on the actual reply.
- **Cheapest first test:** A shared update that drops an ambiguous coordinate versus a purportedly blind learned gate that reads it indirectly through a cache; compare dynamic read logging, a type checker plus ordinary verification, and a licensed queried gate.
- **Old-task retention check:** Vary the forbidden slot in shadow and check A/C after the same blind script; use a delayed C failure to show noninterference alone does not certify retention.

#### 06. Keep the intersection as an editable reply envelope (P)
- **Mechanism:** Export a certified inner region of covering replies tagged by public cell and suffix, rather than one chosen payload. A later public constraint can narrow that region without asking the old histories; expanding or moving outside it needs a new proof.
- **Novelty vs nearest prior art:** [Pacti][pacti] and [CROWN][crown] express feasible contracts or affine bounds. The hypothesis is that a small inner region is a reusable permission to *choose a new reply*, beating cached individual reply certificates at the same bytes.
- **Cheapest first test:** Issue different held-out B targets inside and outside a two-dimensional region; compare an inner polytope, a same-byte bank of checked points, generic parametric synthesis and full re-verification.
- **Old-task retention check:** Verify independent A/C at extremal points and held-out interior replies; include a C-sensitive suffix excluded by the region's validity scope.

#### 07. Synthesize one adapter with a protected residual budget (P)
- **Mechanism:** Use the obstruction's projected obligations to fit a common low-rank corrective block; allocate each protected slice an explicit residual margin and verify that the same block plus the worst legal continuation stays within every margin. Include rank and training cost in the tariff.
- **Novelty vs nearest prior art:** [LoRA][lora] and [CEG repair][repair] already restrict repair geometry or enforce robust specs. The candidate is an adapter synthesized against **retained obligations** in a blind edit, not one adapter per history or historical-example rehearsal.
- **Cheapest first test:** A rank-one linear correction on three branches with one rank-two-only negative; compare equally ranked pooled repair, gradient projection and exact bounded-rank search at matched admitted B.
- **Old-task retention check:** Check A/C under extremal legal suffixes, including a rare C direction outside the fitting span. Do not infer retention from a small fit residual.

#### 08. Add a universally safe intermediate state to the language (P)
- **Mechanism:** Construct one script that first parks a shared coordinate in a neutral state safe for every history, then applies the useful change, then retires the park. No reading which history actually occupied it. Certify capacity and service at the intermediate state as well as the final state.
- **Novelty vs nearest prior art:** [Make-before-break (PR #157)][make] and transactional updates already protect transitions. The hypothesis is that a temporary actuator synthesized from a group certificate can change realizability without introducing per-history migration.
- **Cheapest first test:** A two-tick table with a shared spare and three incompatible direct replacements; compare generic conformant planning, exact joint search and an ordinary make-before-break template. Remove the spare for a no-cover negative.
- **Old-task retention check:** Interrupt immediately after the park and run old A/C, then resume under a held-out permitted suffix. Do not count a script that only passes at commit.

#### 09. Mint a public reply parameter from a counterexample certificate (P)
- **Mechanism:** Turn a separating inequality into a public template parameter (e.g. a cap on a common write), re-prove the new law across the entire cell, and reuse the parameter only for editors instantiating the certified schema. No per-deployment counterexample sampling.
- **Novelty vs nearest prior art:** [SyGuS][sygus] and [CEG repair][repair] already use counterexamples to guide refinement; the proposed product is a compact, transferable restriction on **future reply construction** rather than a repaired incumbent.
- **Cheapest first test:** Three linear editors sharing a certified cap but with different payloads, plus one fourth editor violating its interface; compare generic invariant caching, capped repair and per-editor synthesis.
- **Old-task retention check:** Check held-out A/C after edited payloads at and just beyond the cap; verify the out-of-scope editor cannot inherit the certificate.

#### 10. Repay construction cost across overlapping cores (P)
- **Mechanism:** Build a cover frontier keyed by implication between obligations, not by history IDs. A newly minted reply can retire several cores only when a verifier proves the union of their obligations; later compatible histories can invalidate the frontier entry without revealing which old core occurred.
- **Novelty vs nearest prior art:** [CEGIS][sygus] reuses counterexamples and the parent caches cores. This caches the positive consequence of actually adding a lawful action and explicitly scopes it to multiple obstructions, rather than assuming piercing one erases the rest.
- **Cheapest first test:** Use the four-history fixture and a sequence of changed constraints. Compare exact core caching plus generic reply caching, synthesis from scratch and one-reply amortization at matched memory.
- **Old-task retention check:** Give the newly overlapping history a distinct rare C slice. Check it alongside ordinary A and prior C after each reuse, not only after initial synthesis.

### Shape training so future obstructions have small witnesses

#### 11. Train a shared convex chart for viable replies (P; parent 19)
- **Mechanism:** Use truthful batch ordering or constrained optimizer updates to keep slot effects in a predeclared `d`-parameter chart where each history's admissible replies in that chart are convex. If the deployed menu is that common convex domain, finite Helly gives `k ≤ d+1`. If it also includes other reply families, the chart proof alone does not bound the whole menu.
- **Novelty vs nearest prior art:** [Helly's theorem][helly] gives the bound, and [CSO][cso] shapes update subspaces. The candidate is to train for a verified **future reply-domain** property, not a low-rank optimizer or gradient statistic alone.
- **Cheapest first test:** Use a linear momentum learner and a two-dimensional continuous reply chart; compare unshaped, #193#02 and ordinary projected training at matched B. Plant a nonconvex admissibility slice and a discrete-menu variant, which must both invalidate the claimed chart proof.
- **Old-task retention check:** Independently check ordinary A, rare C and a second continuation step. Measure refusal and useful edits to rule out a chart that merely cuts off plasticity.

#### 12. Align the binding constraints, not the optimizer vectors (P)
- **Mechanism:** Fit a frozen bank of symbolic future edit probes to identify which slot-mediated inequalities bind reply feasibility. Train truthful updates to keep those inequalities in a common one-dimensional reply coordinate with interval safe sets. Disjoint intervals have a witness of size at most two, even when moment vectors remain far apart.
- **Novelty vs nearest prior art:** [OGD][ogd] protects old outputs and [CROWN][crown] bounds responses. The target here is preservation of interval-shaped feasibility across hidden histories, including the B regret constraint, rather than near-zero gradient interference.
- **Cheapest first test:** Two-slot momentum worlds where equal vector norms yield different allowable intervals; compare anisotropic shaping, projection and norm clipping. Use exact reply enumeration or interval intersection, and shadow swaps at common weights and clock.
- **Old-task retention check:** Keep a C task sensitive to the coordinate the projection ignores and check it after a held-out second update; matching A and B alone is insufficient.

#### 13. Enforce a small union of convex reply charts (P)
- **Mechanism:** Train against a fixed set of chart tags and shape slot relations so each history's allowed parameters for each tag are convex. If a cover is impossible, select a Helly witness per tag; with `m` tags of dimension at most `d`, their union proves a bound `m(d+1)`. The tag selects the reply, not the hidden history.
- **Novelty vs nearest prior art:** [Disjunctive programming][balas] represents unions of convex pieces. The proposed training contract preserves useful discrete modes while giving a bound on future obstruction arity, rather than forcing one convex relaxation.
- **Cheapest first test:** Two one-dimensional lawful actuator modes with distinct uses; compare a single chart, chart-aware shaping, generic mixed-integer synthesis and exact post-hoc cores. Plant a hidden third mode that invalidates the declared union proof.
- **Old-task retention check:** Check A/C when either mode is deployed blindly, with a rare C task served by only one mode; do not claim savings if shaping suppresses that mode.

#### 14. Bound arity by a small exact conflict vocabulary (P)
- **Mechanism:** In a fixed template, train slot dynamics so all history exclusions factor through at most `k` predeclared predicates on reply parameters. Prove exactness in the declared scope: each history excludes the union of the predicate regions it activates. Choosing one activating history per used predicate reproduces the full exclusion union, hence bounds an obstruction by `k` histories.
- **Novelty vs nearest prior art:** [CEGAR][cegar] selects predicates after seeing a failure. This instead trains so a fixed predicate vocabulary remains complete for future reply exclusion, certifying a witness count, not merely accelerating abstraction.
- **Cheapest first test:** A finite quantized optimizer with three exclusion predicates; compare truthful predicate-preserving ordering, post-hoc CEGAR and unshaped training with matched margins. Exhaustively validate against a planted fourth exclusion outside the vocabulary.
- **Old-task retention check:** Give the fourth exclusion a disjoint old C failure and ensure the proposed abstraction cannot erase it; run ordinary old A/C outside the calibration probes.

#### 15. Preserve ordered nested reply sets through slot updates (P)
- **Mechanism:** Train on truthful sequences with a checked monotonicity condition: after conditioning on the public cell, each joint A/C-and-B admissible set nests along a scalar slot order. A finite incompatible cell then has a singleton witness. Condition must hold for the *whole joint* reply set, not just one margin.
- **Novelty vs nearest prior art:** [Isotonic regression][isotonic] fits monotone responses; [FOGO][fogo] reduces interference. Here monotone *set inclusion* is a training invariant for future blind feasibility, not a learned scalar risk predictor.
- **Cheapest first test:** Three reachable orderings of the same truthful minibatches in a scalar learner. Compare sorted curricula, monotone shaping, B-matched unshaped training and exact set checks; plant crossing lower/upper reply bounds.
- **Old-task retention check:** Include a rare C slice whose lower margin reverses the A order, and confirm it invalidates nesting before an unsafe reply is admitted.

#### 16. Make the low-arity invariant survive the optimizer clock (P)
- **Mechanism:** Prove a slot-coupling invariant closed under the permitted optimizer clock, including decay/bias corrections and one held-out step; filter only training transitions that leave the invariant. A current-state fit earns no bound for a later horizon without closure.
- **Novelty vs nearest prior art:** [Barrier certificates][barrier] prove dynamical invariance and #200#12 leases a relation by decay. Here the invariant supports the future reply-arity theorem across edits instead of keeping a queried bit fresh.
- **Cheapest first test:** Enumerate three reachable Adam clocks with common weights, then compare horizon-unrolled checks, clipping, and invariant-guided training. Include a delayed `(k+1)` case hidden at the same current logits.
- **Old-task retention check:** Run A/C after the entire held-out horizon, including at the clock transition where the planted obstruction would first expose C.

#### 17. Localize a coupling by inserting a truthful counter-gradient (P)
- **Mechanism:** Among permissible orders of an already available truthful batch, choose one whose optimizer recurrence cancels a cross-slot term that makes reply boundaries nonconvex. Require a matched weight endpoint and optimizer clock; prove the boundary property on the full reachable family, not one observed cancellation.
- **Novelty vs nearest prior art:** [Slot splices (PR #185)][splice] already use phased cancellation as a witness for a particular future edit. The proposed product is a persistent structural invariant limiting obstruction size for a declared family, not a transplant or one-step rescue.
- **Cheapest first test:** Enumerate opposite orders of two cancelling gradients plus a coupling pulse; compare random order, direct reset, projected updates and exact a posteriori core search. Swap slots in shadow to test causality.
- **Old-task retention check:** Check A/C between batches as well as at common endpoints, then after a held-out pulse with a different sign and the same B objective.

#### 18. Train with adversarial high-arity cell counterexamples (P)
- **Mechanism:** On development edits only, find a reachable minimal obstruction larger than `k` and translate its binding slot interaction into a training-time constraint. Obtain a global arity proof only from an invariant or exhaustive coverage of the declared reachable family; otherwise report the held-out tail, not a guarantee.
- **Novelty vs nearest prior art:** [CEG repair][repair] eliminates failures and ordinary hard-example training prioritizes bad cases. This attacks a joint contradiction whose proper subgroups already pass; reducing mean regret or collecting more individual failures can leave it untouched.
- **Cheapest first test:** Reorder truthful data in a tiny momentum learner while searching development cores. Compare with pairwise interference adversaries, a posteriori exact search and #193#02, and reserve a different planted `(k+1)` family for evaluation.
- **Old-task retention check:** Hold out rare C slices and whole edit types; reject any apparent core reduction due to changing margins, lowering B gain, or refusing all the hard edits.

#### 19. Partition slot writes into independently checkable reply factors (P)
- **Mechanism:** Shape the update so the shared legal reply domain is a Cartesian product and each history's full feasible set factors over blocks. An empty joint intersection then implies one block is empty; certify its local arity bound. A shared budget, normalization or regret constraint can break factorization and must be handled explicitly.
- **Novelty vs nearest prior art:** [GPM][gpm] protects gradient subspaces and [Pacti][pacti] decomposes contracts. The proposed output is a training-preserved certificate that the global obstruction can be found locally, with a separate proof that no hidden global coupling remains.
- **Cheapest first test:** Two blocks with interval feasibility and one optional shared work cap. Compare blockwise shaping, naive blockwise verification and exact global checks; demand proof rejection with the unmodeled cap enabled.
- **Old-task retention check:** Use C on a cross-block combination invisible to local probes and old A on each block; check all after the joint reply and its next update.

### Combine training and construction only if the interaction pays

#### 20. Train a reply compiler's domain, not its answers (P)
- **Mechanism:** Precommit a small compiler and train truthful optimizer dynamics so future cores lie in its proven coverage domain; payloads and chosen replies remain held out. The compiler abstains outside scope. The interaction should let a compact compiler cover cell types that neither shaping with the old menu nor generic synthesis at the same budget can serve.
- **Novelty vs nearest prior art:** [Amortized program synthesis][amortized] accelerates repeated search. Here training changes reachable slot couplings to make a *checked* compiler applicable, and never distills per-history repairs.
- **Cheapest first test:** A `2×2` on a finite momentum learner (shaping vs unshaped, compiler vs generic synthesis), plus the strongest separately optimized shaping and synthesis controls stacked at equal time and bytes. Reserve unseen reply payloads and a no-cover cell.
- **Old-task retention check:** Check ordinary A/C in all arms during training and after blind execution, with a rare C slice that the compiler's fast check does not use.

#### 21. Issue expiring coverage guarantees with a prechecked fallback (P)
- **Mechanism:** Couple a training invariant with a generated covering script and a public expiration event (clock, optimizer schema, or allowed workload change). Before expiry the invariant discharges the reply proof; after expiry, fall back or use a fresh proof, not a read of stale hidden slots.
- **Novelty vs nearest prior art:** [Pacti][pacti] checks compositional scope, and #200#12 leases observations. This proposed lease grants a blind actuator justified by a training invariant, not reuse of an observed predicate.
- **Cheapest first test:** Use a six-tick toy stream with a registered optimizer transition; compare fresh CEG repair every tick, ordinary certificate caching plus invariant checks, and an unsafe no-expiry negative.
- **Old-task retention check:** Stress a C slice whose failure first becomes possible just after expiry. Check A/C on the last legal reply and on actual fallback after expiration.

#### 22. Search for the regime where the two seeds lose (I)
- **Mechanism:** Tabulate the cheapest verified combination of training, construction, split and refusal under fixed service, on small fully enumerated streams; separate menu obstructions, language obstructions, and proof failures. Count the largest minimal core, not only the first core found.
- **Novelty vs nearest prior art:** [Equivalence-class active learning][ec2] and [CEG repair][repair] solve different work allocations. This is a falsification audit to see whether the proposed interfaces buy anything beyond their best stacked implementations.
- **Cheapest first test:** A factorial paper/CPU grid: cheap vs costly queries, reusable vs one-off jobs, lawful vs impossible cover, and naturally reachable vs planted `(k+1)` cores. Report any dominance reversal after charging the training and proof work.
- **Old-task retention check:** Compare only arms meeting the same per-slice A/C floors and B utility; report failures and refusals separately, including the observation-only baseline.

## Ranked deeper questions

1. **Can a blind editor construct a genuinely new lawful reply more cheaply than it can buy the split, once the deleted histories stay deleted?** Start with 01, 03 and 22. Separate recoverable menu obstructions from language impossibility and compare with exact joint search as the ceiling. A win must survive #173 + #179 + generic repair and the strongest affordable split strategy at matched B utility and A/C.
2. **Can truthful training impose a useful arity bound on held-out blind edits without shrinking what the learner can do?** Start with 11, 13 and 19. Require a proof for the declared language and horizon, a planted `(k+1)` negative and a weight/clock-controlled slot mediation test. If only the empirical tail shrinks, report that narrower result.
3. **What is worth retaining after the first successful construction: a template constraint, a region, or the reply itself?** Use 01, 06 and 10 on overlapping cores and changing public targets. Compare to equal-byte cached replies plus ordinary verification, including stale-scope and rare-C negatives.
4. **Do the two seeds interact or merely add their separate gains?** Use 20 and 21 with the best stacked controls. Count a joint win only if shaping makes new blind constructions applicable often enough to repay its own training and certification cost, without hiding work in an observation or fallback.

**Verdict:** Keep the covering-reply claim only if one checked, useful reply works across the whole compatible cell without extra information and beats the best matched split-plus-repair stack. Keep slot shaping only if it lowers the size of the worst necessary obstruction witness in a declared future family without buying the reduction through missed edits, weaker B gain or lost A/C retention. The toy fixtures make these claims falsifiable, not established.

[sygus]: https://doi.org/10.1109/FMCAD.2013.6679385
[repair]: https://arxiv.org/abs/2301.11342
[shared]: https://github.com/manojbajaj95/cl/pull/173
[teaching]: https://github.com/manojbajaj95/cl/pull/179
[conformant]: https://arxiv.org/abs/1401.3468
[ogd]: https://arxiv.org/abs/1910.07104
[fogo]: https://arxiv.org/abs/2606.10406
[cso]: https://arxiv.org/abs/2505.11816
[fold]: https://github.com/manojbajaj95/cl/pull/193
[pacti]: https://arxiv.org/abs/2303.17751
[unreal]: https://arxiv.org/abs/1905.05800
[ec2]: https://arxiv.org/abs/1010.3091
[flow]: https://doi.org/10.1109/JSAC.2002.806121
[crown]: https://arxiv.org/abs/1811.00866
[lora]: https://arxiv.org/abs/2106.09685
[make]: https://github.com/manojbajaj95/cl/pull/157
[helly]: https://arxiv.org/abs/1508.07606
[balas]: https://doi.org/10.1016/S0167-5060(08)70342-X
[cegar]: https://doi.org/10.1007/10722167_15
[isotonic]: https://doi.org/10.1214/aos/1176345866
[barrier]: https://doi.org/10.1109/TAC.2007.902736
[splice]: https://github.com/manojbajaj95/cl/pull/185
[gpm]: https://arxiv.org/abs/2103.09762
[amortized]: https://arxiv.org/abs/2006.08381
