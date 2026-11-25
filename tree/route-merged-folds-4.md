# Route-merged folds IV: repair global colour obstructions and borrow only the weight reads already paid for

**Status:** Ideas only; no learner experiments, implementation, or GPU work. **Parent:** [Route-merged folds III](route-merged-folds-3.md) ([PR #298](https://github.com/manojbajaj95/cl/pull/298)). **Review seeds:** [Flood triage, rows 414–417 (PR #298 at row 416)](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L414-L417), on [PR #6](https://github.com/manojbajaj95/cl/pull/6), gives score 3 to [#298#03](route-merged-folds-3.md#03-attack-a-colour-lower-bound-with-no-large-clique-p-29113) (target a non-clique obstruction without changing the largest clique) and [#298#13](route-merged-folds-3.md#13-use-the-weightmoment-relation-instead-of-storing-a-correction-p-29102) (make required C couple weights and moments so a fixed reader needs a smaller key). The #291 graph and reachability ideas are controls, not new seeds.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). No Noether-style gradient-flow storage, fixed-point restore, fitted observability proxy, or credit for facts encoded in weight precision the old reader never used. **P** is a candidate reusable operation; **I** is an audit or improvement. The prior-art comparisons are starting points, not exhaustive novelty claims.

## What might be new?

[Witsenhausen](https://doi.org/10.1109/TIT.1976.1055607) and [Orlitsky–Roche](https://doi.org/10.1109/ISIT.1995.550438) already say how to distinguish histories when a decoder has lawful side information. Odd-cycle transversals, critical graphs and SAT cores already describe why a fixed graph does not fit. The bet is that such a witness can tell a learner *which mandatory batch to do next*, even when local disagreement and clique size send it the wrong way. On the optimizer side, predictive residual coding and [Guarded Compression of Adam State](https://www.alphaxiv.org/abs/2611.00589) are controls. The bet is that ordinary C can make a fixed reader reconstruct the required moment contribution using an existing weight read and less extra state, not that a better fitted predictor saves bytes on an untouched checkpoint. A joint win must beat doing those two things independently and coding the resulting state exactly.

## Contract and first gates

- Inherit the [parent contract](route-merged-folds-3.md#contract-and-first-gates): A is old-task service, B is successor service, C is required labelled work. Fix the discrete update, legal observations and request/arrival support **per history**, frequencies, deadlines, horizon, arithmetic, expiry and fallback. No C action may alter the request law, relabel a record, insert work, or use an unobserved future arrival. Compare equal C service and width-steps and price evidence, working memory and latency. History identities stay fixed even when states coincide.
- Build the exact confusion graph from unequal required continuations at a shared legal observation. An edge survives until its last witness is gone; if the interface includes a weight read, that read is part of the observation. Keep the request law fixed and report weight-read values and fibers separately: a changed weight value may refine observations without changing any requests. Diagnose that effect with matched weight-fiber controls; do not credit it as smaller conditional moment variation. Compare graph-only arms at fixed observations. Report clique number, exact colours, rounded width, peak allocated bytes and any B write the release actually admits.
- Freeze the weight tensor/interface, precision, read sites and decoder before selecting C. No extra read, wider weight, schedule tag, writable slack bits or encoding-time mutation. Forecast the **demanded contribution**, not necessarily the whole moment. Test against the exact unfolded continuation for each C order, including the first state-mutating B action and any later read inside the horizon. Count the key, decoder/verifier tables, normal weight reads, and any state held over to expiry. In the strongest positive test keep full post-C states distinct, momentum live, and the weight fibers nontrivial. Report changes in weight values and A-visible behavior rather than treating identical tensor shape as evidence of a free signal.
- Score held-out A at entry, after each C batch, at the cut, after each legal first B read and after the write that spends any released capacity; the cards add targeted A probes. Require pinned A/B/C floors and matched service in addition to exact replay. Include an untouched obstruction and a C stream whose legal weight reads cannot predict moments.
- **Stacked control:** causal #298#03 graph-directed C, causal #298#13 relation-directed C, their best feasible sequential combinations in both orders, and exact conditional coding on each resulting state, with equal evidence budget, expiry and fallback. Include #291#13 edge-count C, #291#02 reachability-only C, max-clique/per-request selectors, random eligible prefixes, equal-byte quantization and a reset arm with scored retention. Give exact static coding the candidate order as well: a tie there credits the C policy only. Tiny exhaustive causal selection is a ceiling on service for the pinned budget, not a practical implementation claim.

## One exact paper check (not a learner result)

Take histories `u,v,a,b,c,d,e,f,g`. Hold nine histories and ten request pairs fixed: `uv,ua,ab,bc,cv,ud,de,ef,fv,vg`. Each pair is a legal common request for its two endpoints only. In table X all pairs disagree except `vg`; in table Y all disagree except `uv`. Thus each graph has nine edges and clique number two. X contains two five-cycles sharing `uv`; for a three-colouring, assign `u,b,e,g` colour 0, `a,c,d,f` colour 1 and `v` colour 2. Y has bipartition `{u,b,e,v}` / `{a,c,d,f,g}`. The shared edge was a one-edge hit on both odd cycles; swapping it for `vg` changes exact width from 2 bits to 1 with no change in maximum clique or edge count. Deleting only `ab` leaves the other five-cycle alive.

These are answer tables, not outcomes of lawful C updates. The check motivates card 01; it says nothing about learner reachability, A retention, conditional coding with weights, or allocated bytes.

## Idea cards

### 01. Spend one required batch on two odd cycles (P; #298#03)
- **Mechanism:** Collect two surviving odd cycles at a one-bit fold target. Prefer a legal C prefix that kills every witness of a shared edge over a prefix that repairs an edge in just one cycle. Spend the saving only after a complete bipartition check.
- **Novelty vs nearest prior art:** Edge bipartization and #298#03 already find obstructions. The proposed operation maps overlapping obstructions to a single executable batch effect with shared evidence and service cost.
- **Cheapest first test:** Use the paper graph as a target for enumerating a tiny finite momentum host with two legal prefixes. Compare first-cycle, edge-count, max-clique and exhaustive selectors, including a shared edge with two independent request witnesses that no one batch removes.
- **Old-task retention check:** Test A on histories from both cycles, including vertices not incident to the shared edge, and after each legal B read.

### 02. Target a three-colour failure that has no triangle (P; #298#03)
- **Mechanism:** At a four-to-three colour target, use a minimally infeasible three-colouring subproblem, rather than a list of odd cycles. Search required C prefixes that make the subproblem three-colourable, then verify the entire graph. A standalone key still takes two bits; claim a gain only at a declared allocation boundary, e.g. a batch of five jointly packed keys that shrinks from ten bits to eight.
- **Novelty vs nearest prior art:** Critical graphs and SAT unsatisfiable cores are established. The new target for C selection is a change missed by both max-clique and odd-cycle presence, not a new graph lower bound.
- **Cheapest first test:** Try a triangle-free four-chromatic graph such as the Grötzsch graph as an obstruction template. Enumerate a two-batch host for a four-to-three change while at least one odd cycle survives; compare odd-cycle and core selectors against the exhaustive frontier.
- **Old-task retention check:** Test A at every vertex of the returned core and on a held-out legal history outside it after C and the first B read.

### 03. Choose batches that block newly created odd cycles (P; #298#03)
- **Mechanism:** If a candidate repair removes an old disagreement but creates another edge, reserve a second due batch that prevents the new edge from closing an even-length path into an odd cycle. Evaluate the two actions against a single parity obligation instead of ranking their edge effects independently.
- **Novelty vs nearest prior art:** #298#04 permits edge trades; offline dynamic bipartiteness checks their aftermath. The candidate selects a compensating ordinary update specifically because of the parity of a path that the first batch creates or preserves.
- **Cheapest first test:** Enumerate three due records and score exact graph snapshots for each legal two-record prefix. Compare one-step edge-trade, shortest-cycle deletion, and two-step exhaustive selection with equal service; include a menu that cannot prevent the replacement cycle.
- **Old-task retention check:** Check A in the intermediate state while the replacement cycle exists and on both paths after folding and B service.

### 04. Factored witnesses for batch choices that cannot help (P; #298#03)
- **Mechanism:** For a candidate family of C prefixes, certify that each family member leaves at least one odd cycle, even if no one cycle survives every member. Use that certificate to skip the family and spend the decision budget on another eligible family.
- **Novelty vs nearest prior art:** Branch-and-bound and robust colouring produce infeasibility certificates. Unlike #298#20's common colour certificate, this is a family-level *negative* certificate for C choices, with potentially different counterexamples per branch.
- **Cheapest first test:** Enumerate two independent binary ordering choices and build two witness cycles whose survival depends on only one of the choices. Compare the number and bytes of exact continuation queries against exhaustive rejection and a single-obstruction refusal rule.
- **Old-task retention check:** Test A both when the learner falls back after rejecting a family and when it folds using the surviving family; score the same A deadlines.

### 05. Aim C at the edge that pins the wrong parity (P; #298#03)
- **Mechanism:** At a live cut, valid existing keys may be immovable under the declared migration cap. Treat their opposite/equal bit requirements as parity constraints and use C to repair the shortest contradiction between pinned endpoints, without rewriting those keys.
- **Novelty vs nearest prior art:** Precolouring extension is classical and #298#08 pins retirement. The candidate changes learner disagreement along a path so an existing live encoding extends to new histories with no key movement, even when unrestricted colour count never changes.
- **Cheapest first test:** Start with a bipartite host and two pinned histories at the wrong parity distance. Enumerate two legal C orders, comparing unpinned colouring plus paid migration, parity-aware selection and refusal; include an isolated or compatible pinned pair as a null.
- **Old-task retention check:** Reissue A reads tied to both old keys after the new histories enter, and check A on the intermediate path histories after B.

### 06. Fold at a certified separator without clearing both sides (P; #298#03)
- **Mechanism:** Find a vertex separator with compatible colourings on each side but incompatible sets of colour assignments at the boundary. Use ordinary local C on one side to enlarge its boundary menu until it shares an assignment with the other side, leaving the remote side's state alone.
- **Novelty vs nearest prior art:** Separator dynamic programming and #298#06's reuse of a codebook are controls. Here the separator identifies a *one-sided modification* of the reachable disagreement relation, not a way to search a fixed graph faster.
- **Cheapest first test:** Glue two bipartite paths of opposite parity at labelled endpoints. Search a two-route host for a C record touching only one side where a change to that path buys compatibility; compare globally recolouring unchanged state, joint C and random local C.
- **Old-task retention check:** Probe A on the untouched side and both boundary vertices as well as on the side that got C, before and after B.

### 07. Aim at a colour-budget obstruction that grows only in combination (P; #298#03)
- **Mechanism:** Run a shared C policy across two independently arriving history families whose union must use one slot format. Choose it against a cross-family obstruction assembled only from legal common observations; no single family has an obstruction on its own and the chosen order needs no family tag at decode.
- **Novelty vs nearest prior art:** #298#06 shares a codebook across ingress points; universal coding for multiple sources is established. The proposed steering target is a witness requiring histories across sources, not compatible codecs for graphs each source already supplies.
- **Cheapest first test:** Split an odd cycle across two recorded ingress populations and search a tiny discrete learner for a common order that changes only a cross-family edge. Compare separately optimizing each family, full static coding of the union, and a matched no-common-request null.
- **Old-task retention check:** Test A separately per population and after B on both endpoints of the cross-family edge; do not average away failure in the smaller population.

### 08. Reuse a contradiction across arrivals, not a predicted graph (I; #298#03)
- **Mechanism:** Cache only the exact continuation queries needed for a small contradictory subgraph. When another legal arrival changes the state, revalidate those queries before using the witness to steer C, discarding it on the first invalidated edge.
- **Novelty vs nearest prior art:** Incremental SAT already reuses proof state; #298#20 targets a common certificate across envelopes. This audit asks whether charged revalidation of a lower-bound witness can beat full graph reconstruction under actual optimizer transitions.
- **Cheapest first test:** Enumerate two sequential cuts, with a frequent arrival that preserves the old witness and a rare one that removes its last edge. Compare paid query counts and peak bytes against rebuild and a stale-witness heuristic; never accept a fold without fresh exact verification.
- **Old-task retention check:** Test A on the rare invalidating arrival, on fallback, and after the first ordinary B update in the common case.

### 09. Keep the weight aliases; shrink only the moment differences (P; #298#13)
- **Mechanism:** Choose C to align required moment contributions *inside* precommitted lawful weight-read fibers while preserving the membership of those fibers. A moment-sensitive read not included in the reconstruction target must still have paid state if it is owed later.
- **Novelty vs nearest prior art:** Conditional coding buys cheaper descriptions with good side information. This operation deliberately rules out better identification via weights, isolating an intervention on residual distinctions beyond #298#13's unrestricted relation.
- **Cheapest first test:** Search a two-parameter discrete momentum host for two orders with the same weight-fiber partition, distinct full states and different residual multiplicities. Compare exact conditional coding per order, equal-byte quantization and a pair whose residual variation no allowed batch changes.
- **Old-task retention check:** Test A on multiple histories inside each unchanged weight fiber, including A probes that expose lost optimizer behavior after an ordinary B update.

### 10. Train one key to answer two different weight reads (P; #298#13)
- **Mechanism:** Choose C so the same stored residual label works with two existing weight read sites, using a fixed route-specific reconstruction at each, even when the values read differ. Encode before the request and never materialize a second weight read on that route.
- **Novelty vs nearest prior art:** Coding with multiple decoders (Heegard–Berger) and #298#13 are closest. The intervention makes a single residual label usable across read interfaces instead of optimizing a code for given weights at each decoder.
- **Cheapest first test:** Enumerate two routes that read disjoint parameter blocks and a small due C menu. Look for smaller exact joint key width while the best code for each individual route is unchanged. Compare separate residual codes and exact joint coding on the unsteered host.
- **Old-task retention check:** Check held-out A through both blocks before C, after the cut and after each route uses the shared key to update its own block.

### 11. Learn a residual that survives the first weight mutation (P; #298#13)
- **Mechanism:** Select C so the predeclared residual key and the lawful *new* weight read suffice after a real B update, without remembering the old weight. Try to make the key reusable unchanged through that update; never defer a read to a convenient snapshot.
- **Novelty vs nearest prior art:** Recursive state estimation and #298#07's service-cut colours are controls. The claim is exact cross-cut reuse of a side-information residual earned by C without retaining either a pre-update snapshot or a freshly computed residual.
- **Cheapest first test:** Enumerate one C prefix followed by two required B reads with an optimizer step between. Compare one immutable key, a paid residual refresh, and a saved old weight read. Include a B step whose own weight update destroys the relation.
- **Old-task retention check:** Probe A immediately after the weight mutation and after the second B read, including histories with identical new weights but different old ones.

### 12. Expose only the moment contraction the reader spends (P; #298#13)
- **Mechanism:** Target a relation between an unchanged weight interface and the exact projection of momentum needed by a declared successor, leaving other moment directions live where old or later reads still require them. Fold the projected contribution only if those other directions' costs are charged.
- **Novelty vs nearest prior art:** Functional compression and reduced-order observers already target a function rather than full recovery. The candidate is using due C labels to change which projection is predictable without shrinking the full conditional moment state.
- **Cheapest first test:** On a two-coordinate learner, pin B to an existing rank-one momentum read and add a real later route sensitive to the other direction. Compare C aimed at the contraction to full-moment coding, single-route minimization and an equal-byte low-rank sketch.
- **Old-task retention check:** Include A examples sensitive to the orthogonal direction and score them after both the projected B action and the later reader.

### 13. Make a fixed decoder work on an unseen C order (P; #298#13)
- **Mechanism:** Predeclare one algebraic reconstruction law and choose among legal orderings of whatever C records actually arrive so the reached state satisfies it. Use the same compiled decoder on held-out arrival menus; store neither order fingerprint nor per-menu coefficients.
- **Novelty vs nearest prior art:** Dictionary reuse and #298#16's common reader law over disconnected charts are nearby. Here the law must be fixed before seeing held-out arrivals, and due work has to land on it without a menu identity at decode.
- **Cheapest first test:** Freeze a low-parameter integer decoder on one small arrival menu, then enumerate different required records at test time, some with no valid order. Compare header-priced conditional codebooks, the fixed decoder without steering and exhaustive lawful steering with scored refusals.
- **Old-task retention check:** Assess A on both successful and refused held-out menus through the first B step; include histories for which two legal orders produce different A behavior.

### 14. Make an existing read span the missing contraction under both masks (P; #298#13)
- **Mechanism:** With two legitimate weight masks already in service, choose C so each masked read plus the same residual can recover a common owed contribution whenever that mask is the one naturally exposed. Do not use the union of the masks or choose which mask arrives.
- **Novelty vs nearest prior art:** Erasure side information and multiple-description coding already handle missing coordinates; unlike card 10's different output laws, this asks C to make two incomplete reads interchangeable for the *same* continuation requirement.
- **Cheapest first test:** Pin two complementary masks and a full-state exact reference. Enumerate a due C menu and compare exact conditional coding with either mask, union-as-oracle, and separate paid correction for each mask; include a state where one mask erases the deciding coordinate.
- **Old-task retention check:** Probe A on both masked coordinate groups after each C batch and after the B step exposed through each mask.

### 15. Make coarse lawful weights suffice without leaning on a rounding tie (P; #298#13)
- **Mechanism:** Aim C for a relation that supports reconstruction throughout each reachable cell of the *existing* rounded read, rather than only on a rounding boundary. Verify on the pinned discrete host and treat arithmetic variants as separately declared robustness arms.
- **Novelty vs nearest prior art:** Robust predictive quantization and #291#19's arithmetic stress test are controls. Here the legal C selector avoids states whose moment reconstruction depends on precision not available to the reader, rather than changing quantization.
- **Cheapest first test:** Enumerate integer-grid momentum with a coarser production weight read, first on a training grid and then on declared one-unit perturbations of incoming states. Compare relation matching on exact weights, the official coarse reader, and a quantized state with equal bytes.
- **Old-task retention check:** Test A across both sides of each reachable rounding boundary and after the first optimizer update on the two hardest cells.

### 16. Refuse weight credit when it only moves the bits (I; #298#13)
- **Mechanism:** Match before/after weight-read fibers up to relabelling, then ask which disagreement witnesses vanish inside those fibers. Decompose a wider win into fiber splitting and true conditional simplification, and charge useful native weight changes separately from a new identity channel.
- **Novelty vs nearest prior art:** Side-information rate accounting is standard. This audit turns #298#13's no-scratch-space condition into a paired exact test rather than treating unchanged marginal weight entropy or unchanged format as enough.
- **Cheapest first test:** Build two negative controls with the same weight histogram: one permutes membership to distinguish previously ambiguous pairs, one merely renames weight values. Compare their exact joint graphs and residual costs to a C arm with unchanged fibers and real within-fiber agreement.
- **Old-task retention check:** Check held-out A under each weight transformation and after B; require interaction with a probe sensitive to the changed weights, not just preservation on easy examples.

### 17. Hit the last odd-cycle witness only after the weight read (P; both seeds)
- **Mechanism:** Track edges with both weight-blind and weight-conditioned witnesses. Select C that removes the last **conditional** witness of a blocking edge by making demanded moment contributions agree under a shared fixed weight read. The blind cycle may survive via a different request on which the histories have different legal weight reads.
- **Novelty vs nearest prior art:** Witsenhausen's conditional graph and #298#03/#13 already supply the pieces. The candidate dispatches ordinary work against a specific remaining conditioned witness that neither the blind core nor average residual cost would choose.
- **Cheapest first test:** Find a finite host with a triangle-free odd cycle inside the lawful conditional graph, and a legal C order whose exact conditional code crosses a bit boundary while the blind graph and weight-fiber memberships do not. Compare blind-core C plus exact conditioning, residual-count C plus exact colouring, and the stacked control.
- **Old-task retention check:** Probe A on all cycle histories, including equal-weight histories with different live moments, and after the B action newly enabled by the smaller fold.

### 18. Spend a graph repair and a residual repair on the same C record (P; both seeds)
- **Mechanism:** Select a qualifying C record for its joint effect on a blocking path and on a separate moment-reconstruction ambiguity, so the pair of obligations can be met before the cut even though either independently best first choice misses the deadline.
- **Novelty vs nearest prior art:** Budgeted multiobjective scheduling and #298#19/#21 are controls. The candidate couples two concrete exact witnesses through the same ordinary update and requires a strict improvement over feasible sequential steering in either order, not two metrics improving in isolation.
- **Cheapest first test:** Enumerate a small due menu with room for one batch before the fold but all C service still due. Compare the joint one-batch selector with both single-objective selectors, all feasible sequential controls and exact conditional codes; null out one targeted effect while preserving the other.
- **Old-task retention check:** Test A after the shared batch, at the earlier cut, after the admitted B work and after the remaining C backlog is served.

### 19. Use a weight-conditioned parity certificate to release capacity before a second cut (P; both seeds)
- **Mechanism:** Certify the first cut with a fixed conditional two-colouring and let the next ordinary B update change weights. Release an additional slot at the second cut only if the surviving key still determines the next encoding using the new lawful observation, without reconstructing discarded history.
- **Novelty vs nearest prior art:** #298#07 prices colours across cuts and #298#13 reconstructs a contribution. The proposed operation earns a later refund via a transition on conditional colour classes, not two independent compressions run with access to the original checkpoints.
- **Cheapest first test:** Exhaustively check two reachable cuts of a tiny discrete host, with the second conditional graph conflict arising from a legal B weight write. Compare independently optimal codecs with paid carry, a never-release arm, and graph-only cross-cut coding.
- **Old-task retention check:** Check A after the weight write, after the second cut and after spending the refund on a real second B record, including histories sharing the first key.

### 20. Route around the obstruction with a paid late weight read (P; both seeds)
- **Mechanism:** Preserve an unconditional first answer with the small key; defer only the moment-dependent second answer to a decoder observation already delivered by the ordinary B sequence. Use due C to align the early answers that would otherwise form a non-clique obstruction. No owed answer is delayed past its original deadline.
- **Novelty vs nearest prior art:** Successive refinement and #280#12's shared prefix are controls. The candidate is an early obstruction repair targeted to what lawful late side information cannot save, not free access to the late read when choosing the early colour.
- **Cheapest first test:** Pin a two-answer route grammar with late native weight access. Compare sequential exact coding after C to early-access oracle, a priced extra early read, #298#03 against a graph built from the early observations, and a null where the first answer cannot be aligned in time.
- **Old-task retention check:** Check A between the answers, after the second answer's optimizer action, and on a route where the late read never arrives and fallback is owed.

### 21. Find the finite witness that survives every joint intervention (I; both seeds)
- **Mechanism:** Ask whether every causally selectable C order leaves a non-clique obstruction in its weight-conditioned graph. Separate one immutable obstruction from a family of orders each blocked by a different witness. Report the minimum extra paid width instead of grading a proxy.
- **Novelty vs nearest prior art:** #298#18 identifies protected variation and graph cores certify individual bounds. This joint audit certifies unusable capacity against a causal menu, even if a hindsight selector could colour each arrival separately.
- **Cheapest first test:** Enumerate two indistinguishable pre-choice arrivals needing different C policies to fit, plus one solvable arrival with a paid discriminator. Compare causal enumeration, clairvoyant enumeration and causal access to that discriminator with its byte cost.
- **Old-task retention check:** Check A on both arrivals under the same causal rule and on the fallback when the bound forces a refusal.

### 22. Demand a real write from the last rounded byte (I; both seeds)
- **Mechanism:** Translate the best exact graph and conditional residual into a declared slot format, including decoder working state and memory live at migration. Spend a saved byte on a predeclared B write before expiry or count the gain as unrealized.
- **Novelty vs nearest prior art:** #280#22 already requires spending released width. This is a kill test for the fourth-level interaction: neither raw colour count nor an isolated conditional residual estimate is usable capacity once both proofs and the native read lifetime are charged.
- **Cheapest first test:** Use a CPU ledger for one packed-slot boundary with a priced proof, weight read and decoder. Compare exact graph-only, exact conditional-only and joint policies, including one raw-bit win that fails once padding or peak memory is counted.
- **Old-task retention check:** Run the same held-out A set with and without the admitted B write, including the expiry/fallback path where no space was released.

## Ranked deeper questions

1. **Can required C remove a conditioned non-clique obstruction without changing who the weights identify?** Start with 01, 09 and 17. Require a real discrete, injective host, fixed weight fibers, unchanged clique number and a strict allocated-width or B-admission gain over the stacked policy. An exact static-code tie on the chosen state is expected; the remaining question is what the scheduler earned.
2. **Can a fixed weight-side reader keep the saving after the first ordinary optimizer step?** Start with 10–15 and 19. Reconstruct exact demanded contributions through a state-mutating B record without an old-weight snapshot, reset, widened tensor or key refresh. Use an independent-weights null and matched weight-fiber audit (16).
3. **Which obstruction evidence actually changes a causal batch decision at a useful cost?** Use 02–08 and 21. Compare witnessed selection to max-clique, per-request and edge-count policies and to exhaustive causal search in a held-out arrival menu. If the proof costs as much as exact search or the target misses the allocation boundary, there is no usable primitive.
4. **Does doing the two repairs together serve anything the best sequential stack cannot?** Use 18, 20 and 22. Pin the deadline, candidate B write, A/B/C floors and peak allocations before looking at the joint frontier. If the only win appears with a free late read, a migrated weight side channel, or after rounding away the difference, stop.
