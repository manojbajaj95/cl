# Split-timed proof deadlines: can a learner's point of no return expire a proof?

**Status:** Ideas only; no experiments, probe code, or GPU work.

**Parent:** [Cross-pool round 43](https://github.com/manojbajaj95/cl/blob/31518a234f781c31c182d7c6d6ab5a46a571a535/ideas/flood/cross-pool-43.md) ([PR #36](https://github.com/manojbajaj95/cl/pull/36)), PSP1 and PSP3.

**Review seed:** [Flood triage, row 276](https://github.com/manojbajaj95/cl/blob/a5e4d368c09f7a3e6108c7a0214c7bb3cecf58c1/reviews/flood-triage.md#L276) scores both 3: PSP1 derives the last safe port entry from loss of repairability; PSP3 ends a hidden-coordinate lease at the optimizer-slot split that commits it to affecting the proof, even if the effect is not visible yet. The ingredients come from [certificate entry ports (PR #171)](https://github.com/manojbajaj95/cl/pull/171) and [irreversible splits (PR #172)](https://github.com/manojbajaj95/cl/pull/172). The reviewer found no merge in the round that already beats its best part.

**Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/a5e4d368c09f7a3e6108c7a0214c7bb3cecf58c1/reviews/idea-ledger.md): beat the stacked parts at equal budget, check ordinary old-task ability in each first test, and don't mistake a planted threshold or a save/restore tie for a new primitive.

## Is a proof that expires at the learner's own point of no return a new object for continual learning?

**Provisionally, yes as a reusable admission operation, not as a new kind of theorem.** The frozen suffix theorem never expires. What expires is an importer's right to enter under that theorem or to keep part of its training state out of the proof. A point of no return is not a new notion: [reach-avoid dynamic programming](https://arxiv.org/abs/1410.6445) already computes safe reachability, [critical learning periods](https://arxiv.org/abs/1711.08856) show history-dependent plasticity, and [Pacti](https://arxiv.org/abs/2303.17751) already composes contracts. The candidate CL primitive is a source-free, independently checkable admission receipt that reuses one training-substitution proof across late-arriving jobs, while binding entry and slot visibility to the same loss of intervention options. If a reach-avoid/Pacti implementation of the same contract ties on reuse and total cost, or the stacked CL parts tie, the node is an improvement at best.

### What is timed?

- **Freeze the scope.** Publish the entry set `E`, witness `W` and its suffix proof, the original edit, full-state update law (including slots, clocks and legal future batches), observations, truthful repair grammar, horizon, budget and old-task floors. The teacher used to produce `W` is unavailable after publication. An importer must prove its prefix and binding to `E` without consulting the teacher or redoing the suffix proof.
- **Use an action boundary, not a timestamp.** At decision boundary `i` the importer observes a transcript before update `i → i+1`. A stop/repair action selected there must be shared across all compatible full states; the legal continuations then branch. Define the winning set of transcripts by backward search: stop now with a legal source-free bridge to `E`, or wait only if every possible next observation admits a winning continuation. Both require old-task safety throughout, including while the bridge runs. The last safe decision is the last one on that history before continuing would eliminate all admissible ways to enter. A bridge can take several updates; it must be launched early enough to complete entry before the relevant split. An unobservable sibling cannot lend its deadline to the observed branch.
- **Separate a closed window from a closed checker.** A dynamical split rules out recovery under the frozen grammar and budget even for an exact finite-scope oracle that sees the full state. If full-state observation restores a winning strategy but no transcript policy wins, label it an information limit. If the exact transcript-level oracle wins but the deployed checker refuses, label it proof incompleteness. A single false row in a table of *immediate* placements is not irreversibility: report reopenings and disconnected windows, and use bisection only after proving monotonicity for the query it searches.
- **Make the lease end before the carrying update.** A lease states which variations in hidden coordinates may remain untracked and for which future updates the suffix substitution still holds. If update `j → j+1` can commit a slot residual to a later proof-visible effect beyond tolerance, require disclosure, a certified renewal, or refusal at boundary `j`, not at the first changed prediction. Renew only with a permitted state transform that preserves installed behavior and leaves the same correction admissible. An exact full-state oracle should distinguish harmful carry from harmless slot drift.

**Paper example (not evidence):** Take two histories with the same weights and logits but different momentum slots after a frozen warmup. A scheduled unmasking will let momentum push one history through a gate on step 4; its next few batches do not read that gate, but a later correction needs it. If enumeration shows that a truthful counter-impulse can restore the entry condition before step 4 and none of the allowed interventions can recover after it, boundary 3 is both the latest handoff opportunity in that history and the lease's stop boundary. A leaky or reopening gate, an allowed post-step reset, or a transcript that fails to distinguish incompatible responses can change that answer. Current output agreement alone says nothing about it.

### First-test contract

All tests below are proposed CPU enumerations or tiny learners, not results. Use a finite sibling family with a hard gate, a smooth ramp, a reopening and a no-carry control; use planted cases to debug, not to establish novelty. Then hold out stream families or slot histories with unplanted, strict interior boundaries. Freeze the package before the independent import stream is revealed. Match useful new-task progress and charge prefix/bridge updates, samples, observation and slot bytes, retained artifacts, oracle/checker work and failures of admission. Compare at minimum against (i) endpoint port and fixed early/long-budget variants, (ii) split localization alone, (iii) static leakage lease, slot reset and full-state proof, and (iv) the strongest of those parts stacked with the same observations and resources. Include a generic reach-avoid contract as a representability control. Measure safe useful admissions, unsafe admissions, and marginal proof cost; report coverage rather than hiding rejected jobs. For any ranking claim, first show deadline variation above noise and beat a constant and norm/margin-matched heuristics. In every test, `A/C` means held-out ordinary old tasks, including rare slices; compare prequential floors and final retention, not just the compiler's proof obligations.

## Idea cards

### Make handoff a policy instead of a date

#### 01. Import the same proof on two different clocks (P)
- **Mechanism:** Export one suffix artifact and a local stop-policy proof. Identical endpoint projections may require different bridge launch decisions because the intervening update laws create different repair windows.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) and [PR #171 card 7](https://github.com/manojbajaj95/cl/pull/171) already allow local compatibility; the proposed operation is reusing a deleted-teacher suffix proof while independently certifying that the import actually reaches it on time.
- **Cheapest first test:** Seal one port; reveal four small streams with coincident endpoints but different update order. Compare endpoint port, generously early handoff, split-search plus endpoint-port stack, and a generic time-indexed contract. Kill if the policy gives no extra safe useful admission at matched cost.
- **Old-task retention check:** Check held-out A/C after each waiting and bridge step and after the unchanged edit, not only on successful imports.

#### 02. Buy one bit about the slot, not the whole slot (P)
- **Mechanism:** Make a lease conditional on a proof-certified pre-update observation that splits a belief set only when the histories need incompatible entry actions.
- **Novelty vs nearest prior art:** [Belief-support planning for POMDPs](https://arxiv.org/abs/1511.08456) already reasons over hidden states; here a disclosure extends the domain of a frozen training proof without exposing the rest of the slot or changing the correction.
- **Cheapest first test:** Enumerate four quantized momentum states with identical visible traces; compare no read, one-bit threshold read, full-state checking and a generic belief policy at matched information/check costs.
- **Old-task retention check:** Check A/C on every full state behind each disclosed bit, including a rare slice that breaks if the two response classes are merged.

#### 03. Pay for a fast proof when the proof queue would miss the split (P)
- **Mechanism:** Model certificate computation as an action that consumes training ticks; keep a cheap, narrower admission receipt and a slower broad receipt for the same suffix.
- **Novelty vs nearest prior art:** [Reach-avoid dynamic programming](https://arxiv.org/abs/1410.6445) can price delays; the candidate is a proof portfolio with a learner-state-dependent expiry, not prioritizing verification jobs by fixed due dates.
- **Cheapest first test:** Two interleaved toy learners, one verifier and finite verification actions; let training continue on a frozen schedule. Compare earliest-deadline-first and pause-to-verify with the portfolio, charging paused updates as lost B progress.
- **Old-task retention check:** Score A/C while waiting in the queue and after execution, especially for the learner whose broad certificate was deferred.

#### 04. Carry an expiring witness through a closed entry window (P)
- **Mechanism:** Allow a source-free prefix proof to escrow a bounded slot correction at one open window and exercise it at a later safe entry window; the receipt has to prove the intervening closed window cannot invalidate what was escrowed.
- **Novelty vs nearest prior art:** [PR #172](https://github.com/manojbajaj95/cl/pull/172) audits whether windows reopen; [Pacti](https://arxiv.org/abs/2303.17751) composes time-indexed guarantees. The proposed unit is a separately redeemable preparation action across a non-entry interval, not a scalar latest date.
- **Cheapest first test:** Enumerate schedules with an open–closed–open gate; compare interval-aware placement, wait-until-reopen and immediate handoff, with identical samples and retained bytes.
- **Old-task retention check:** Score A/C inside the closed window as well as after redemption and after an extra legal overwrite.

#### 05. Prove the bridge can finish before it starts (P)
- **Mechanism:** Certify a multi-update truthful bridge by backward deadlines on its remaining stages; release each bridge stage only with enough slack to reach entry before irreversible carry.
- **Novelty vs nearest prior art:** [Iterative machine teaching](https://arxiv.org/abs/1705.10470) already chooses examples en route to a target; [PR #171 card 10](https://github.com/manojbajaj95/cl/pull/171) already proves source-free bridges. This candidate lets independently scheduled bridge stages inherit a completion proof rather than recalculating the witness.
- **Cheapest first test:** Exhaust all two-example bridges under two legal arrivals; compare guaranteed-completion scheduling to arrival-only entry and to time-constrained machine teaching with full rechecking.
- **Old-task retention check:** Check A/C between the two examples and at all remaining stages; a bridge that temporarily drops a floor is not a win.

### End a lease before hidden work becomes visible

#### 06. Revoke before momentum speaks (P)
- **Mechanism:** Bind a projection-fiber lease to the first update that makes harmful slot carry unavoidable under the remaining repair budget. Keep the private coordinate hidden on otherwise identical non-carry histories.
- **Novelty vs nearest prior art:** [PR #171 card 4](https://github.com/manojbajaj95/cl/pull/171) budgets leakage, [PR #172 card 3](https://github.com/manojbajaj95/cl/pull/172) finds slot-only splits, and [PackNet](https://arxiv.org/abs/1711.05769) isolates by freezing weights. The candidate is timed handoff of proof responsibility while retaining useful private learning, not blanket isolation.
- **Cheapest first test:** Enumerate matched-weight/matched-gradient histories with distinct momentum and delayed exposure. Compare both parts alone and stacked, static expiry, full-state proof and reset at equal work. Count delayed failures and useful private updates saved.
- **Old-task retention check:** Check nominal and rare A/C before expiry, just after carrying, on the edit and several steps after delayed exposure.

#### 07. Renew by transferring momentum into a safe block (P)
- **Mechanism:** Transfer only certified residual slot components into a block the frozen suffix never reads, if a checked transform preserves the original edit and keeps B progress. Do not renew merely because the final logits match.
- **Novelty vs nearest prior art:** [Gradient Projection Memory](https://arxiv.org/abs/2103.09762) projects current gradients, while [PR #171](https://github.com/manojbajaj95/cl/pull/171) budgets leakage. This is a renewal receipt over optimizer state and later repair, not projection of the next gradient alone.
- **Cheapest first test:** Two-block momentum model with rotating read direction; enumerate legal transfers versus gradient projection, full slot reset and no renewal at matched work.
- **Old-task retention check:** Score A/C before and after transfer and through read-direction rotation, including a rare old input that reads the destination block.

#### 08. Charge cancellations only when their order is guaranteed (P)
- **Mechanism:** Admit two private slot writes under a joint cancellation certificate if every legal path applies the cancellation before carry; otherwise retain each write's separate debit and expire on the first unsafe prefix.
- **Novelty vs nearest prior art:** Robust bounds such as [interval bound propagation](https://arxiv.org/abs/1810.12715) often lose correlation. The proposed operation ties netting a CL lease to a proven update order, not final perturbation size.
- **Cheapest first test:** Enumerate two opposite moment increments, both orderings and a possible intervening gate read. Compare absolute leakage sum, exact paired reachability, and a joint lease priced by proof cost.
- **Old-task retention check:** Run ordinary A/C after each increment and through the optional gate read so endpoint cancellation cannot hide forgetting.

#### 09. Distinguish two optimizer memories that agree on the next update (P)
- **Mechanism:** Use a cutoff certificate for the first future forcing sequence that separates hidden second moments even when the first gradient, next update and outputs match. Disclose only on a legal route to carry.
- **Novelty vs nearest prior art:** [Adam](https://arxiv.org/abs/1412.6980) has hidden moment state by design; [PR #172 card 3](https://github.com/manojbajaj95/cl/pull/172) spots slot-only splits. This extends the lease interface to delayed distinguishability under held-out forcing rather than declaring all such states immediately incompatible.
- **Cheapest first test:** Find paired two-coordinate quantized Adam states with identical first update but distinct later response; compare one-step signatures, slot norms and full-state recertification under equal checks.
- **Old-task retention check:** Check A/C on every forcing prefix and two delayed steps after the unchanged edit.

#### 10. Give one lease to mutually exclusive branches, not one lease each (P)
- **Mechanism:** Issue a shared leakage allowance whose safe balance is conditioned on which branch actually executes; require all compatible histories to have enough slack until they can be distinguished.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) can compose disjunctions; the candidate is saving proof work by pooling expiring slack across mutually exclusive useful training branches without double-spending it.
- **Cheapest first test:** Use a binary B stream with mutually exclusive slot amplifiers and then add an overlap branch as a negative control. Compare independent leases, uniform worst-case bounds and disjunctive full-state contracts at equal checker cost.
- **Old-task retention check:** Score A/C separately on both pure branches and the overlap branch, including after later stage mixing.

### Join decisions that the separate parts cannot price

#### 11. Spend one example to extend both clock and lease (P)
- **Mechanism:** Search for truthful examples whose slot effect delays carry and keeps a multi-step bridge launchable. Buy the effect only if it substitutes for two separate interventions, with the edit unchanged.
- **Novelty vs nearest prior art:** [Matching Training Trajectories](https://arxiv.org/abs/2203.11932) optimizes trajectory-matching data; [PR #172](https://github.com/manojbajaj95/cl/pull/172) buys earlier evidence. Here a single example must simultaneously enlarge a safe entry domain and extend safe untracked variation.
- **Cheapest first test:** Exhaust a small truthful pool with examples that affect only one clock and some that affect both. Compare joint choice against separately optimized bridge plus renewal under equal examples and oracle calls.
- **Old-task retention check:** Use a margin-matched A/C battery before the example, just after the original carry step and after the shared suffix.

#### 12. Control the order of independent B updates to preserve proof options (P)
- **Mechanism:** Where the future law allows reordering, certify two legal update orders with the same samples and final B target. Pick the order that leaves the lease valid until the bridge can meet entry.
- **Novelty vs nearest prior art:** [Critical learning periods](https://arxiv.org/abs/1711.08856) and [iterative machine teaching](https://arxiv.org/abs/1705.10470) already show timing matters. The proposed operation schedules equivalent B work by whether it preserves the ability to import a different, frozen proof.
- **Cheapest first test:** Permute four available batches in a tiny masked learner. Compare B-loss curriculum, split avoidance alone and joint order selection with matched B gains and search work.
- **Old-task retention check:** Measure worst-prefix A/C for each order and re-evaluate A/C after a common adversarially chosen legal batch.

#### 13. Trade an early entry for a longer private suffix lease (P)
- **Mechanism:** Publish a frontier of certified handoff/lease pairs: early entry can buy a different admissible hidden-state trajectory, while late entry may demand immediate disclosure. Importers choose a verified pair, not independently optimal times.
- **Novelty vs nearest prior art:** [Reach-avoid planning](https://arxiv.org/abs/1410.6445) can handle multiple constraints; the candidate artifact is a reusable joint menu with one installed suffix proof and no source-dependent renegotiation.
- **Cheapest first test:** Exhaust slot amplitudes and handoff positions in a two-stage learner. Compare the menu against independent schedules, the Cartesian product of individually valid choices and full-state multiobjective enumeration.
- **Old-task retention check:** Check A/C along every offered pair, particularly the pair with the latest carry boundary; also check A/C after retiring its extra private state.

#### 14. Put proof expiry across a serialized checkpoint (P)
- **Mechanism:** Re-use a deadline only if a checkpoint migration proves the restored optimizer slots, counters and numerical law preserve the same stop policy and lease validity. Otherwise mint a new prefix receipt or decline import.
- **Novelty vs nearest prior art:** [Pacti](https://arxiv.org/abs/2303.17751) composes interface compatibility, and [Adam](https://arxiv.org/abs/1412.6980) already requires moment state. The candidate is transporting a temporal right to use a proof, not transporting parameters or certifying identical restored execution.
- **Cheapest first test:** Restore matched weights under two legal slot encodings with distinct rounding. Compare byte-identical restore, slot reset, and separately re-proved entry; ask whether more than identical restore can reuse the suffix safely.
- **Old-task retention check:** Score A/C immediately after restore, at the first counter-dependent update and after the original edit.

#### 15. Protect a scarce shared repair action with contingent reservations (P)
- **Mechanism:** Two ports may need the same teaching example or verifier tick before different slot splits. Prove a reservation policy on joint observable histories, so neither importer spends a resource its sibling still needs on the same branch.
- **Novelty vs nearest prior art:** [Reach-avoid dynamic programming](https://arxiv.org/abs/1410.6445) can plan with a shared resource; the proposed CL operation composes admission receipts without recomputing either suffix proof.
- **Cheapest first test:** Two tiny learners, two possible arrival orders, one shared repair tick; compare individual deadlines, greedy earliest split and joint contract with the same clocks and workload.
- **Old-task retention check:** Check A/C for both admitted learners at every joint prefix and log retained capability for any blocked job.

### Try to make the primitive disappear

#### 16. Try to turn every sharp deadline into a smooth shadow price (I)
- **Mechanism:** Estimate the minimal safe bridge/renewal cost at each time over multiple repair budgets; distinguish a stable local cost jump from a smooth curve truncated by one arbitrary budget.
- **Novelty vs nearest prior art:** [PR #113](https://github.com/manojbajaj95/cl/pull/113) already found near-oracle ties for simple schedules in a smooth host; [critical periods](https://arxiv.org/abs/1711.08856) need not imply categorical expiry. This is a combined PSP falsifier, not a new object.
- **Cheapest first test:** Vary budget and gate softness in a tiny learner, then compare an oracle stop rule against fixed, linear-price and norm-based schedules on held-out streams. A planted hard gate is only a positive control.
- **Old-task retention check:** Fit costs only on paths that maintain A/C floors; match initial per-item margins and B progress across gate families.

#### 17. Ask whether the deadline is an abstraction bug (I)
- **Mechanism:** Attribute each refusal to actual loss of feasible repair, insufficient observations, or an incomplete checker. Reallocate the same budget to class-appropriate refinement rather than teaching or revoking by default.
- **Novelty vs nearest prior art:** [Neural network abstraction refinement](https://arxiv.org/abs/1910.14574) and [PR #172 card 9](https://github.com/manojbajaj95/cl/pull/172) already refine spurious failures. This card audits whether combining entry and lease creates more verifier mirages than real timing advantages.
- **Cheapest first test:** Use exact full-state, exact information-set and interval solvers on the same small graph; compare how many refusals vanish when spending one equivalent proof refinement rather than one truthful example.
- **Old-task retention check:** Recheck A/C over the exact reachable prefixes of every newly admitted path and independently flag unsafe admissions.

#### 18. Search for a witness that makes both clocks redundant (I)
- **Mechanism:** Optimize a slightly larger frozen buffer against all admissible slot histories and prefixes; check whether robustness absorbs every claimed deadline within the same total storage and verification budget.
- **Novelty vs nearest prior art:** [Matching Training Trajectories](https://arxiv.org/abs/2203.11932) and [Gradient Coreset Replay](https://arxiv.org/abs/2111.11210) already optimize rehearsal artifacts. This is the competing no-new-object explanation: just spend more of the same budget on a better buffer.
- **Cheapest first test:** Exhaust two feasible buffer sizes and all small truthful subsets. Compare robust fixed investment against receipts amortized over a blind family of imports, including shared-proof maintenance.
- **Old-task retention check:** Evaluate held-out A/C on all reachable paths, including overstress late slot histories not used to select the buffer.

#### 19. Break a seemingly portable deadline with a new editor (P)
- **Mechanism:** Publish a typed lease boundary and the hypotheses under which a held-out edit may reuse it. Require a new prefix proof for that payload and retain a separating continuation if the timing lemma fails.
- **Novelty vs nearest prior art:** [PSP4 in the parent](https://github.com/manojbajaj95/cl/blob/31518a234f781c31c182d7c6d6ab5a46a571a535/ideas/flood/cross-pool-43.md) and [Pacti](https://arxiv.org/abs/2303.17751) already retrieve reusable lemmas. The candidate is a transport rule for expiry with an explicit limit on what an unseen edit can infer, not a split atlas as routing permission.
- **Cheapest first test:** Seal deadlines from two editors; reveal two held-out ones, including one with identical slot signature and a different required response. Compare retrieval-only, checking all from scratch and hypothesis-bound transfer.
- **Old-task retention check:** Score A/C on each editor's actual suffix and rare slices specific to the separating continuation, not only on the editor that supplied the timing lemma.

#### 20. Compile the whole proposal away (I)
- **Mechanism:** Encode the same entry, hidden carry and admissible repairs as an ordinary partially observed reach-avoid problem, then export its policy and proof under a generic contract. Look for a reduction that preserves independent import and amortized proof cost.
- **Novelty vs nearest prior art:** [Reach-avoid](https://arxiv.org/abs/1410.6445) plus [Pacti](https://arxiv.org/abs/2303.17751) is the strongest prior-art account; a cost-preserving compilation would demote the node to an application of existing tools.
- **Cheapest first test:** Compare representations on the same finite graphs while increasing independent job count. Charge certificate bytes and first/marginal checking work on both sides; do not charge one side to re-prove a theorem it can validly reuse.
- **Old-task retention check:** Verify A/C at each prefix and after the common suffix for both policy representations, including traces blocked by only one representation.

## Ranked deeper questions

1. **Does coupling entry and lease expiry buy safe, useful admissions that the two parts stacked cannot buy?** Run cards 01, 06 and 11 on the same blind imports, old-task floors and budgets. Require an interaction on held-out histories at matched B gain and no unsafe admission; if the generic contract also ties (card 20), call it an improvement even if it beats the individual parts.
2. **Are there stable, strict interior expiry boundaries, or only price ramps and checker refusals?** Cards 16 and 17 must separate stable cliffs from thresholding one budget, information limits and proof incompleteness before claiming a new timing operation.
3. **What is the least information needed to act before hidden carry?** Cards 02, 08 and 09 ask when one disclosure bit or a checked order can replace full slot observation without cheating on shared actions.
4. **Can a deadline be transported without quietly changing the proof, edit or legal future?** Cards 14 and 19 test whether a timing lemma actually reduces marginal work across new optimizer states and editors, or whether every transfer needs a fresh reachability proof.
