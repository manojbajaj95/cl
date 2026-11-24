# Certificate entry ports: let a new learner prove entry, not the buffer again

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Return corridors](return-corridors.md) ([PR #168](https://github.com/manojbajaj95/cl/pull/168)), cards 2 and 14. **Review seed:** [Flood triage row 267](https://github.com/manojbajaj95/cl/blob/2d4ed8254dbc15802fb65dbf9c34332f36569d06/reviews/flood-triage.md#L267), two score-3 directions: push branch differences into units the witness never reads so one proof covers many branches; publish the certified region, buffer, and entry condition for independent learners. **Ledger read first:** [idea ledger](https://github.com/manojbajaj95/cl/blob/2d4ed8254dbc15802fb65dbf9c34332f36569d06/reviews/idea-ledger.md).

## Is an inheritable proof port a new object for continual learning?

**Not merely as a certificate with an entry condition.** [Pacti](https://arxiv.org/abs/2303.17751) already composes assume–guarantee contracts; [funnel libraries](https://arxiv.org/abs/1601.04037) already let independent planners compose preverified regions by checking interfaces. [PackNet](https://arxiv.org/abs/1711.05769) and [GPM](https://arxiv.org/abs/2103.09762) already protect selected parameters or directions. [MTT](https://arxiv.org/abs/2203.11932) makes small data match training trajectories, and [InterContiNet](https://arxiv.org/abs/2206.07996) and [Certified CL](https://arxiv.org/abs/2407.06697) certify aspects of retention. None of those distinctions, individually, makes this a primitive.

The candidate is a **portable certificate for retiring a training dependency**: the publisher uses truthful data to concentrate future branch differences in state the witness provably does not need; a later learner can keep those differences, substitute the same frozen buffer for the retired source, and prove entry without querying the source or rerunning the buffer proof. New for CL only if this buys substantially cheaper verification or wider useful admission than a generic contract wrapping the strongest existing training/substitution stack, at matched retention and learning. Otherwise the result is a useful contract design, not a new operation.

### Publish once, discharge locally

- **Publisher:** Freeze a versioned port `(π, C, W, E, K, H, ε, proof)`. `π` is the proof-relevant projection; `C` is the certified region (possibly time-indexed); `W` is the exact replacement buffer; `E` is the entry predicate and deadline; `K` fixes admitted post-entry transition semantics, including the external batch interface, optimizer and numerics; `H` is the covered suffix horizon; `ε` is the declared discrepancy budget. The proof binds these artifacts and the retired source version. For every admitted pair of live-source and replacement states in the region, the proof bounds the declared substitution error and establishes closure under both transitions for the suffix. It can use the parent's set chain or a paired relation. The theorem quantifies over the whole declared fiber of `π`, not just the publisher's reachable representatives; if it cannot, publish the missing fiber constraints or reject the projection.
- **Importer:** After the package is frozen, an independent builder reveals a new B stream family and supplies a local proof that **all** its admitted prefixes meet `E` by `τ`, on both arms if replacement can occur before entry, and that the suffix obeys `K` and stays within `H`. Until handoff, an already checked substitute or a source-free prefix must cover the transient; if entry needs the live source, charge it and do not count the job as post-retirement reuse. If the publisher supplied closure, the importer only discharges entry and applicability; do not charge it for reproving closure or silently assume a different optimizer is compatible. Outside scope, fail closed and count refusal. A proof checker may authenticate/check the shared proof once; per-job replay of that proof is not entry-only savings.
- **What “never reads” means:** A hidden coordinate may affect B, but must not disturb the certified guarantee now **or through future legal updates**. For exact hiding one sufficient condition is that the projected transitions and witness discrepancy factor through `π` uniformly on admitted fibers; for approximate hiding bound hidden-to-visible leakage and carry it through the paired proof. Momentum, clocks, gates, normalization, and adaptive samplers are part of the state when they affect that claim. Agreement on `π` alone proves nothing about full-state equality or A/C; state the protected output metric, and separately bound or test ordinary old-task retention. If a metric requires full-state agreement *between branches*, this is not the port for it.

**Smallest shared construction, on paper.** Use a finite quantized ReLU learner with a shared trunk, an A readout, and a live B readout. Two B orders have measurably different held-out B behavior. Choose a fixed subset `D` of truthful examples before the branches run. Search for a subset that routes the order effect into a unit read by B but stably off on the witness's inputs; do not hard-wire the separation. Exhaustively check the projected transitions under the declared suffix grammar, including hidden state and both arms. Publish one `C,W,E`; freeze it before a second builder reveals a different B family inside the predeclared interface. Include a legal near-boundary continuation that reopens the gate if allowed; the proof must either account for leakage or refuse. Compare with a fixed block-diagonal linear toy as a sanity check, not evidence: there the split is free. Use enumeration as ground truth for finite toys only.

### Common controls, accounting, and kill criteria

- **Free corridor:** measure the first naturally shared region and port cost with no shaping, at the same deadline and progress, using [linear mode connectivity](https://arxiv.org/abs/1912.05671) as a diagnostic, never as a substitution proof. Try full-state and projected pooling with the same verifier. Waiting and refusing both have costs.
- **Rigid corridor:** compare freezing, low learning rate, saturated gates, and lazy width at matched bytes, B progress, and a later plasticity probe on a task that needs a formerly shared feature. Count width and frozen private copies. Tiny certificates bought by stopping learning do not count.
- **Erased branches:** require distinct *useful* B behavior on held-out B inputs where the two objectives call for different answers, not just different weights or label-insensitive gauges. Compare against full-state agreement selection and an explicit reset/erase arm at the same budget; reject a cheap port that makes one branch's acquired B behavior disappear.
- **Stacked control:** compare no shaping, full-state agreement selection, PackNet/GPM, and proof-aware truthful selection against [HAL](https://arxiv.org/abs/2002.08165)/[TAR](https://arxiv.org/abs/2408.00761)-style shaping plus joint MTT, [verified training](https://arxiv.org/abs/1810.12715), Pacti and the same checker/retirement planner. Give the stack the same interface grammar and tuning budget. Compare full recertification of `W`, fresh buffer fitting and certification, and equal-byte replay or save/restore; label source-available arms as such rather than pretending they can run post-cut. No credit for the coalition unless it beats the strongest simple stack on the same jobs or shifts the useful admissions frontier.
- **Accounting:** precommit both the eligible-job denominator and tolerances before freezing the package. Count unique persisted and peak bytes (projection, region, buffer, proof, entry receipts, verifier metadata, copies/transient cover); separate publisher fit/source calls, shared proof check, marginal entry work, refusal/fallback, and runtime. Compare cumulative cost over several imports at matched scope or report the break-even count and where it never breaks even. Compare build/verify operation counts and wall time; do not charge a baseline to retain proofs it can soundly discard. A/C are normal old tasks on independent evaluation data, scored by acquisition and pre-cut references, worst slice and worst prefix, before entry, after actual retirement/overwrite with useful B state, and after reuse. Never supply the evaluation oracle to the learner or entry verifier. Refusals stay in the denominator.
- **Ledger gates:** kill as prior art if an existing operation with the same guarantees and cost implements the proposed novelty; reject claims true by construction (exact restore, planted freeze, a surcharge hard-coded into the checker). Falsify a result if a simple equal-budget baseline ties, any declared old-task floor fails, or useful B transfer vanishes. Before predictor/ranking claims, require variance above seed noise, test a constant/norm baseline, and match per-item margins for forgetting-order claims. If using sampled rollout truth, first report split-half reliability; validate surprise-mined effects over at least ten seeds before treating them as mechanisms. Do not assume sparse read or leakage structure without measuring it. **P** is a conditional primitive candidate (new operation if its novelty gate holds); **I** is an improvement or an audit. All tests below are proposals for CPU or paper work.

## Idea cards

### Buy a smaller proof by moving, not erasing, disagreement

#### 1. Teach a proof-invisible B channel (P)
- **Mechanism:** Score truthful subsets on the interaction between certified witness read footprint and branch differentiation. Move the order-dependent gradient into dynamically unread units, then fit one common buffer.
- **Novelty vs nearest prior art:** PackNet/GPM isolate tasks by restricting writes; this would induce order-specific separation by data, then export the resulting substitution proof, without prescribing a mask.
- **Cheapest first test:** Exhaust size-two subsets of a 12-example pool in the shared construction; compare full-state agreement, masks, free corridor and the HAL + joint MTT stack on common versus per-order buffer and proof sizes. Require useful order-specific B outputs.
- **Old-task retention check:** Score held-out A/C on both orders before and after entry and after overwrite; reject the subset if a legal gate reopening breaks a floor.

#### 2. Buy the right to forget a coordinate for three steps (P)
- **Mechanism:** Publish a time-indexed read projection: omit a B-bearing unit while it is unread, then require an explicit boundary relation on its value before that unit can rejoin the proof.
- **Novelty vs nearest prior art:** [IBP](https://arxiv.org/abs/1810.12715) and funnel composition use time-dependent sets; the candidate operation drops and later restores a state obligation without paying to track it throughout.
- **Cheapest first test:** Enumerate a four-step legal batch grammar with a delayed gate; compare a static union of relevant coordinates, separate proofs per order, and scheduled projection including boundary cost. Plant an out-of-relation arrival as a negative control.
- **Old-task retention check:** Score A/C immediately before and after the read set expands and after the next B update; count failed boundary checks as refusals.

#### 3. Find hidden-to-visible paths through the optimizer (I)
- **Mechanism:** Build a backward dependency slice from the error and protected metrics through all suffix updates, including momentum, global clipping, sampler and normalization. Only omit coordinates outside the slice or with a certified influence bound.
- **Novelty vs nearest prior art:** [LayerNorm](https://arxiv.org/abs/1607.06450) couples coordinates and formal verification already propagates dependencies. This checks the port's soundness, rather than proposing a new primitive.
- **Cheapest first test:** Exhaust paired starts with identical visible weights but different slots; toggle clipping or normalization and compare one-step masks to the dynamic slice. Include coupled and decoupled arms.
- **Old-task retention check:** Score A/C when the first hidden value reaches a visible gradient, including delayed overshoot, against the live-source arm.

#### 4. Lease a bounded leakage budget (P)
- **Mechanism:** Keep B directions that weakly feed the witness, but give each importer a certified budget for how much of that hidden-to-visible perturbation it may spend through the remaining updates.
- **Novelty vs nearest prior art:** [Certified CL](https://arxiv.org/abs/2407.06697) and robust funnels bound uncertainty; the putative operation is spending a composable budget on **untracked B variation** while reusing a training-replacement buffer, rather than certifying all state drift anew.
- **Cheapest first test:** Two coupled scalar updates with two legal batch amplitudes; compare a scalar cumulative budget to one worst-case bound, full-state proof, and a Pacti contract carrying the same scalar. Enumerate every missed-admission and unsound-admission candidate.
- **Old-task retention check:** Put independent A/C examples at several margins and check worst-prefix and post-cut errors at the budget edge, not just the average error.

#### 5. Hide disagreement in a moving basis (P)
- **Mechanism:** Let the ignored B span rotate after each legal batch, with a checked map between successive visible projections. Preserve branch information without keeping a fixed private block.
- **Novelty vs nearest prior art:** [GPM](https://arxiv.org/abs/2103.09762) estimates protected subspaces; the candidate is transporting a shared substitution proof across a sequence of different protected subspaces, not merely changing a gradient projection.
- **Cheapest first test:** Three-coordinate piecewise-linear learner with two activation cells; compare fixed projection, stepwise basis with certificate cost, and full-state proof. A plain invertible reparameterization is a null, not a win.
- **Old-task retention check:** Score old A/C across each basis change and on a later B task that needs the rotated feature; verify both original B branches remain useful.

#### 6. Choose training data against the strongest read-free alternative (I)
- **Mechanism:** Build a map from each truthful example's accuracy contribution to its marginal removal of proof-relevant dependencies; compare data shaping with simply making the learner modular.
- **Novelty vs nearest prior art:** [Progressive Neural Networks](https://arxiv.org/abs/1606.04671) isolate later learning structurally; the card asks whether data-induced hiding survives a stronger architecture control than GPM, not whether modularity is new.
- **Cheapest first test:** Tiny CPU MLP on split synthetic factors; exhaust truthful subsets in the shared arm and allocate the same parameter and byte budget to a modular arm. Compare proof leverage only if it varies beyond seed noise and beats gradient-norm ranking.
- **Old-task retention check:** Check ordinary A/C and a rare A/C slice that shares a factor with B, at matched B progress; add a later shared-feature learning probe.

### Make independent import useful

#### 7. Blind entry-only retirement (P)
- **Mechanism:** Freeze one package and retire the source; reveal independently designed streams; accept a local entry proof plus compatibility receipt, not a new witness proof or a refit.
- **Novelty vs nearest prior art:** Pacti and funnel libraries already supply the interface structure. The candidate operation is independent arrival after a training dependency has been destroyed, with one **substitution** proof amortized across useful new learners.
- **Cheapest first test:** Two builders in the finite toy, with the second B family specified before but sealed from the publisher until release. Compare no-shaping port, full recertification and fresh fitting with source access, and Pacti + strongest CL stack; count eligible jobs, admitted jobs and cumulative/marginal verification.
- **Old-task retention check:** Use independent A/C on each imported learner at every visible prefix and after overwrite; charge imports that fail entry rather than keeping only successes.

#### 8. Import a different model through a checked adapter (P)
- **Mechanism:** Map a new learner's projected transition/state into the publisher's interface; prove the map commutes with each admitted update and preserves the error metric, then check entry through it.
- **Novelty vs nearest prior art:** [Network Morphism](https://arxiv.org/abs/1603.01670) preserves a network function across architecture changes; this would preserve a *training-substitution theorem* across changes, not merely initial predictions.
- **Cheapest first test:** Try one extra ReLU channel with nonzero B activity, not an inert duplicate. Enumerate a compatible map and a width change that breaks the update equivalence. Compare adapter work with fresh proof and a generic refinement check in Pacti.
- **Old-task retention check:** Check A/C after every native update through and after widening; an adapter matching only the initial readouts must fail the test.

#### 9. Admit a novel batch alphabet by proving an abstraction (P)
- **Mechanism:** Let a second builder use new concrete B examples. Prove that their effects refine an already certified abstract batch alphabet, including adaptive sequence rules, instead of adding them to the publisher's concrete proof.
- **Novelty vs nearest prior art:** Pacti already checks refinement; the possible new operation is importing learning examples by equivalence of **training effects on the retired obligation**, while preserving distinct B semantics.
- **Cheapest first test:** Exhaust a quantized toy where distinct labeled batches share visible update classes; compare action-class checks, rerunning enumeration per concrete batch, and Pacti at equal grammar. Include one pair that only coincides at the entry point.
- **Old-task retention check:** Check A/C after repeating the new batches and after sampler switches; the pointwise-but-not-suffix class must not be admitted.

#### 10. Prove entry from a source-free training prefix (P)
- **Mechanism:** Design a truthful bridge that reaches the port using only the new learner and declared data, with an independently certified old-task floor until `W` takes over.
- **Novelty vs nearest prior art:** Funnel capture and [iterative machine teaching](https://arxiv.org/abs/1705.10470) already steer to target sets. The candidate operation extends the useful entry region **after** deleting the resource that would normally steer or certify the prefix.
- **Cheapest first test:** Enumerate length-one to length-three bridge sequences for starts outside `E`; compare waiting, retaining a live teacher for the transient, and a machine-teaching/Pacti stack. Count the entire bridge and proof rather than just post-entry work.
- **Old-task retention check:** Score A/C after every bridge example, not just on arrival; compare starts rejected because the only bridge briefly forgets A/C.

#### 11. Publish several entrances to one witness proof (I)
- **Mechanism:** Attach multiple certified entry predicates and deadlines to a single frozen suffix. Importers pick the cheapest valid entrance rather than widening the region to fit all starts.
- **Novelty vs nearest prior art:** A funnel library already offers multiple capture sets. This is an engineering comparison of admission versus certificate size, not a new object by itself.
- **Cheapest first test:** Enumerate two start clusters and one boundary case; compare the union of narrow entrances with one enclosing box and per-cluster buffers. Count entrance receipts and refusal cost.
- **Old-task retention check:** Compare A/C through both transients, including the longer entrance, and after identical suffix lengths from arrival.

#### 12. Publish an entry obstruction, not just a refusal (I)
- **Mechanism:** Attach a checkable lower bound on the distance any allowed truthful bridge can close before the deadline, distinguishing an impossible import from an incomplete search.
- **Novelty vs nearest prior art:** Funnel reachability and the [synchronizing consolidation obstruction (PR #108)](https://github.com/manojbajaj95/cl/pull/108) already show target sets can be unreachable. This is a useful negative receipt for training entry, not a primitive on its own.
- **Cheapest first test:** Use a finite injective-update toy with one unreachable target and one merely expensive reachable target. Compare lower-bound receipts with timeout and exhaustive oracle; count false refusals and receipt cost.
- **Old-task retention check:** For admitted and fallback arms, score A/C at normal deadlines; also check whether apparent reachability depends on allowing a bridge that drops an old-task floor.

### Reuse a port without turning it into a new dependency

#### 13. Link two ports by checking cross-reads (P)
- **Mechanism:** Allow two old training sources to retire if each port can prove the other's replacement writes preserve its entry and closure assumptions. Export a joint compatibility receipt without refitting either buffer.
- **Novelty vs nearest prior art:** Pacti composes contracts; [self-closing witnesses](self-closing-witnesses.md) already considers generic composition. Here the specific candidate is reusing **independently published** substitution proofs and discovering conflicts only through cross-read obligations.
- **Cheapest first test:** Two witness buffers and three units. Exhaust baseline combinations and both application orders; include a case safe in isolation but unsafe together. Compare the cross-read receipt with full joint certification and Pacti + joint MTT at equal bytes.
- **Old-task retention check:** Score both old task suites at every interleaving, not just after both corrections; retire both sources and check again after useful reuse of their space.

#### 14. Relay a proof through a later port (P)
- **Mechanism:** An importer proves its exit set implies another port's entry predicate with a compatible remaining horizon, then republishes a relay receipt so a third learner can use the path without opening the interior proofs.
- **Novelty vs nearest prior art:** Funnel composition already checks set inclusion between library elements. The candidate is a relay of checked *read substitutions* across independently retired sources, with an explicit error budget across handoffs.
- **Cheapest first test:** Three tiny task episodes, two blind handoffs; compare relay inclusion checks with generic contract composition and end-to-end recertification. Include incompatible error metrics or a witness switch at the wrong clock as a negative.
- **Old-task retention check:** Score A/C between ports and after the second handoff; plug in a last task that preserves the latest behavior but can break the oldest one.

#### 15. Patch the entry interface without replacing the buffer (P)
- **Mechanism:** Version the interface independently from `W`; support a tighter entry region or a changed batch interface via a checked refinement, and reuse only those receipts whose assumptions still hold.
- **Novelty vs nearest prior art:** Pacti supports refinement and [learned invalidation (PR #148)](https://github.com/manojbajaj95/cl/pull/148) addresses invalidation; the candidate operation is a compatibility patch whose unaffected imports keep a training-substitution theorem without the source.
- **Cheapest first test:** Shrink the region after adding a new B job that exposes an assumption violation under a proposed interface extension. Compare reissuing only affected entry receipts, rechecking all imports, and generic contract dependency tracking. No new claims outside the original certified scope.
- **Old-task retention check:** Replay the affected and unaffected A/C suites after the patch and overwrite; make one previously admissible job fail cleanly under the new interface.

#### 16. Make the second import cheaper than the first without assuming they match (P)
- **Mechanism:** Let importers publish source-free entry lemmas over families of starts, and allow later importers to cite just those lemmas whose predicates they prove. Keep the frozen buffer proof unchanged.
- **Novelty vs nearest prior art:** Funnel libraries and Pacti support reusable local artifacts. The proposed CL operation builds a library of learner-produced entry lemmas around one retired source, without turning the library into example replay or requiring publisher intervention.
- **Cheapest first test:** Four blind B families with partial overlap in prefix grammar. Compare a checked entry-lemma cache with exact receipt caching, Pacti and no cache; measure marginal proof work on both overlapping and disjoint jobs.
- **Old-task retention check:** Run A/C on each new family and on the original one after expansion of the library; a broad lemma that admits a forgetting path is a failure, even if the reused proof is correct on its original domain.

#### 17. Translate a changed optimizer rather than accepting a new law (P)
- **Mechanism:** Let an importer prove that its concrete optimizer and slots simulate the port's visible transition semantics within the published budget. If no such map exists, keep the original law or refuse.
- **Novelty vs nearest prior art:** Pacti refinement and robust funnels already model alternative dynamics. The possible novelty is a checked translation that permits reuse of a frozen substitution proof without widening the publisher's region to all optimizers up front.
- **Cheapest first test:** Quantized scalar SGD against a momentum schedule with a provable relation in one tight regime and overshoot outside it. Compare translation, a robust multi-law corridor, and full recertification with the same tolerance.
- **Old-task retention check:** Score held-out A/C after optimizer changes and at worst overshoot; a matched prediction at the first step is not enough.

#### 18. Fuse two retirement obligations into a shared quotient (P)
- **Mechanism:** Instead of linking two ports as in card 13, jointly design the projection and buffer so both sources' substitution proofs share the same checked facts but retain independently stated guarantees.
- **Novelty vs nearest prior art:** Joint MTT and GPM already share representations across tasks. Here the object under test is a multi-source proof that can be discharged once even though importers request different source-specific guarantees.
- **Cheapest first test:** Enumerate two source corrections with overlapping, but not identical, read sets. Compare independent ports, linked ports, joint MTT plus two verified contracts, and a shared proof factoring out common steps; count bytes and source queries.
- **Old-task retention check:** Score each source's A/C slices separately on importers requesting each guarantee and on importers needing both. Do not average away damage to the less frequent source.

### Find where the primitive claim fails

#### 19. Price truthful examples by the independent jobs they unlock (I)
- **Mechanism:** Rank candidate examples by the marginal number of entry-only imports they enable at fixed byte budget, rather than by the size of the publisher's own proof.
- **Novelty vs nearest prior art:** [HAL](https://arxiv.org/abs/2002.08165) and look-ahead selection price future learning effects. This changes the objective to a portability metric; it is not a new operation by itself.
- **Cheapest first test:** Choose from a small pool using a development family, then score the chosen subset on sealed whole families. Compare proof-size, margin, gradient-norm and random rankings; stop if admitted-job counts barely vary.
- **Old-task retention check:** Recompute the useful-admission ranking after imposing per-prefix A/C floors; a job bought by slight but systematic A/C loss does not count.

#### 20. Plot the proof-port break-even curve (I)
- **Mechanism:** Measure how many independent jobs must import successfully before publishing and authenticating the artifact pays for itself, including cold starts, refusals and immutable byte costs.
- **Novelty vs nearest prior art:** Proof reuse in Pacti and funnel libraries already amortizes build work; this is the accounting audit for source retirement, not a new object.
- **Cheapest first test:** Sweep job count and eligibility in a finite toy; compare against full recertification, fresh fitting, exact retirement and equal-byte replay. Report the no-break-even regime as well as the best case.
- **Old-task retention check:** Hold A/C floors and B progress constant when setting each curve; report invalid or refused jobs in the precommitted denominator.

#### 21. Minimize what the port reveals without hiding what it assumes (P)
- **Mechanism:** Export a coarse entry predicate and compact proof of its sufficiency; keep the publisher's concrete trajectories out of the artifact. Treat any retained source summary used by the verifier as part of the port, not as free infrastructure.
- **Novelty vs nearest prior art:** Pacti projects internal variables out of contracts; [IBP](https://arxiv.org/abs/1810.12715) propagates abstract bounds. The candidate is a minimally revealing **retirement** proof whose sufficient entry predicate preserves useful blind imports with fewer persisted source-derived artifacts. It is not a privacy guarantee.
- **Cheapest first test:** On a finite alphabet compare a small predicate built from necessary visible features, a generic projected Pacti contract and a lookup table over admissible starts. Charge false refusals, summary bytes and checker work.
- **Old-task retention check:** Enumerate A/C on starts that the coarser predicate merges, including a rare slice that distinguishes two superficially identical starts; any unsafe acceptance fails.

#### 22. Compile the whole port into existing operations (I)
- **Mechanism:** Encode the same artifact as a Pacti contract over a standard certified-training/MTT stack. Ask which operation, if any, cannot be recovered without loss on blind imports. Run equal-budget replay and save/restore as additional nulls.
- **Novelty vs nearest prior art:** Pacti, funnel libraries, MTT and Certified CL are not weak baselines; if the stack recovers the interface and gains, the primitive claim is already explained.
- **Cheapest first test:** Use the same precommitted importer panel, proof grammar and checker for shaped/unshaped and shared/separate arms. Compare the incremental gain of combining hiding and reuse with mounting both features independently on the strongest stack. A simple tie is a negative result.
- **Old-task retention check:** Score normal A/C at every prefix and after actual overwrite for every arm at matched B progress; ordinary retention must survive both the composed and independently reused settings.

## Ranked deeper questions

1. **Can an independent learner inherit a retired-source substitution proof by proving only entry?** Freeze `C,W,E` before revealing the blind B family (cards 7, 9, 10). Require no post-cut source calls, useful admissions and intact A/C; compare cumulative and marginal work with refitting, full recertification, and the strongest Pacti stack. Equivalent admissions and work mean the port is not a new CL primitive.
2. **Does hiding branch differences actually make reuse cheaper?** Establish the free LMC corridor and rigid-corridor frontier first, then compare shaped and unshaped projections against full-state agreement and masks (cards 1–6). Require different useful B outputs, dynamic noninterference or priced leakage, and a joint gain beyond the stacked parts. Otherwise either no shaping was needed or the “win” erased learning.
3. **Can independent proofs be linked without reopening the old ones?** Check cross-reads and relay handoffs for three tasks (cards 13–18). Seek reusable receipts at matched admission scope, total error and every old-task floor; a generic contract composition tie is evidence against a new object.
4. **Where is the boundary between a cheap port and moving recertification into entry?** Compare import across batches, widths and optimizers (cards 8, 9, 17, 20–22). Plot the break-even under a fixed job denominator; show an honest refusal and a useful transfer. If compatible entry costs about as much as recertifying, or the only cheap entry is a frozen clone, stop.
