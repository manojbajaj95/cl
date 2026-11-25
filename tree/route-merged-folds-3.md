# Route-merged folds III: train away colour barriers without resetting momentum

**Status:** Ideas only; no learner experiments or GPU work. **Parent:** [Route-merged fold successors](route-merged-folds-next.md) ([PR #291](https://github.com/manojbajaj95/cl/pull/291)). **Review seeds:** [Flood triage, row 409](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L409) on [PR #6](https://github.com/manojbajaj95/cl/pull/6) gives score 3 to [#291#13](route-merged-folds-next.md#13-change-the-confusion-graph-without-changing-the-route-frequencies-p) (train the confusion graph with mandatory C) and [#291#02](route-merged-folds-next.md#02-align-readers-by-restricting-reachability-not-resetting-momentum-p) (align readers on reachable states without resetting momentum). The inherited refinement and exception-elision cards are controls, not third-level seeds.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/idea-ledger.md). No continuous-flow invariant standing in for discrete updates, fitted Gramian score standing in for exact continuation, or gain from a simulator-defined reset. **P** marks a candidate reusable operation; **I** marks an audit or improvement. Prior-art comparisons are working hypotheses, not claims of an exhaustive search.

## What might be new?

[Witsenhausen's zero-error coding with side information](https://doi.org/10.1109/TIT.1976.1055607) prices a *given* confusion graph. Functional compression, e.g. [Orlitsky and Roche, *Coding for Computing*](https://doi.org/10.1109/ISIT.1995.550438), already distinguishes only inputs that need different function values. The candidate operation is an ordinary, required learning prefix that changes which histories demand different continuations **at the same legal reader observations**. It buys an exact colour threshold crossing, not just fewer conflicting pairs. Separately, [exact and ordinary lumpability](https://doi.org/10.2307/3215235) and minimal realization can reduce a fixed reachable system. The candidate is to *steer* the reachable set into an alignment using C, while keeping live momentum in both channels and preserving a separate old-task read. [Guarded Compression of Adam State](https://www.alphaxiv.org/abs/2611.00589) is the nearby optimizer comparison: guard compression of a given state rather than earn a different exact continuation relation by doing mandatory work.

## Contract and first gates

- Inherit the [parent contract](route-merged-folds-next.md#contract-and-first-gates). A is old-task service, B is successor service, and C is required labeled work. Pin the discrete update, admissible batch orders, legal request/arrival support **per history**, route frequencies, readers, arithmetic, horizon and expiry before comparing policies. A C order must be executable from paid causal information; it may not manipulate which request arrives, change labels, or insert dummy work. The reader consumes a truthful request, not a hidden C schedule transcript.
- Use pre-C history identities as vertices in every arm, even if two histories end in one state. For a policy π and legal observation o, `fπ(h,o)` is the complete required continuation output for history h at o, including any specified actions within the horizon. Put an edge between h and h′ if some o is legal for both and their outputs differ. Count distinct *witness observations* per edge: deleting one of several witnesses does not delete the edge. A shared legal observation here includes any paid live state actually accessible to the reader. Hold that information interface fixed in comparisons; price any explicitly varied interface separately. Compare exact colour count χ, `ceil(log₂ χ)`, allocated bytes, peak migration, evidence costs, and B admission. A colouring lower bound is not working storage until an encoder and decoder fit those budgets.
- For reachability, enumerate actual post-C states separately from the graph and from any state visible at decode. Check injectivity on the input history set in the strongest positive arm, report the number of values in each momentum slot, and compare the exact joint continuation classes with the best remaining single route. An invertible update can restrict the image to an aligned subset relative to the host state space; it cannot lower the cardinality of the input set. Distinguish that case from collisions, clipping, reset, and merely dropping a reader.
- Compare exact no-fold continuation **under each order** separately from task retention: keep precommitted A/B/C floors and match service, deadlines, width-steps and information. Check held-out A before C, after every C batch, at the cut and after every legal first sensitive read; also check after any later write that consumes the released slot. A zero-error fold can still faithfully reproduce a C policy that forgot A; that arm fails.
- **Stacked control:** best causal #280#03 nesting prefix or single-route shrinker plus exact static Witsenhausen colouring of its post-C graph, partial/full paid tags (#280#05) where implementable, and the same priced expiry. Also give that codec the candidate order: a tie there credits C selection, not a new codec. Include random eligible orders, untrained exact colouring/minimal realization, simple slot and momentum resets with retention scored, a floor-matched quantized optimizer, and a C pool that cannot move the decisive obstruction. An oracle route tag is a floor, not an implementable arm. If exhaustive equal-budget schedule plus exact codec ties, the only remaining claim is a cheaper causal selector and it must beat that search on evidence or decision cost.

## One exact paper check (not a learner result)

Five histories `0–4` and three legal reader observations with supports `{0,1,2}`, `{1,2,3}`, and `{2,3,4}`. In each support exactly one history answers `1`; the others answer `0`. Compare singleton choices `(0,2,2)` and `(0,3,2)`. Both use the same supports and have two answers per observation and five graph edges. The second choice removes edge `1–2` and adds `1–3`. The first graph has triangle `0–1–2` and is three-colourable; the second has a bipartition `{0,3,4}` / `{1,2}` and at least one edge. Exhaustive colouring thus gives `3 → 2` colours (`2 → 1` raw bits), despite no decrease in edge count or in any observation's answer count.

The two output tables are illustrative, not lawful C transitions. The check isolates a signal that local counts miss; it establishes neither a reachable learner transition nor retention, allocated-byte savings or an improvement over optimal coding of the second table.

## Idea cards

### 01. Target a colour obstruction instead of an edge count (P; #291#13)
- **Mechanism:** Before C, find a witness that rules out the available slot budget, then choose required updates that hit every witness of at least one edge in that obstruction. Allocate only after certifying a complete colouring at the target width.
- **Novelty vs nearest prior art:** Witsenhausen prices a fixed graph; #291#13 targets fewer colours. Here a failed target-width colouring supplies the next learning target, rather than rewarding all deletions equally.
- **Cheapest first test:** On a tiny quantized momentum host, compare two truthful C orders: one deletes many edges away from a triangle, the other hits a triangle edge. Demand a full two-colouring after C and compare edge-count, random and exact best-static controls.
- **Old-task retention check:** Test A on the histories incident to the targeted edge and on untouched histories, after both C orders and after each legal B request.

### 02. Buy the whole edge, not the cheapest witness (P; #291#13)
- **Mechanism:** Attach the full set of distinguishing requests to each blocking edge. Choose ordinary C work to eliminate the last surviving witness, only then spending the colour saving.
- **Novelty vs nearest prior art:** Functional compression takes the union over legal observations; the candidate batch selector plans against redundant witnesses, not the number of route-local disagreements removed.
- **Cheapest first test:** Enumerate two C records on a two-slot learner with two request variants exposing the same edge. Compare a selector that removes more witnesses but leaves that edge with one that kills it and fits the slot.
- **Old-task retention check:** Score A after each batch and both request variants; include an A example exposed by the witness the greedy arm leaves behind.

### 03. Attack a colour lower bound with no large clique (P; #291#13)
- **Mechanism:** Use a non-clique colouring obstruction to direct C against a fold that already passes all local clique checks. Target a reduction in χ without changing the largest clique.
- **Novelty vs nearest prior art:** The clique bound's weakness is textbook; the proposed learning primitive spends real updates against a global obstruction missed by per-request and max-clique selectors.
- **Cheapest first test:** Seek a five-history non-bipartite graph with clique number two, created by pinned request pairs and real continuation differences. Enumerate a two-batch menu and price three-to-two colours versus maximum-clique and nesting selectors.
- **Old-task retention check:** Include A on every cycle vertex, not just the endpoints of the deleted edge, and score it after the first B read.

### 04. Trade edges instead of insisting on monotonically deleting them (P; #291#13)
- **Mechanism:** Allow C to introduce distinctions inside an old colour class if they can be absorbed in a new colouring after a larger obstruction disappears. Treat recolouring and its peak memory as part of the purchase.
- **Novelty vs nearest prior art:** Dynamic graph colouring handles exogenous insertions and deletions; the candidate is choosing ordinary learning updates that induce a cheaper recolouring even when monotone edge deletion cannot.
- **Cheapest first test:** Find two legal orders on six histories, one only deleting edges but preserving χ and one adding at least one edge while crossing the target bit boundary. Compare monotone and exact static stacks.
- **Old-task retention check:** Check A both on newly separated histories and on newly shared codes, through each legal B read and any migration.

### 05. Train a smaller code without changing any observation's output count (P; #291#13)
- **Mechanism:** Target which histories share an output within each observation, not how many outputs it has. Align these local groupings across overlapping observations while keeping the full legal support fixed.
- **Novelty vs nearest prior art:** Per-observation rate and single-route quotients miss incompatibilities between groupings. Unlike #291#01's global partition nesting target, this requires savings with the same local cardinalities and need not produce a finest reader.
- **Cheapest first test:** On a finite two-feature host, enumerate allowed C orders and compare two post-C graphs with identical per-observation class counts but different rounded exact code widths. Compare exact single-route shrinkage plus post-C colouring.
- **Old-task retention check:** Include A from each reassigned group and evaluate it at every observation shared by two formerly conflicting histories.

### 06. Make two independent ingress points reuse a codebook (P; #291#13)
- **Mechanism:** Generate local exact palettes at two ingestion sites and pay C to make the required identification of shared histories consistent across them, so a single compiled encoder can write to either site without a schema selector.
- **Novelty vs nearest prior art:** Distributed source coding and graph precolouring extension already model shared labels; the new action is altering the demand for those labels via required updates under a fixed cross-site encoder interface.
- **Cheapest first test:** Use two sites with overlapping history support and one fixed serializer; compare independent codecs plus a paid selector, unrestricted global colouring, and selecting C for extension of the current palette. Claim improvement only if a deployment cost falls.
- **Old-task retention check:** Test A on all overlap histories using both sites' reads, and on histories legal at only one site; keep the same B/C deadlines.

### 07. Price a colour that must survive the next service cut (P; #291#13)
- **Mechanism:** Target compatibility of colour assignments across two cuts when the later encoder can see only the earlier code and new truthful inputs, not the original history. Choose the first C prefix to make an exact no-recovery handoff possible.
- **Novelty vs nearest prior art:** Streaming functional compression imposes causal encoders, and #291#05 asks a fixed finest route to survive a suffix. The new target is a legal *change* of overlapping-observation palette without recovering erased history.
- **Cheapest first test:** Exhaustively enumerate two-cut encoders for a four-history learner and two C arrivals. Look for orders with equal per-cut χ but different minimum live bytes under the causal transition; compare independent colourings with charged carry state.
- **Old-task retention check:** Evaluate A before the first cut, between cuts and through the later reader that exposes an invalid carry.

### 08. Lower the graph under a pinned retirement order for stored bits (P; #291#13)
- **Mechanism:** When the allocator releases one bank before another, require a long-lived coarse code shared by all later readers and a temporary refinement for near readers. C targets a factorization into those two levels, not the minimum one-shot width.
- **Novelty vs nearest prior art:** Successive refinement and the parent lease already price tiers and horizons. The distinct operation is learning into a prescribed physical code projection with overlapping lawful observations at each tier.
- **Cheapest first test:** Enumerate nested one-bit projections on six histories under two C orders; compare unrestricted exact palettes plus re-encoding, simultaneous lease expiry, and the best independent short/long codes at equal peak bytes.
- **Old-task retention check:** Test A after the early bank is reclaimed, after the replacement B write, and on the late request that would need the retired bit in the null arm.

### 09. Train the graph away from decoder-table growth (P; #291#13)
- **Mechanism:** Choose C to align conflict structure with a pinned low-cost decoder family, such as one affine bit projection per request, rather than relying on arbitrary tables that may exceed the saving.
- **Novelty vs nearest prior art:** Structured codes trade code size for decoder complexity; here mandatory learning changes which small structured decoder is realizable, with exact colouring serving as the payload floor.
- **Cheapest first test:** Enumerate all affine binary encoders on three quantized state bits and lawful C prefixes. Compare equal-χ graphs where only one admits the affordable decoder; charge table and schema bytes to the unrestricted arm.
- **Old-task retention check:** Exercise A at inputs outside the high-traffic decoder rows, including every legal rare observation in the small host.

### 10. Keep the same colour budget through a witnessed ambiguity (P; #291#13)
- **Mechanism:** If the same declared request may arrive intact or missing an optional field, find C work that makes the degraded mode safe within the same slot, without influencing which mode occurs or encoding a replacement field.
- **Novelty vs nearest prior art:** Complementary/degraded side-information coding treats the weaker observation as a fixed constraint. This targets exact learning of the output equalities the weaker mode needs, not #291#14's removal of variants from an exception block.
- **Cheapest first test:** Pin intact and missing-field cases before enumerating two ordinary C orders on a two-moment host. Use exact colouring of the combined graph, a separately paid backup and an immutable degraded graph as controls.
- **Old-task retention check:** Check A after both receipt modes, including rare old histories distinguishable only by the missing field before C.

### 11. Move the reachable line by a reversible update order (P; #291#02)
- **Mechanism:** Use an order of full-rank, nonsingular C updates whose composition rotates or shears the reachable set into a relation on which a fixed reader determines another. Retain both nonconstant momentum coordinates at the cut.
- **Novelty vs nearest prior art:** Minimal realization and order-dependent SGD give the ingredients; the claimed operation selects an invertible order for alignment of a fixed read interface rather than learning a projection or lowering rank of the update.
- **Cheapest first test:** Enumerate two noncommuting squared-loss batches with fixed momentum on a low-rank but nontrivial incoming state family. Require a strictly smaller joint quotient than the reversed order with equal state count and compare slot reset, untrained minimal realization and random order.
- **Old-task retention check:** Include old probes that read both live directions and intermediate states; require lawful B/C floors so flattening learner output cannot pass.

### 12. Make a sensor collision harmless using a curved reachable set (P; #291#02)
- **Mechanism:** Use ordinary nonlinear C updates to bend the reachable state set so histories with equal output of one fixed reader also agree for another, while retaining distinctions along the curved set for A.
- **Novelty vs nearest prior art:** Nonlinear observability checks a given reachable manifold; the candidate steers it into a functional dependence that no matched linear update on the same host earns.
- **Cheapest first test:** Enumerate a quantized two-feature piecewise-linear learner on six histories and a two-record C menu. Compare all legal orders, matched linearized updates and equal-byte nonlinear static coding. Reject if the effect vanishes without a hard clipping boundary.
- **Old-task retention check:** Probe A on both sides of each activation boundary and after a B read on each branch, including histories sharing the cheap reader's output.

### 13. Use the weight–moment relation instead of storing a correction (P; #291#02)
- **Mechanism:** Choose C to couple live weights and moments so a fixed reader can reconstruct its demanded moment contribution from a lawful preexisting weight read and a smaller folded key. Do not widen or reserialize the weight bank as scratch storage.
- **Novelty vs nearest prior art:** Conditional compression already uses weights as side information; the claim is that required C builds a predictable weight–moment relation without sacrificing the weights' original function or merely moving bits into unused precision.
- **Cheapest first test:** Enumerate a two-weight momentum model with a pinned weight format and A-visible predictions; compare exact conditional coding before and after C, a matched explicit residual, and rounding weights to the predeclared A-visible precision.
- **Old-task retention check:** Check held-out A before and after C, and after the first ordinary update that consumes the reconstructed moment, with test inputs that expose either weight shifting.

### 14. Steer the common source of two alternating readers (P; #291#02)
- **Mechanism:** Target an invariant relation of the *composition* of two actual reader-triggered optimizer transitions. The state may leave that relation after either individual transition; the fixed contract still exacts the intermediate read and allows folding only at the declared boundary.
- **Novelty vs nearest prior art:** Lifted periodic realizations and the parent suffix-closure card are controls. The change is using C to land in a cheaper recurrent image at actual fold boundaries without requiring per-step invariant alignment.
- **Cheapest first test:** In a two-route alternating fixture with both phases pinned, compare enumerated C landings and exact phase-aware coding of untrained states. Count intermediate peak bytes and include mixed phase starts if legal.
- **Old-task retention check:** Test A at both phases, especially the off-relation intermediate state, and after a second complete cycle.

### 15. Buy a finite common continuation by synchronizing only the observable phase (P; #291#02)
- **Mechanism:** Select ordinary C updates that align the phase of two reader trajectories without coalescing their full states. The fold keeps a phase key only if the readers need no other varying component inside the paid horizon.
- **Novelty vs nearest prior art:** Synchronizing automata merge full states, and #291#16 substitutes a bounded common state. The candidate instead preserves distinct learner states and synchronizes the trajectories' observable phase, with no uncharged time reference.
- **Cheapest first test:** Enumerate a small finite optimizer with a pinned alternating batch menu; compare exact phase-key continuation to full-state synchronizing prefixes, a paid phase field and no-fold replay, including a one-step horizon extension that distinguishes the states.
- **Old-task retention check:** Test A on states of equal phase but different momentum at each phase and at the declared expiry/fallback.

### 16. Keep separate reachable charts but a single reader law (P; #291#02)
- **Mechanism:** Use C to make the same fixed functional dependence hold on disconnected components of the reachable set. Components remain distinct in raw state, but the fold does not store a chart index if all legal reads agree wherever their keys collide.
- **Novelty vs nearest prior art:** A mixture of local models generally pays a gate. Unlike learning a finest partition independently in each component, this targets compatibility at overlapping keys across remote parts of state space.
- **Cheapest first test:** Start a two-slot learner from two separated checkpoint sets; enumerate one common C prefix and compare a shared decoder with per-component codecs plus paid gate and with exact static joint realization.
- **Old-task retention check:** Run A on both checkpoint sets and on pairs straddling the components with the same fold key; no averaging away a component's failure.

### 17. Transport an earned relation across an ordinary parameter rebalance (P; #291#02)
- **Mechanism:** When a pinned host periodically rescales equivalent parameterizations, choose C to earn reader alignment in both coordinate charts, transporting moment contributions by the actual optimizer rule rather than assuming functional reparameterization is invisible to dynamics.
- **Novelty vs nearest prior art:** Gauge-equivariant optimization and reparameterization already supply change-of-coordinate rules. The candidate is a smaller *exact fold* across a scheduled rebalance; the ledger's Noether failure makes a gradient-flow argument insufficient.
- **Cheapest first test:** Enumerate two C orders on a two-factor linear predictor with a fixed rational rescale and momentum rule. Compare matching trained and untrained codec costs, a fresh reset after rescale and an uncharged gauge-oracle floor.
- **Old-task retention check:** Score A before rebalancing, immediately after it, and after the next momentum-sensitive B step; prediction equality at the rebalance alone does not pass.

### 18. Mark which incoming variation can never be aligned (I; #291#02)
- **Mechanism:** Before scheduling, propagate a state-difference witness through every admissible C action. If a fixed candidate key always aliases the pair and a second legal reader always separates it, rule out that key for this menu.
- **Novelty vs nearest prior art:** Controlled invariance and #280#04 already give no-go tests. This version isolates protected incoming variation under mandatory updates; it is a falsifier, not a new compression primitive or a learned observability predictor.
- **Cheapest first test:** Exhaustively propagate two differences through a two-batch menu, one in a C-inaccessible channel and one C can mix into the alignment. Verify the proof against direct state enumeration and require it not to falsely exclude the movable case.
- **Old-task retention check:** Select A examples that detect erasure of the protected variation; compare any apparent success from resetting it against those same A probes.

### 19. Learn cross-history agreement without changing a public signal's joint law (P; both seeds)
- **Mechanism:** Move the reachable state geometry so output classes agree on overlaps at a fixed truthful signal, even though a small tagless code still cannot serve every reader. Keep the full history/request incidence matrix unchanged, not only aggregate route frequencies.
- **Novelty vs nearest prior art:** #291#02 rewards global reader dependence and #291#13 rewards lower χ. This is an interaction target: learn *conditional* agreement that crosses a colour threshold but cannot be explained by tagless alignment or arrival selection.
- **Cheapest first test:** Enumerate a two-slot learner with three fixed partially overlapping request supports and a two-batch menu. Demand injective C, equal tagless class count, fewer priced colours, and a strict byte or B-admission gain over the nesting-first plus exact-colouring stack.
- **Old-task retention check:** Check A on both sides of every overlap and at private-to-one-request histories; include a signed reader that uses the retained momentum direction.

### 20. Aim for a common colour certificate across real arrival envelopes (P; both seeds)
- **Mechanism:** Choose C so one fixed encoder works in either of two legal future environments whose support is known but whose realized case the encoder cannot observe. For disjoint public observation alphabets, certify a colouring of the union graph without exposing the environment to the encoder. With shared observations, build the graph over combined supports and veto any conflicting output for the same history and observation.
- **Novelty vs nearest prior art:** Universal coding and #291#08's robust refinement corridor are controls. The proposed operation aligns the reachable images against the *union* obstruction rather than buying each cheap but incompatible per-environment code.
- **Cheapest first test:** Pin two request envelopes with disjoint observation alphabets whose individual graphs are bipartite but whose union is not; seek C orders that make the union two-colourable without dropping one legal observation. Compare separate codecs and a paid environment selector where lawful.
- **Old-task retention check:** Evaluate A on each envelope, especially histories legal at their overlap and the worst branch of the schedule chosen without knowing the envelope.

### 21. Find schedules whose effect on code cost reverses between the two seeds (I; both seeds)
- **Mechanism:** Preregister a matched schedule pair and compute an exact frontier with two separate objectives: tagless joint classes and legal-observation colour count. Look for order reversals rather than treating one count as a proxy for the other.
- **Novelty vs nearest prior art:** Confusion graphs and exact quotients are known; the proposed falsifier exposes when a nesting-first or graph-first selector cannot substitute for the other, rather than merging two metrics into one score.
- **Cheapest first test:** Enumerate all feasible orders of three truthful records on a finite host with partially overlapping readers. Compare the exact best schedule for each objective and an exhaustive Pareto baseline once, with byte prices and B demand fixed before enumeration.
- **Old-task retention check:** Compare frontiers only among schedules that pass all A checkpoints at matched B/C service; report the history of the largest A loss separately on each frontier.

### 22. Reject savings bought with training evidence too wide to keep (I; both seeds)
- **Mechanism:** Run the obstruction-aware and reachable-set selectors with fixed budgets for causal probes and temporary certificate state. Permit fallback to the best static code when the learner cannot certify the proposed purchase within the budget.
- **Novelty vs nearest prior art:** #269 already prices receipts and live memory. This is the weakest-link test for this pair of seeds: distinguish an implementable selector from exhaustive hindsight colouring or a stored replay of the incoming histories.
- **Cheapest first test:** On the smallest positive host, enumerate legal selectors given one predeclared causal summary; compare full-information search as a floor, direct continuation verification, and static exact colouring, including peak verifier and decoder allocations.
- **Old-task retention check:** Test A on both the fallback and purchased arms after the same service deadlines, including histories the summary aliases and any later B write enabled by the purchase.

## Ranked deeper questions

1. **Can mandatory C make the exact code fit without a reset, a smaller single-route quotient, or a changed request law?** Start with 01–05, 11 and 19. Look for a real discrete host with an injective winning C prefix and a lower graph colour budget at fixed legal support, even though the tagless quotient is unchanged. Demand a strict physical saving or new B admission against the nesting-first plus exact-code stack at matched A/B/C retention. If only the graph calculator looks better, stop.
2. **What is the weakest reachable-state relation that gives durable savings without relying on collisions?** Use 11–18. Require a matched invertible positive case and a protected-variation null, both with momentum exposed to old probes. Separate a genuinely learned relation from arithmetic clipping, a public-weight side channel or exact minimization of a system that was small all along.
3. **Do graph-directed schedules remain useful when the fold must continue from its own compressed state?** Use 06–10 and 20. Require legal encoding at two successive cuts without access to erased history; compare the peak and expiry costs with independent static codecs and paid carry. A graph that is cheap only with hindsight or a large decoder table is not a write primitive.
4. **Can an affordable causal selector approach the exhaustive frontier, and where should it refuse?** Use 03, 18, 21 and 22. Preregister one held-out arrival menu, a bit/byte boundary and a B write; compare the selected actions against the full frontier and equal-budget static controls. Treat ties as evidence against the stronger interaction claim, not as partial wins.
