# Optimizer-slot splits: can forgetting begin before the model changes?

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Irreversible split points](irreversible-splits.md) ([PR #172](https://github.com/manojbajaj95/cl/pull/172)). **Seeds:** [Flood triage row 273](https://github.com/manojbajaj95/cl/blob/c80397b27734310db586a200d8644b520a9a4ca1/reviews/flood-triage.md#L273) scores parent cards 03 (slot-only split) and 09 (move the model or refine the verifier) at 3. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/f3dbc1cf3d7dc26e99fc657d0f2d19079e521dd6/reviews/idea-ledger.md). Match margins and useful new learning, reject effects true by construction, and make a combined method beat the best controls for its parts run together. Every first test includes old-task service after the new work.

## Is optimizer state a new continual-learning object?

**No as a hidden carrier; possibly yes as a reusable intervention boundary.** [Momentum fossils (PR #136)](https://github.com/manojbajaj95/cl/pull/136) already swaps slots onto common weights, so equal logits and first gradients are free. [Delayed-release edits (PR #141)](https://github.com/manojbajaj95/cl/pull/141) already writes to slots for a later behavioral effect; [PR #109](https://github.com/manojbajaj95/cl/pull/109) warns that a writable gauge quantity need not protect anything. [Matched Specialization, Different Adaptation](https://arxiv.org/abs/2610.15830) reports second-moment swaps and prospective gradient shaping changing later adaptation under matched readouts, including effects beyond overall step scale. [Stored in Optimizer State, Valued by Later Training](https://arxiv.org/abs/2608.20442) gives causal slot mediation for subliminal transfer; [Delayed Optimizer-State Transport](https://arxiv.org/abs/2608.24593) already beats immediate-response scoring for short, committed future minibatch paths. [Optimizer resetting](https://arxiv.org/abs/2306.17833), [STABLE](https://arxiv.org/abs/2611.10655), and [GPM](https://arxiv.org/abs/2103.09762) give cheap rivals: reset contaminated moments, bound drift, or project the update.

The candidate is an **edit-conditioned split contract**: on a declared slice of optimizer state, give a checked boundary for a future old-task failure, the last opportunity to make a bounded repair that preserves today's function, and the conditions under which an independent editor can reuse that repair or, if the split is only epistemic, reuse a proof. Neither [reachability](https://arxiv.org/abs/1709.07523) on a larger state space nor [regression CEGAR](https://arxiv.org/abs/1806.04829) with cached summaries is new. [Neural proof sharing](https://arxiv.org/abs/2608.19351) is a direct control, including its reuse overhead. Primitive status requires admitting more useful blind edits or reducing total intervention and checking work at the same retention, relative to a full-state rollout/repair and reusable verifier stack. A better timestamp, regression score, or cache hit rate alone is an improvement.

### Two boundaries, three clocks

Freeze the source and substitute starting states, the refused edit payload, the legal family of future batches/schedules, the available witness actions, their timing and budget, and old-task floors. Use trainer state `z = (θ, m, v, k, ξ)`, with `k` the Adam clock and `ξ` all other continuation-relevant state (e.g. sampler, schedule, normalization, precision). At a purported *slot-only* checkpoint require equal `θ, k, ξ` and inferred logits, not just equal accuracy. A common next batch then gives the same gradient if the loss does not read slots. Require a stronger, separately reported control that also matches the **vector** of realized weight updates on a specified immediate probe, not just its norm. That equivalence is probe-specific; it need not survive arbitrary next batches.

- **Dynamical:** Pull a later gate sign and old-task service floor back through the frozen future dynamics into the current `(m,v)` slice. On one fixed continuation this is a path-specific preimage, not necessarily an invariant basin boundary; for a bounded continuation family keep possible failure and guaranteed safety separate. Record the earliest observed slot separation `t_slot`, the first actual gate flip `t_flip`, and the last feasible repair time `t_last` under the declared actions and budgets. A first observed separation is not proof of a transition from the same side; log earlier prefixes and report left censoring. Do not infer `t_last` or irreversibility from a gate flip. Enumerate feasible repair times on tiny oracles; if opportunities reopen, report the feasible set, not a binary-searched cliff.
- **Causal test:** At the same complete checkpoint, exchange `m`, `v`, and both factorially, then replay the same continuation and edit in both directions. Check that the gate and old-task outcome move with the targeted slots and that a lawful early witness can reproduce the benefit. A surgical write can identify the carrier even when it is not a legal training intervention. An equal first gradient is not an intervention, and a sampled successful path is not a safety proof.
- **Verifier-only:** For a fixed obligation and continuation set, exact verification says the edit is safe, but the cheap sound checker returns **unknown** after losing a dependency. Let `t_v` denote that first unresolved straddle, not `t_slot` or `t_last`. On an exact toy universe exhaust every legal continuation (or use an exact symbolic bound); when neither true safety nor failure is established, label it *unresolved*, not verifier-only. A proof refinement cannot fix a real failure. A state move must be rechecked and must not change the edit's intended result.

### Paper witness: identical weights and one Adam response, different delayed gate

Take scalar bias-corrected Adam with `β₁ = β₂ = 1/2`, `η = ε = 1`, no weight decay, and update count `k`. A slot update gives `m⁺ = (m+g)/2`, `v⁺ = (v+g²)/2`, then subtracts `[m⁺/(1−2^(−k⁺))] / [√(v⁺/(1−2^(−k⁺)))+1]` from `w`, where `k⁺` is the incremented update count. Use injected shadow checkpoints at `k=1`: both have `w=5/8`, source `(m,v)=(9/8,6)`, substitute `(3/4,3/2)`. These are state interventions, not a claim that these tuples arose from one Adam step from zeros.

| Event | Source | Substitute |
| --- | --- | --- |
| Common zero-gradient batch (not a skipped update), `k=2` | `(m,v)=(9/16,3)`, subtract `1/4` | `(m,v)=(3/8,3/4)`, subtract `1/4` |
| Now `w=3/8` on both; common `g=1` pulse, `k=3` | Subtract `(25/28)/(1+4/√7) < 3/8` | Subtract `11/28 > 3/8` |

The gate boundary pulled back to the matched-weight slice at `k=2` is `[4(m+1)/7] / [1+√(4(v+1)/7)] = 3/8`. The two slot tuples lie on opposite sides even though the full preceding weight update was identical. This does not reveal when the two injected histories first separated.

Use a rescue route `ReLU(w)` and an old-task fallback that serves A before the edit. The identical frozen edit removes the fallback after the pulse; it is safe on the source and leaves the substitute with a dead route. For example, an A-positive score of `fallback + x·ReLU(w)` on `x ∈ [1,2]` clears a `1/100` floor on the source after removal, not on the substitute. A second old task C has an independent protected readout. At `k=2`, transplant only the source's `v=3` into the substitute: the pulse now subtracts `(11/14)/(1+4/√7)`, preserving the route without changing current logits. A slot-only write after the pulse cannot change the outcome **if no remaining weight update is allowed before the read**. This is a separation with a finite action deadline, not a demonstration of permanent death, a naturally reachable pair, or a cliff in realistic training. The gradient pulse can be supplied by an independent current-task loss on the shared coordinate. A leaky rescue, redundant old paths, or an extra recovery step can undo this construction's conclusion.

### Paper pricing game: one rare straddle or six repeated ones

For a verifier-only toy, let a reachable gate have preactivation `m − x + h`, with `x ∈ [0,1]`, `m=x+s`, `s ∈ [1/8,1/4]`, and `h=0`. The actual gate is always on; independent intervals give `[-7/8,5/4]`. Two valid proposals:

- **Move (M):** Spend a truthful calibration example. In this toy, a separate legal one-step squared-loss update on bias `h` toward a true target `1` with unit step gives `h=1`, so the cheap interval lower bound is `1/8`. This arm pays for data and a training step, plus checks that changing the bias kept all old floors and the frozen edit's utility.
- **Refine (R):** Keep training untouched. Prove the relational bound `m−x≥1/8` once, then revalidate its premises for each edit's reachable tube. Six out of ten independently submitted edits may use the same refinement, but sharing a gate identifier is not evidence that six tubes satisfy its premises.

Illustrative accounting in arbitrary units: if M costs 3 **per independent edit** and R costs 8 up front plus 1 per use, M wins for one and R wins for six (18 vs. 14); they tie at four. Those prices are not measurements. A persistent move may also help many edits: charge it once when sound, and account for side effects, invalidation and rechecks on **both** sides. Run isolated forks for the simple accounting check and a persistent stream for the real comparison. Use hard ceilings for peak bytes, edit delay and exact retention/utility obligations; under those ceilings compare useful admissions, total FLOPs and bytes moved, with a preregistered FLOPs-plus-bytes price as a secondary view. Charge truthful-example acquisition/storage, optimizer writes, refined artifacts, validation, rejected quotes and fallback checks. Never trade a retention violation for a cheaper proof. Compare pure movement/certified training, pure CEGAR **with** reuse, per-edit exact checks where feasible, and a stacked policy running both with a simple break-even rule; report the offline oracle separately from online policies that cannot see future arrivals.

### Shared CPU protocol for the cards

Use the above as algebraic controls, then propose a tiny CPU Adam MLP with independent old task slices A/C and a disjoint current B stream; train first, freeze edits before analysis, fit boundaries/repairs/refinements on development histories only, and reveal held-out edit families, histories and suffixes afterward. Include ordinary continuations, same-task continuation, harmless slot variation, smooth or leaky gates, and a deliberately changed verifier premise. Measure held-out A/C before intervention, immediately after each committed action and after unassisted B continuation; report worst checkpoint and worst old slice as well as average. Match per-item starting margins, B progress, frozen edit utility, information and action/query bytes; report gate sign as mechanism evidence, never as an old-task substitute. Count horizon, verifier strength and proof scope explicitly. In addition to the strongest card-specific control, include weight-only bisection, [state matching (PR #114)](https://github.com/manojbajaj95/cl/pull/114), [momentum fossils](https://github.com/manojbajaj95/cl/pull/136), reset, matched update vector on the immediate probe, short full-state rollout, projected replay, and matched-work direct checks where applicable. Planting a split only establishes a positive control; look for natural incidence and a nondegenerate null before claiming anything.

## Idea cards

**P** = candidate primitive only if its object transfers or improves the attainable retention/utility/cost frontier; **I** = new use, diagnostic or optimization of a known object. The first tests below are proposals, not results. A/C always mean independent old behavioral suites, not examples used to fit a witness.

### A. Discover and repair the silent split

#### 01. One-response-equivalent risk boundary (P)
- **Mechanism:** Map the safe side of a future gate within the level set of an identical present weight and next-update vector; return the smallest crossing witnessed by a future B batch plus frozen edit.
- **Novelty / control:** Fossils and second-moment exchange identify hidden history; compare to one-step state matching and eight-step full-state transport at equal queries. The candidate is a *reusable separating surface*, not a delayed response.
- **First CPU test:** Fit on one small Adam gate with exact matched pairs and two pulse types; predict held-out pulse/edit pairs without refitting. Include unplanted, naturally trained endpoints.
- **Retention:** At equal B gain, require independent A/C at the post-edit switch and after clean B continuation, including features outside the fitted gate.

#### 02. Minimum two-sided slot splice (P)
- **Mechanism:** Find the cheapest legal block rewrite that makes the substitute safe and the reverse diagnostic transfer makes the source unsafe; spare the rest of the optimizer state.
- **Novelty / control:** Adam resets and Takahashi's `v` exchange already mediate effects. The candidate carries a portable, causal minimal block plus a use condition; compare full swap, uniform reset and norm-matched block dampening.
- **First CPU test:** Exhaust subsets of four slot blocks in a tiny Adam MLP; score a mask on a blind second editor and include a planted decoy block with greater moment norm.
- **Retention:** Require rescue of the failing rare A slice and no loss on unaffected A/C after both useful edits; log the intentionally unsafe reverse transfer only in shadow.

#### 03. Slot-only witness from phased gradient cancellation (P)
- **Mechanism:** Use two truthful minibatches whose net weight effect cancels at the intervention boundary but leaves a useful `(m,v)` change; constrain intermediate behavior too.
- **Novelty / control:** Delayed-release edits, gradient matching and [matching training trajectories (MTT)](https://arxiv.org/abs/2203.11932) can create persistent effects. The candidate is a repeatable sample-only actuator on the dangerous quotient; compare same two batches in reverse, two-step MTT and direct slot write.
- **First CPU test:** Search a tiny labeled sample pool and two legal learning rates for matched endpoint weights; test one held-out pulse. Discard approximate pairs if their residual drift alone predicts the result.
- **Retention:** Audit A/C at both intermediate steps, at the edit and after B; match B improvement rather than crediting cancellation for doing no work.

#### 04. Repairability map with holes (I)
- **Mechanism:** Record feasible intervention times and at each time the cost/action set, rather than forcing a single cutoff when an optimizer slot resets or a later gradient reopens the route.
- **Novelty / control:** Extends the parent split diagnostic and [smooth replay deadlines (PR #113)](https://github.com/manojbajaj95/cl/pull/113); exact scheduling and prefix enumeration already represent holes.
- **First CPU test:** Enumerate one truthful action over six event times in an Adam toy with a scheduled reset and compare to bisection, earliest action and the exact oracle.
- **Retention:** A time is feasible only if the frozen edit meets utility and every A/C floor through the rest of the sequence.

#### 05. Steering one gate without evicting its neighbor (P)
- **Mechanism:** Repair `v` to block an A-threatening update while explicitly preserving a second slot-mediated adaptation needed to keep C available after the next write.
- **Novelty / control:** GPM and STABLE protect outputs or update directions. The candidate is a joint *future response* contract even when both old tasks look fine now; compare multi-task full-state constrained repair and matched drift/projection.
- **First CPU test:** Use two gates sharing a parameter block, one with a benign slot effect plus a harmful one; compare joint selection to greedy per-gate resets on a withheld suffix.
- **Retention:** Score rare A and C separately after each update and require unchanged B learning; a rescue accompanied by C loss fails.

#### 06. First naturally occupied silent boundary (I)
- **Mechanism:** Locate slot frontier occupancy in ordinary training prefixes, then use same-weight transplants only to test causality, not to estimate natural prevalence.
- **Novelty / control:** [First-point-of-loss (PR #134)](https://github.com/manojbajaj95/cl/pull/134) and fossils already locate and test hidden transport; the improvement is separating natural incidence from intervention-only possibility.
- **First CPU test:** Collect A→B and same-task histories with shared starts, search matched or near-matched weight/response checkpoints, and bound how much any residual weight drift can move the gate. Report exact-pair incidence separately.
- **Retention:** Check whether discovered events precede actual A/C slice failures on untouched histories and whether a blind repair prevents them at matched B.

#### 07. An early-warning batch that never commits (I)
- **Mechanism:** Ask for a legal shadow pulse selected to distinguish near-identical states on opposite sides of a certified later gate boundary; discard all shadow writes.
- **Novelty / control:** Active diagnosis and optimizer transport already use informative inputs. Compare the pulse with random legal batches, largest-gradient pulse, and a short direct rollout at equal queries.
- **First CPU test:** Choose one pulse from an enumerated B library; report detection gain over matched one-step response controls and charge selection as well as execution.
- **Retention:** Run the subsequent accepted edit on a clean clone; score A/C after the resulting repair, not after the noncommitted shadow pulse.

#### 08. A proof of which slot bits cannot matter (P)
- **Mechanism:** Define a bounded-horizon equivalence on slot states that preserves both gate outcomes and available safe repair responses; store representatives only for classes that can be distinguished by a legal edit.
- **Novelty / control:** Partition refinement and [correction classes (PR #169)](https://github.com/manojbajaj95/cl/pull/169) are known. Contrast with equal-bit optimizer quantization, full-state exact partitioning, and memoized direct checking.
- **First CPU test:** Exhaust a quantized two-coordinate state grid and three legal actions; learn a compact candidate quotient on one stream and challenge it with a held-out edit family.
- **Retention:** After replacing full slots by representatives, test A/C on every legal toy suffix plus independent continuous held-out inputs; expose any quotient alias that hides rare loss.

#### 09. A boundary packaged for the next optimizer (P)
- **Mechanism:** Transport a certified safe intervention and its gate-relevant transition relation across an optimizer or schedule handoff, permitting only translations that simulate the declared continuation outcomes.
- **Novelty / control:** Slot transfer and response matching are known. A reusable cross-optimizer behavioral certificate would matter only beyond reset, calibrated step matching and fresh certificate synthesis at equal cost.
- **First CPU test:** Adam-to-Adam map across two `β₂` schedules in a two-gate host; add one schedule hop where no translation exists and require refusal rather than approximate proof reuse.
- **Retention:** Score A/C under both supported schedules after the same useful B edits, including the first post-handoff burst.

#### 10. Retire the source but keep its warning (P)
- **Mechanism:** Compress a source's safe slot-response region into a small checked witness, delete the teacher/slot bank, then apply the witness to blind requests without reconstructing the source.
- **Novelty / control:** [Training readers (PR #161)](https://github.com/manojbajaj95/cl/pull/161), [witness examples (PR #163)](https://github.com/manojbajaj95/cl/pull/163) and MTT already target retirement. The boundary summary must beat those plus exact retirement accounting, equal-byte replay and compressed slot snapshots.
- **First CPU test:** Keep one witness for two early gates, truly reuse the source's allocation for unrelated B work, and evaluate blind editors with and without an observed hazard.
- **Retention:** Score A/C after reuse and after every blind edit without source queries, hidden rollback storage or recovery training.

#### 11. Counterfactual slot editor's warranty (P)
- **Mechanism:** Publish a limited menu of certified slot corrections whose future obligations are conditional on a later editor's declared batch family; new editors may choose a correction without sharing payload data.
- **Novelty / control:** [Finite edit guards (PR #164)](https://github.com/manojbajaj95/cl/pull/164), safety games and robust control already offer safe action sets. Test whether slot specialization reduces work versus full-state finite guards plus rollout and constrained repair.
- **First CPU test:** Build a menu of two individually useful corrections exposing different future failure directions; choose against a withheld family and test a deliberately out-of-menu family.
- **Retention:** Require A/C service on each supported realized branch and measure abstentions; rejected branches do not count as retained useful edits.

#### 12. Separate the clock, the denominator and the rounding event (I)
- **Mechanism:** Replay the same slot discrepancy as full precision, deployed precision, corrected-time mismatch only and moments-only. Locate whether the first separation is representational, numerical or genuinely due to Adam history.
- **Novelty / control:** [Guarded optimizer-state compression](https://arxiv.org/abs/2611.00589) models moment reconstruction error; the improvement is attributing a later *behavioral* split rather than diagnosing update error.
- **First CPU test:** Quantize a borderline pair, lock the schedule and compare m/v/time and precision swaps against exact or high-precision shadow.
- **Retention:** After the same B update and edit, compare worst-slice A/C for every deployed arm; do not credit a high-precision result absent in the deployed numerics.

### B. Price movement versus reusable proof

#### 13. A refinement with multiple independent buyers (I)
- **Mechanism:** Compile one relational constraint when its validated reuse beats moving each tube; allow a persistent move to earn the same reuse credit.
- **Novelty / control:** Regression CEGAR and neural proof sharing already reuse artifacts. The improvement is a live comparison with training under a common admission and resource budget, not a novel cache.
- **First CPU test:** Use ten frozen edits, six sharing a straddle and at least one decoy sharing only the gate name. Compare the toy amounts to measured CPU work in isolated forks and persistent orderings.
- **Retention:** Recheck A/C after each admitted edit and the following B step; count false admissions, unresolved jobs and utility, not just verifier wins.

#### 14. Cheap premise checks instead of expensive proof replay (P)
- **Mechanism:** Publish a checked refinement with a weaker reusable entry predicate on training-state tubes; revalidate that predicate, transition semantics and task property, not the complete derivation.
- **Novelty / control:** Regression CEGAR procedure summaries and [certificate entry ports (PR #171)](https://github.com/manojbajaj95/cl/pull/171) already offer entry-based reuse. A training-state instance earns credit only for faster safe reuse against strongest summary caching and exact premise implication.
- **First CPU test:** Submit a fresh edit with the same gate and enlarged `v` range, one still implying the predicate and one not; compare hit validation cost to solver warm start and checking from scratch.
- **Retention:** Run A/C after admitted hits and after fresh proofs for misses; the invalid hit must be refused in shadow even if its observed A/C sample happens to pass.

#### 15. Move into an existing proof, then stop moving (P)
- **Mechanism:** Train a truthful, behavior-preserving correction that makes a tube satisfy an existing refinement's premise, instead of either moving far enough for a weak verifier or generating a wholly new proof.
- **Novelty / control:** Interval-bound training and [return corridors (PR #168)](https://github.com/manojbajaj95/cl/pull/168) already train toward certifiable regions. The distinct candidate is partial movement plus a paid certificate entry; compare full M, full R, sequential M+R and joint exact search.
- **First CPU test:** Construct two edits just outside a stored relational predicate yet far from interval clearance; sweep discrete truthful example costs and count the set admitted at the same compute and bytes.
- **Retention:** A/C must pass immediately after the move, after the edit and after subsequent B, with the original frozen-payload utility unchanged.

#### 16. Known-proof-preserving optimizer splice (P)
- **Mechanism:** Choose an early slot repair that changes the genuine risky gate while provably keeping a second already-cached refinement applicable to unrelated edits.
- **Novelty / control:** Incremental verification and constrained repair handle proof invalidation separately. The candidate is a joint slot-write/validity contract; compare optimized slot repair followed by best incremental recheck, with the same action library.
- **First CPU test:** Place a real failure and a spurious straddle at separate gates, then exhaust a two-slot menu where greedy repair invalidates the second certificate. Hold out the later edit that needs it.
- **Retention:** Score A/C after the true repair and after later proof-assisted edits; do not count proof applicability without old-service outcomes.

#### 17. Two cheap proofs that compose only with a shared premise (P)
- **Mechanism:** Join refinements from separate editors at an explicitly correlated slot/weight predicate; refuse union of summaries with no compatible joint domain.
- **Novelty / control:** Assume–guarantee reasoning already composes summaries. A cheaper continual-learning operation must beat ordinary compositional verification, monolithic R and conjunction-free warm starts on the same mixed stream.
- **First CPU test:** Use two valid local contracts whose naive interval product permits a spurious gate, plus an incompatible pair; compare certified admissions under joint byte limits.
- **Retention:** Evaluate both A/C through the combined useful edit sequence and explicitly test the rare slice exercised only at composition.

#### 18. Online proof purchase with an expiration date (I)
- **Mechanism:** Pay to compile a shared refinement after a hit threshold; expire that investment after a version or premise change and adapt the threshold to measured hit/check cost.
- **Novelty / control:** This is ski rental with invalidation, plus verifier summaries. Compare classic rent-or-buy, simple LRU, pure cached R and pure M; no credit for clairvoyant arrival information.
- **First CPU test:** Stream six clustered hits, six dispersed hits and a late invalidation under the same edit-count budget; keep a multicost offline oracle separate.
- **Retention:** Match useful B throughput and measure A/C after every commit, especially just before and after expiration.

#### 19. Charge movement for the proofs it invalidates (I)
- **Mechanism:** Price a truthful trajectory move by its training cost plus stale proof dependencies, not just the current edit's FLOPs.
- **Novelty / control:** Incremental dependency tracking and externality-aware scheduling predate this application. Compare a fixed replacement-cost heuristic and an exact planner over the same dependency graph.
- **First CPU test:** In a two-gate stream, a cheap early move changes an assumption used by later edits; measure when a more expensive refinement wins under a memory cap.
- **Retention:** Evaluate A/C under the changed trajectory and after all deferred edits; confirm each recheck certifies its current state rather than the pre-move host.

#### 20. Proof carryover after verifier representation changes (P)
- **Mechanism:** Store a small independently checkable implication used by both a cheap interval-plus-cuts solver and a tighter verifier, so a change in checker need not discard prior work.
- **Novelty / control:** [Regression CEGAR](https://arxiv.org/abs/1806.04829) already reuses summaries across abstract precisions; compare canonical certificates, neural proof sharing and [solver-level warm starts](https://arxiv.org/abs/2609.25962). The claim is that an augmented-state, edit-local obligation survives with less evidence and revalidation.
- **First CPU test:** Switch checkers midstream on the relational toy, preserving one sound invariant and invalidating another via changed rounding semantics.
- **Retention:** Keep a fixed old-task specification, test A/C on all accepted paths after the switch, and count any stale-certificate false acceptance as failure.

#### 21. Learn which obligation to refine, not which example to replay (I)
- **Mechanism:** Choose one of several straddling inequalities to refine by expected useful admissions across blind editors; use checked candidate cuts as actions, never a learned safety verdict.
- **Novelty / control:** Learned branching and proof sharing already prioritize proof work. Compare strongest first-failure branching, frequency counts and independent verification with the same optimization/check budget.
- **First CPU test:** Use twenty compact requests with two correlated straddles, one common but nonbinding and one less common but decisive; use separate streams to fit and test cut selection.
- **Retention:** Verify A/C after actual admitted B work for each selector; equalize edit utility and report the worst old slice among rare admissions.

#### 22. Change the cost, not the answer (I)
- **Mechanism:** Independently vary proof precision, allowed data moves and suffix horizon; record the Pareto frontier and leave an edit unresolved when neither repair nor proof fits.
- **Novelty / control:** The parent's compile-away audit and budgeted verification already give this control. Its value is preventing a gain from hidden exact-solver calls, larger proof memory, later evaluation or quietly relaxing an old-task floor.
- **First CPU test:** Enumerate all policies for ten edits with shared and unshared cases, including an exact-unsafe control. Check that extra proof budget alone never admits the unsafe edit.
- **Retention:** Verify A/C after equal useful B progress, conservatively score any unverified admission, and report rejected, stalled and genuinely unsafe edits separately.

## Ranked deeper questions

1. **Do naturally trained pairs have actionable, silent split boundaries after conditioning on one full next response?** First establish a reproducible lead before the gate flips in ordinary CPU Adam histories, then intervene blind. If equal margins, vector-response matching plus short full-state transport, or a smooth risk score explain all gains, keep an optimizer diagnosis, not a new object.
2. **Can we correct the carrier without paying for a privileged state transplant?** A truthful lightweight witness must move the right slot region early, maintain both old tasks throughout, and beat direct projected replay/reset at equal B progress and bytes. If only injected moments work, claim causal identification, not a usable CL mechanism.
3. **Is there a real online frontier beyond certified training plus regression CEGAR with reuse?** Vary shared-straddle prevalence, invalidation, and whether moves persist; compare at equal useful admissions, retention, and resources. A result that only beats uncached CEGAR or assumes six future hits is not evidence.
4. **Can an independent editor reuse a split contract after the source is gone?** Withhold editors and suffixes, reuse the source allocation, and test joint slot repair and verifier reuse against rollout/repair plus cached verification. Value comes from more useful safe options or less total work, not from carrying a compressed ghost of the old optimizer.

**First paper-to-pilot gate:** No pilot is proposed for launch here. If the topic is selected later, start with cards 01 and 13 as CPU falsifiers. Keep the two claims separate until both survive their strongest controls.
