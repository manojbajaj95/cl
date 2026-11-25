# Dual-duty parks: keep the park working, then hand off inside recovery

**Status:** Ideas only; no implementation, pilot, or GPU work. **Parent:** [Ready parks](ready-parks.md) ([PR #254][parent]), cards 04 and 18. **Review seed:** [Flood triage, row 369][triage] advances two score-3 ideas: co-train a recovery basin and safe edit region around a feature that normal service demonstrably relies on; then survive a second adaptive default mid-edit by moving live service to another coupled, already-certified feature. **Ledger read first:** [Idea ledger][ledger].

## What would make this a continual-learning primitive?

Let `H` contain all reachable histories consistent with the public transcript. For a park feature `p`, write `B_p` for the states from which lawful ordinary successor work returns to ready, and `E_p(e,d)` for states from which a common blind edit for request `e` can finish by the remaining deadline `d`, including safe clear and the declared continuation. Both sets are **path** claims: endpoint scores alone do not qualify. The training target is useful overlap on reachable held-out requests and update orders, not its geometric volume.

- **Hard normal reliance is separate from hard service retention.** Before training, register normal operating slices, a feature-specific intervention and a minimum loss of service under that intervention. E.g., on an ordinary A slice, normal score must be at least `0.95` and must drop at least `0.15` when the feature's declared contribution is neutralized without changing dispatch, other features, or reads. Require both inequalities independently on held-out slices; do not average an unused slice away. Check the intervention against equal-sized neighboring lesions and matched-distribution replacements, and define feature identity by its causal route rather than an arbitrary basis coordinate. The diagnostic intervention may break the normal target; real deployment ticks must still meet their A, installed B, and rare C floors. A tiny but indispensable trigger is not evidence of a reusable feature unless perturbing its learned content, not just its enable bit, matters.
- **The second default is a fault during a live write, not a second cold start.** After default 1, useful C recovery brings the host inside the certified overlap. A real blind B pair starts there. Before publishing each prefix, certify a directed transfer from `p` to `q` for every in-scope second default the prefix exposes. The proof starts from the actual partial write, residuals and remaining time; it includes the first observation after the switch, old service on `q`, the suffix and public clear. Freeze the admissible fault actions, public detection/dispatch boundary and fault dependence up front. A common-mode or out-of-basin fault may require a pre-reserved safe refusal; don't score that as delivered B or claim retention where no safe fallback exists. No access to a retired feature, no hidden rollback, no refreshed deadline.
- **Same resources and same obligations.** Match feature/optimizer width, peak and resident bytes, normal throughput and scores, actual useful C progress, legal actions and observations, deadlines, initial margins, fault rights, and evidence/training budgets. Charge certification, reservations, refusers, switching, stalls and recertification. Check A, every installed Bᵢ and disjoint rare C separately at every observable step, including both defaults, interrupted edit, handoff, clear and held-out continuation, across all histories in the finite fixture. Also check preservation of the pending write and count on-time B gains separately from safety and from refusal. Keep dispatch, continuing training and optimizer residuals on separate ledgers. Empirical checks on larger hosts are not universal certificates.

**Prior-art floor and kill lines.** [Once-for-All][ofa] already trains nested subnetworks; [OML][oml] and [ANML][anml] train for subsequent adaptation; [fault-aware training][fat] injects faults during training; [predictive safety filters][filter] already certify recovery through backup policies; [imperfect-information games][games] give the exact finite strategy baseline. [ReviveMoE][revive] switches roles or uses redundant experts on hardware failure, and [EEP][eep] maintains live serving membership and repairs expert coverage. Those are strong controls for active redundancy, not evidence of a learning benefit with pending edits. This is a quick abstract-level screen (Hugging Face Papers discovery and linked abstracts), not a novelty proof.

For reliance, beat #254/MRS2 **without** the floor, an equal-width dormant park, nested Once-for-All modes, [#224#12][glued]'s fixed gate and separately trained basin + edit modes under the same floor; include a host where the floor forces the two regions apart. For second defaults, beat single park, [#224#18][glued] rolling parks for one edit, [#236#05][adaptive] two-order overlap, paid restart/checkpointing, an equal-budget active standby ([#256][standby]), and their strongest legal stack. Give exact contingent planning the same state, actions and fault map: its coverage on the **same host** is an upper bound, not something to beat. A nontrivial claim is better host feasibility or less verification/execution cost for equivalent coverage. Row 369 gives no new score-3 rating to the parent's inherited admissions, backing, slot cleanup, public clears or audits; don't relabel them as inventions. The ledger kills return-point adapters for storing the answer in a save/restore stack and read-pinning for passing at the pin while downstream clients fail. A snapshot or good-looking intermediate is not a positive here. `P` marks a conditional primitive candidate, `I` a direct instance, improvement or falsifier.

## Exact paper fixtures (sanity checks, not matched-budget wins)

**R · A real reliance floor can remove the overlap.** Let normal service score be `A(s)=1−(2/5)d(1−s)` at gate setting `s∈[0,1]`, with design parameter `d∈{0,1}`. Normal mode is `s=1`; neutralizing the contribution (`s=0`) drops A by `(2/5)d`. The hard reliance floor `3/10` forces `d=1`. Maintenance A must stay at least `3/4`. A prior B reader is independently 1. From the default at `s=1`, one ordinary recovery action sets `s=2/5`, the ready target; the same action is safe from any `s∈[2/5,1]` at edit bits `w=u=0`. Use rare C readers `C±=1±2ks(w−u)`, with floor 0. A blind pair sets `w=1`, then `u=1`, then clears `s=1`, one operation per tick; the required full mismatch at the first write makes the edit possible at the interruption gate only when `s≤1/(2k)`.

| Host | Reliance drop | Coupling `k` | A and worst C at first write, `s=2/5` | Result |
|---|---:|---:|---|---|
| Fixed coupling, no reliance floor (`d=0`) | 0 | 1 | `1, 1/5` | Edit fits; reliance fails |
| Fixed coupling, hard floor (`d=1`, `k=1+d`) | 2/5 | 2 | `19/25, −3/5` | Refuse: overlap empty along this recovery path |
| Shaped coupling, hard floor (`d=1`, `k=1+d/4`) | 2/5 | 5/4 | `19/25, 0` | Pair fits in three ticks; both C readers return to 1 after second write |

At `s=1/2`, the shaped host's first write instead gives worst C `−1/4`: the center path is not a certificate for every recovery phase. The host coefficients and recovery action are stipulated; this fixture does not show they can be learned or that the C action carries useful task progress.

**H · The second default changes service ownership, not edit history.** Give two resident service features `p,q` one shared live edit seam `(x,y)`; they are coupled through its independent rare C readers `C±=1±2s(x−y)≥0`. A and prior B each have floor `3/4`. While available, `p` gives both scores 1; `q` gives `A=1−|z|`, `B_{old}=1−2|z|` for residual `z` carried by its own service route. Its transfer certificate therefore covers `|z|≤1/8` and separately checks the C path and unfinished edit. Choose one write per tick, half-unit monotone steps for x and y, and public ownership at the tick boundary. At tick 0 default 1 invalidates readiness and leaves `(s,x,y)=(1,0,0)`; tick 1 recovery sets `s=1/2`; tick 2 begins the pair with `x=1/2`. At tick 3 a public second default disables `p` and gives `z=1/8`; a pre-certified switch to `q` uses that tick, with no intermediate service read under the declared atomic dispatch rule. A and prior B are now `7/8,3/4`; worst C is `1/2`. Ticks 4–7 set `y=1/2,x=1,y=1,s=1`, respectively. Worst C on that suffix is `1,1/2,1,1`, and B finishes at its original tick-7 deadline. A restart that discards x consumes at least one rollback tick and repeats the first write, missing the deadline; an exact planner given the same live switch can tie.

If the same public fault tag can also leave hidden `z=1/4`, prior B on q would be `1/2`: the common switch certificate is invalid even if the realized test happened to use `z=1/8`. Give this negative a separately charged, pre-reserved floor-only fallback (A and prior B both `3/4`, no B-edit rights); at tick 3 it keeps the existing C-safe prefix untouched and counts the pending B as unserved. If service reads between disabling p and routing to q, certify that extra boundary or reject the atomic schedule. Neither hardware fault independence nor trainability is implied by this fixture.

## Idea cards

### Train a feature that still works when it isn't parked

#### 01. Train on the triple intersection (I)
- **Mechanism:** Constrain held-out normal reliance and jointly train the feature on useful C recovery prefixes and safe blind edit suffixes; use failing prefixes as new constraints, not as labelled future B answers.
- **Novelty vs nearest prior art:** Directly instantiates #254#04; Once-for-All and OML already train shared modes or adaptive representations. The proposed gain is more reachable, deadline-feasible overlap **at the same causal reliance**, not better multi-mode inference.
- **Cheapest first test:** Exhaust a three-feature linear host's rational coefficient grid on two old update orders and blind held-out B edits; compare with independent basin/edit tuning, the fixed gate and the no-floor frontier.
- **Old-task retention check:** Replay A, prior B and rare C after every step and after clear; audit normal A with and without the declared feature.

#### 02. Make reliance survive a replacement test (I)
- **Mechanism:** Require dependence on the trained feature values under a matched-marginal, wrong-input replacement while keeping the gate and router unchanged. Retain the neutralization floor too.
- **Novelty vs nearest prior art:** Ablation and activation patching are known; this is a falsifier for a gate that switches unrelated work on and off, not a new park.
- **Cheapest first test:** Compare a tiny learned feature with an enable-bit counterfeit that passes zero ablation but ignores which nonzero value it gets.
- **Old-task retention check:** Evaluate unmodified normal A/Bᵢ/C at each phase and measure reliance on predeclared A and prior-B slices independently of the replacement calibration set.

#### 03. Teach a shared feature where defaults would otherwise send it (P)
- **Mechanism:** Choose truthful C examples whose updates direct *different* post-default histories through a small common edit cell; continue to use the same examples for normal prediction rather than allocating a park-only gradient budget.
- **Novelty vs nearest prior art:** #236#10 teaches the basin; OML shapes updates. The candidate is a useful old-example selection policy that also merges the *deadline-feasible blind edits* across those histories at the hard reliance floor.
- **Cheapest first test:** Enumerate subsets of a six-point linear C stream; compare to best matched C utility replay plus a separate park loss on unseen B directions and reversed C orders.
- **Old-task retention check:** Track per-tick A, prior B and rare C including C points excluded from the teaching subset; reject utility bought by delaying required C corrections.

#### 04. Spend a normal activation’s surplus on transient edit room (P)
- **Mechanism:** Learn a feature whose ordinary error margin absorbs a bounded temporary edit-induced deviation and whose useful C updates refill the margin without carrying a saved activation.
- **Novelty vs nearest prior art:** GEM constrains interference and #254 trains compatible regions; the bet is renewable slack in a feature the normal workload needs, not a fixed clipping threshold or spare channel.
- **Cheapest first test:** On a one-ReLU host, enumerate two blind edits and two C corrections; compare to a fixed barrier plus optimal projected C updates under the same A and reliance bounds.
- **Old-task retention check:** Score normal A by slice before/after each recovery cycle and check all prior B/rare C at the worst intermediate deviation, not just on renewed margins.

#### 05. Learn a feature with disjoint service and edit sensitivities, not disjoint slots (P)
- **Mechanism:** Train a shared nonlinear feature to respond strongly to normal data but weakly along the *finite* seam motion of held-out B writes when in the basin. Keep both responses in the same resident state.
- **Novelty vs nearest prior art:** #224#12 already decouples a fixed gate, and projected gradients null local interference. Look for nonlinear path separation that spans multiple useful edits with the same feature and no extra resident slot.
- **Cheapest first test:** Compare fixed gate, tangent projection and co-trained quadratic feature on two finite edit directions with matched normal margins; include a direction tangent at entry but unsafe halfway through.
- **Old-task retention check:** Check A/Bᵢ/C at each sampled write on a finite grid and certify any unsampled intervals separately; repeat the normal ablation after clear.

#### 06. Require ordinary work to pay for moving readiness (P)
- **Mechanism:** Permit the common safe cell to drift as tasks accumulate, but require the same paid updates that correct C to move the feature into its next cell; give the cell a public index, never a hidden history label.
- **Novelty vs nearest prior art:** MRS2 uses C to maintain one park and #168 uses return corridors. A candidate gain is reusing the same useful feature and reusable proof as the cell changes; continually fitting fresh parks is not new.
- **Cheapest first test:** Use three changing scalar C targets and a frozen B request generator; compare against best static robust cell and full re-certification after each target.
- **Old-task retention check:** Keep earlier C targets on disjoint protected slices; check A/Bᵢ/old C during each relocation and normal reliance at each new cell.

#### 07. Give the old workload first claim on the park (P)
- **Mechanism:** Train a feature to support a declared family of normal A/B service windows at high load; use only certified off-peak windows to traverse the edit region, with a reservation that cannot be moved after the request arrives.
- **Novelty vs nearest prior art:** Deadline admissions and slack scheduling already exist (including #254); the test is whether the *learned* service-versus-edit frontier shifts as opposed to merely booking already idle time.
- **Cheapest first test:** Enumerate a two-load, three-slot trace with blind B arrivals at both loads; let the separately trained host use the identical optimal scheduler.
- **Old-task retention check:** Score each high-load A and installed B request on time and each rare C separately; charge every off-peak delay and test reliance in both registered windows.

#### 08. Learn a backlash-resistant park (P)
- **Mechanism:** Shape one active feature so on either side of a C correction's overshoot, two neighboring recovery states remain in edit scope without needing a compensating park write.
- **Novelty vs nearest prior art:** Robust control and #237's order-robust park already cover margins. Seek robust completion of finite blind edits after opposite signed old-task updates, not just proximity to the same center.
- **Cheapest first test:** Use two opposite orderings of rational momentum drives; compare with a predictive safety filter wrapped around an independently trained active park at equal clipping and C progress.
- **Old-task retention check:** Check A/Bᵢ/C at each overshoot and post-clear step including one unused C drive; retain the normal reliance floor at both order endpoints.

#### 09. Build the counterexample host first (I)
- **Mechanism:** Make the sole legal normal carrier and the sole edit-isolation direction algebraically incompatible above a reliance threshold; report the infeasibility rather than bypassing the floor.
- **Novelty vs nearest prior art:** Feasibility bounds are known; this controls the degeneracy that a claimed joint loss can silently relax the old workload.
- **Cheapest first test:** Generalize fixture R to all gates in a bounded interval and solve both inequalities exactly; include a width-matched dormant solution that only works without reliance.
- **Old-task retention check:** Check safe refusal against all A/Bᵢ/C constraints and identify the first old reader that would fail if the pair were forced.

#### 10. Transfer a role definition across changes of basis (P)
- **Mechanism:** Train the certification target on an intervention-defined feature subspace and a public downstream seam, then preserve those across invertible reparameterizations produced by ordinary learning.
- **Novelty vs nearest prior art:** Net2Net and reparameterization preserve functions; #237 checks seam equivalence. Transfer of *edit permissions* only matters if cheaper than a full recheck and valid for the actual effective updates.
- **Cheapest first test:** Rotate a two-dimensional linear representation and solve transformed write sets exactly; compare to unconstrained function-preserving rotation plus a recheck. Include an optimizer-slot rotation omission.
- **Old-task retention check:** Test A/Bᵢ/C before and after both reparameterization and edits; verify the same causal subspace intervention retains its measured normal drop.

#### 11. Share C work, not recovery labels (I)
- **Mechanism:** Train on ordinary C updates but estimate readiness using independently sampled B probes; run a same-utility control with C examples that predict the same task scores but do not contract toward the park.
- **Novelty vs nearest prior art:** Matched-utility and shuffling controls are known and the parent already requires one. This separates causal maintenance from mere recovery phase prediction.
- **Cheapest first test:** Construct two four-point C streams with the same endpoint and distinct intermediate update order, and inject B arrivals independently of the training clock.
- **Old-task retention check:** Check old A/Bᵢ/C through both streams, including examples not used to measure readiness; flag any hidden staging period in normal throughput.

### Move live service when recovery itself is interrupted

#### 12. Commit only prefixes with a certified next owner (I)
- **Mechanism:** Before first publishing an edit prefix on p, attach a certificate that q serves old work and the actual prefix admits a lawful suffix on each in-scope second default.
- **Novelty vs nearest prior art:** Direct #254#18; #224#18 and #236#05 stack rolling parks and two-order coverage. Count a gain only if co-trained coupling makes more prefixes admissible than that stack.
- **Cheapest first test:** Enumerate fault times and starts in fixture H, comparing single park, the two-order stack, exact planning and identical prepaid restart rights.
- **Old-task retention check:** Probe A/Bᵢ/C at entry, before and after each fault and switch, through finish and clear; verify the prefix is neither erased nor silently replayed.

#### 13. Pre-certify the effect of a fault, not its name (P)
- **Mechanism:** Train q and certify transfers for a compact set of *seam effects*, including the live prefix and residual, across names and timings. At dispatch use only the public effect bound; no hidden fault fingerprint.
- **Novelty vs nearest prior art:** Robust tubes and belief-state planning already group uncertainties. The CL claim is that ordinary learning keeps the effect class valid across blind edits and saves paid evidence over a recomputed quotient.
- **Cheapest first test:** Enumerate two fault names with identical admissible effects and one same-tag divergent effect; freeze a certificate before revealing a new edit direction.
- **Old-task retention check:** Require A/Bᵢ/C floors in every world consistent with the tag, including a worst-case effect not used in training; outside the bound use a charged safe refusal.

#### 14. Carry the debt forward with the service route (P)
- **Mechanism:** Couple two park features so q's lawful suffix accounts for both prior edit progress and the survivor's accumulated optimizer drift, without restoring a private p slot.
- **Novelty vs nearest prior art:** #256 already matches residual-tail partners with realized drift. Look for a trained active route that gives one certified *blind* suffix over several drift beliefs, not a fresh tail match after reading drift.
- **Cheapest first test:** Add bounded signed momentum to fixture H, compare exact blind and drift-observing planners under separately priced reads, and use a case where a zero-initialized tail appears safe but isn't.
- **Old-task retention check:** Check signed cumulative A/Bᵢ/C impact across the handoff and remaining tail, including the first post-clear optimizer step.

#### 15. Certify a switch while both coupled features are still serving (P)
- **Mechanism:** Train the features so the transfer can occur with non-atomic routing and at least one observable mixed-route tick, without counting the same service twice or cancelling it only at endpoints.
- **Novelty vs nearest prior art:** Make-before-break and ReviveMoE role switching already handle capacity transitions. The bet is a mixed state that remains a safe blind edit state with no extra copy of the live model.
- **Cheapest first test:** Enumerate two read orders in a bilinear two-gate host; compare an atomic switch, a paid duplicate service lane, and a learned overlap at equal bytes and lawful observations.
- **Old-task retention check:** Evaluate each A/Bᵢ/C reader both before and between routing changes through the pending write and clear; disallow an intermediate outage hidden by a tick average.

#### 16. Learn a pair whose failures overlap less than its useful work (P)
- **Mechanism:** Co-train p and q on shared ordinary service but diversify exactly their dependence on vulnerable seam producers so either can cover the other's declared failure while both retain useful capacity.
- **Novelty vs nearest prior art:** Fault-aware training and active redundancy already diversify failure paths. The candidate is improved *post-write* functional separation at the same normal reliance, not static fault accuracy.
- **Cheapest first test:** With three resident features and one shared clip producer, enumerate every allowed producer failure; compare robustly trained duplicate heads, an independent hot spare and the coupled design.
- **Old-task retention check:** Probe ordinary A/Bᵢ and rare C on both independent and common-mode faults, and explicitly report no handoff where the common producer invalidates both certificates.

#### 17. Learn directed handoff coverage, not two interchangeable spares (P)
- **Mechanism:** Shape p→q and q→p against different reachable partial writes. Choose normal routes that preserve a legal directed exit for the currently admitted request, not routes that maximize symmetric feature similarity.
- **Novelty vs nearest prior art:** Fault automata and imperfect-information games already express directed transitions. Test whether a fixed-width learned host can add directed edges while keeping both live service roles, beyond an optimal policy on a symmetric host.
- **Cheapest first test:** Enumerate two request families with asymmetric deadlines in a two-gate finite game; hold policy class constant and change only the trained coupling.
- **Old-task retention check:** Run A/Bᵢ/C through both legal directions and the reverse-direction negative; verify ordinary reliance for each direction's source on its registered slice.

#### 18. Reserve against timing chosen after the first write (P)
- **Mechanism:** Train the carrier pair against an adaptive second default that can inspect public progress and strike at the worst legal phase; accept fewer first writes if that raises delivered work worst case.
- **Novelty vs nearest prior art:** Robust games already choose adversarial timing; the training claim is that p/q coupling reshapes the bad phases rather than scheduling around a known fault script.
- **Cheapest first test:** Exhaust the small phase game from first publication to last clear; compare random fault injection, optimal adversarial certification of separately trained parks, and restart.
- **Old-task retention check:** Check A/Bᵢ/C at every phase including late and no-fault traces, and report served B as a fraction of all arrivals, not just certified successes.

#### 19. Make the backup ready before the publisher learns the request (P)
- **Mechanism:** Train q to cover a public *class* of partial-write effects before the B payload arrives; bind the eventual payload only through a cheap check of its effect and deadlines.
- **Novelty vs nearest prior art:** Assume/guarantee contracts and #171 proof ports already separate generic proofs from entry checks. A win requires learning one live backup state that covers held-out effects cheaper than generating ports per request on the best matched host.
- **Cheapest first test:** Certify on two rational edit amplitudes, then test blind mixed amplitudes and one out-of-class request; compare to exact online replanning with cached contracts.
- **Old-task retention check:** Replay A/Bᵢ/C through switches for unseen requests and ensure no train-time B answer or auxiliary feature is needed at dispatch.

#### 20. Make readiness renewable without a third resident feature (P)
- **Mechanism:** Once q takes service, useful C work must return p to certified readiness while leaving q's load-bearing representation intact. Admit the next cycle only after checking directed coverage on the new binding state.
- **Novelty vs nearest prior art:** #254 alternating renewal and EEP rank reintegration are known. The strict candidate is recurring second-default coverage at fixed feature/slot width while learning useful C, not a third parked replica or uncharged reset.
- **Cheapest first test:** Enumerate three two-default cycles with alternating lane ownership, compare against optimal one-cycle controllers with paid recertification, and include a cycle where C utility and renewal conflict.
- **Old-task retention check:** Track all installed A/Bᵢ/C and normal reliance after each renewal; charge refusal in any cycle that cannot safely restore coverage.

#### 21. Test a fault that changes only the next reader (I)
- **Mechanism:** Shadow-swap q's hidden norm or optimizer history while holding its public switch tag fixed. Compare actual effective edits and post-clear reads, not branch names.
- **Novelty vs nearest prior art:** #237's seam audit and relational non-interference already do this; it catches a falsely pre-certified transfer in this setting.
- **Cheapest first test:** Extend fixture H with a hidden scale that affects the next x increment but not tick-3 old scores; compare no scale read, transparent charged public read, and unsafe blind dispatch.
- **Old-task retention check:** Check A/Bᵢ/C immediately after dispatch and at the delayed reader under both hidden histories; count a leaking trace as invalid even if all current scores pass.

#### 22. Cross the two bets before attributing a win (I)
- **Mechanism:** Cross joint versus separate basin/edit training, hard versus absent normal reliance, and coupled versus dedicated transfer; keep fault timing, exact planner and resource ledger shared.
- **Novelty vs nearest prior art:** Factorial ablation is known; this rules out a win from using only the ordinary ready-park stack, only a hot spare, or unequal fault scope.
- **Cheapest first test:** Exhaust one fixed-width finite host family with fixtures R and H as unit cases, then test the cross on held-out recovery phases and B directions. Report paired coverage or cost frontiers at matched utility, not raw averages.
- **Old-task retention check:** Use the same independent A/Bᵢ/C judges and normal reliance lesions in every cell, including no-fault, both faults, refusal and extended post-clear runs.

## Ranked deeper questions

1. **Does joint training preserve any useful, reachable overlap once normal service must rely on the edited feature, and does it beat the best separately tuned stack at the same floor?** Start with R and cards 01–05, 09, 22. Match normal quality, C progress and width; test fresh requests and report where the floor provably forces separation. If the gain requires a dormant route or relaxed retention, stop.
2. **Can a coupled active q take over on the worst publicly adaptive second default without reopening the first write, breaking an old reader, or restarting the clock?** Start with H and cards 12–18. Matched active standby and exact same-host planning are essential. Break the certificate deliberately with shared faults, ambiguous tags and a non-atomic reader.
3. **Can one pre-certified handoff class serve unseen effects more cheaply than exact replanning with cached contracts?** Start with cards 10, 13, 14, 19 and 21. Test actual suffixes and hidden-state swaps, including post-clear residuals; report scope and proof maintenance costs, not just reuse counts.
4. **After repeated defaults, does actual old-task work renew the two-feature guarantee or merely fund covert repair?** Start with cards 03, 06, 11 and 20. Require repeated legal renewal at fixed width with no deleted-state reads and with the same per-tick A/Bᵢ/C floors; separate refusal, useful workload and recovery cost.

**Verdict:** Load-bearing redundancy and backup routing are not new by themselves. Keep a primitive candidate only if training changes what blind edits and mid-write second defaults are safely serviceable at fixed reliance and equal resources, or makes the same guarantee provably cheaper to maintain. The fixtures show why checking normal load, prefix progress and second-fault scope separately matters; they do not establish a win.

[parent]: https://github.com/manojbajaj95/cl/pull/254
[triage]: https://github.com/manojbajaj95/cl/blob/c00531ea25c93381bc3e3359725307daf4518393/reviews/flood-triage.md#L369
[ledger]: https://github.com/manojbajaj95/cl/blob/c00531ea25c93381bc3e3359725307daf4518393/reviews/idea-ledger.md
[glued]: https://github.com/manojbajaj95/cl/pull/224
[adaptive]: https://github.com/manojbajaj95/cl/pull/236
[standby]: https://github.com/manojbajaj95/cl/pull/256
[ofa]: https://arxiv.org/abs/1908.09791
[oml]: https://huggingface.co/papers/1905.12588
[anml]: https://www.alphaxiv.org/abs/2002.09571
[fat]: https://arxiv.org/abs/2011.05873
[filter]: https://arxiv.org/abs/1812.05506
[games]: https://www.alphaxiv.org/abs/0706.2619
[revive]: https://arxiv.org/abs/2602.21140
[eep]: https://arxiv.org/abs/2605.10670
