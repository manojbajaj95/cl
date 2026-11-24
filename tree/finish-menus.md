# Finish menus for live branch handshakes

**Status:** Ideas only; paper fixtures and proposed CPU tests, no training runs, implementation, or GPU. **Parent:** [Live branch handshakes](branch-handshakes.md) ([PR #212](https://github.com/manojbajaj95/cl/pull/212)). **Review seeds:** [Flood triage row 323](https://github.com/manojbajaj95/cl/blob/0a3fc72668fc1f4cd6fd73dc5cb8886514765787/reviews/flood-triage.md#L323), score 3: parent card 03 underwrites a late-bound completion menu; parent card 14 redirects paired residual momentum toward B while keeping the path for fresh B gradients open.

**Ledger read first:** The [idea ledger](https://github.com/manojbajaj95/cl/blob/0a3fc72668fc1f4cd6fd73dc5cb8886514765787/reviews/idea-ledger.md) requires ordinary old-task retention, simple budget-matched controls, and a combined idea that beats the best stack of its parts. Exact save/restore is not a primitive. Labels below are proposals, not reviewer verdicts: **P** = candidate reusable object or operation, **I** = improvement or audit rather than a new primitive; all have paper or CPU first checks, not pilot commitments.

## What is actually being promised?

- **Late choice, early liability.** Before branch 1 publishes a live, zero-B-gain move, branch 2 binds itself to execute one of several legal finishes by a common deadline. Only the information available when B arrives may select the finish. Reserve enough for the costliest admissible finish, including validation, dispatch and recovery under the declared fault model. With a single scalar resource and one finish consumed, that is the maximum, not the expected cost or the sum. With several resources, reserve the componentwise worst simultaneous requirements or demonstrate that the needed bundles coexist in a schedulable reservation. Concurrent handshakes share capacity only if joint feasibility is certified.
- **Nonempty for what the chooser can see.** For every reachable observation at B arrival, there must be a common finish safe under every state and future interleaving consistent with that observation and compatible with its B demand. It is not enough that each hidden state has a different legal finish. Refuse **before branch 1 publishes** if any allowed arrival, delay, failure, or invalidation can empty the menu. Treat no-show and outside-menu inputs explicitly: either exclude them with an enforceable admission boundary or cover them with a reserved safe finish that grants no B credit. Turning B away must not strand a live half-state. A freeze or old-version route is a paid alternative, not a live safety proof.
- **Two paths into the next update.** Keep both weights, merge rule, current predictions, schedule and counters fixed at the slot intervention. Change both branches' slots; preserve nonzero residual first moments rather than passing by erasing them. For fixed preconditioners, separate the residual-only update from the fresh-gradient increment. For Adam, where the denominator changes with the gradient, compare paired shadow updates from the same state with the actual gradient and with zero gradient, then measure the difference. Require signed useful response to fresh gradients over the shared horizon, not just nonzero update norm; follow real, nonzero-gradient suffixes once trajectories diverge. Rotate full second moments by congruence, or use signed permutations for diagonal slots; charge richer block storage and test any approximated rotation on the updates it actually produces.

**Common test discipline.** A is ordinary old-task evaluation, C an independently protected reader or slice, and B the new task. Retention floors apply at every served prefix, including faults and the deadline event; report held-out A/C after B and worst prefix separately from the checks used to construct a certificate. Match attained B when comparing retention (or say there is no common point), and compare B or admission at matched retention. Charge waiting time, held capacity even when unused, rejection, state and proof bytes, recovery, optimizer steps, probes and search. Same-budget controls get the same actions, observation times and failure model. Compare atomic switch, a deadline-aware [compositional shield](https://arxiv.org/abs/2410.10460) and exact contingent search on small hosts. A menu is already a contingent plan (and closely related to adjustable robust optimization); two-phase commit binds a commit decision, not by itself a promise that ordinary readers can safely see the half-state. On slots, grant [Adam](https://arxiv.org/abs/1412.6980), [Shampoo](https://arxiv.org/abs/1802.09568), [GEM](https://arxiv.org/abs/1706.08840), [OGD](https://arxiv.org/abs/1910.07104), [PCGrad](https://arxiv.org/abs/2001.06782), resets and preview-aimed momentum ([PR #207](https://github.com/manojbajaj95/cl/pull/207)) equally strong tuning. This is a targeted comparison, not a priority claim.

## Two exact paper fixtures, not evidence of a win

**A menu that costs 3 even when the cheap finish is chosen.** Branch 1 holds x, branch 2 holds (y,c), initially (x,y,c) = (0,0,0). A requires |x+y| ≤ 1, C requires |c| ≤ 1/2. A mandatory tick adds 1 to x after the common finish deadline. Branch 1 publishes x ← 1 before B is known: A and C still pass, and B gets zero because neither finish has executed. B can request `+` or `−`; it earns one only from the matching finish.

| Finish chosen on B arrival | Reserved execution cost | (y,c) written | A readout x+y just after finish → after tick | C readout |
|---|---:|---|---|---|
| `+` | 2 | (−1, 1/2) | 0 → 1 | 1/2 |
| `−` | 3 | (−2, −1/2) | −1 → 0 | −1/2 |

Capacity 3 admits both demands under a model that guarantees one finish by the deadline and excludes no-shows. Capacity 2 cannot admit the same domain: if `−` arrives its menu is empty, so refuse the first move. Likewise refuse if an allowed delay can make both finishes unavailable, or reserve an independently executable alternative. Without a finish the tick yields x+y = 2; after refusal it yields 1. A fixed finish can keep A/C safe but cannot earn both B rewards. The costs and rewards here are stipulated to expose the admission logic; equally capable contingent scheduling ties the fixture.

**A paired reorientation that does not mute any fresh gradient.** Use two heavy-ball branches with w₁ = w₂ = (0,0), m₁ = (2,0), m₂ = (−2,0), and each step `m ← m/2 + g; w ← w − m`. Merge by summing weights. A requires |x₁+x₂| ≤ 1/2 and C requires |y₁−y₂| ≤ 1/2. Rotate m₁ clockwise and m₂ counterclockwise by 90° so both are (0,−2), without changing either norm or any prediction. For two steps use g₁ = g₂ = (0,−1/2), the gradients of linear B loss −(y₁+y₂)/2. The untouched state gives merged y = 1 then 5/2; the paired state gives 3 then 11/2. A and C read zero on both trajectories. Rotating only one branch gives |x₁+x₂| = 1 at the first step and fails A. At a fixed state the update increment from fresh g instead of zero g is exactly −g in all arms, so the extra B movement in the paired arm comes from redirected residuals. An oracle can simply choose these two rotations; the fixture establishes neither a new search method nor a win over equivalent protected momentum steering.

## Idea cards

### Menus for a genuinely live first move

#### 01. Bind a menu, not a single finish (P)
- **Mechanism:** Store one binding deadline, a finite map from admitted B observations to writes, and a worst-case reservation before publishing the zero-gain write. Retire the reservation only when a selected finish becomes live; refuse publication if any supported observation would have no legal finish.
- **Novelty vs nearest prior art:** This is the reviewer seed itself, not a new result beyond parent card 03 or general contingent planning. Candidate primitive: a completion obligation exposed to the learner, distinct from choosing an unbound plan later.
- **Cheapest first test:** Exhaust both arrivals in the menu fixture, add an unlisted B and a deadline miss, and compare fixed parent completion, cached full plans and an exact shield with the same capacity and wait.
- **Old-task retention check:** Read ordinary A and C at the half-state, finish, and mandatory tick, including after refusal; an unlisted B must never strand the half-state.

#### 02. Certify choices for indistinguishable arrivals (P)
- **Mechanism:** Compute the intersection of legal finishes over each set of hidden states that B's arrival message cannot distinguish; reserve for a finish from that intersection, not from the union. Allow an extra query only if its worst-case time is booked before publishing.
- **Novelty vs nearest prior art:** Belief-state planning already uses information sets; the candidate object is a query-priced certificate for whether an already visible branch prefix can be underwritten.
- **Cheapest first test:** Use two histories with identical observations and disjoint singleton finish sets; add a one-bit separating query and sweep its latency. Compare full cached policies and observation-aware exact planning with the same bit and time budgets.
- **Old-task retention check:** Enumerate ordinary A/C for both histories at every event; show a union-based policy actually breaks a reader, not merely a certificate predicate.

#### 03. Keep a neutral finish for a B that never comes (I)
- **Mechanism:** Reserve a B-independent finish with no B credit and a latest-start time. Dispatch it if B remains absent; once dispatched, do not admit a tardy B against the retired menu.
- **Novelty vs nearest prior art:** Deadline fallback and default actions are standard; this improves the admissible arrival model without relabeling a neutral settlement as learning.
- **Cheapest first test:** Add a no-show and an arrival at the last dispatch tick to the fixture. Compare unconditional default, freeze, and atomic staging with identical deadlines and work.
- **Old-task retention check:** Run A/C including simultaneous arrival and timer events; test the branch that wins each ordering and the tick after it.

#### 04. Reserve bundles, not scalar prices (P)
- **Mechanism:** Underwrite a joint set of execution-time, version-lease and memory reservations so each selectable finish has a realizable bundle, including on failover. No reservation is reclaimed while an allowed trace can still exercise it.
- **Novelty vs nearest prior art:** Multiresource scheduling already provides feasibility checks; the candidate is an embeddable bundle certificate for a branch menu whose legal endpoints themselves depend on version leases.
- **Cheapest first test:** Enumerate two finishes, one memory-heavy and one time-heavy, with a lease expiring between slots. Compare componentwise reservation plus exact scheduling and a fixed finish at matched resource ceilings.
- **Old-task retention check:** Read A/C while serving the half-state and after each allowed lease/failure order; reproduce a failure from a scalar-budget admission.

#### 05. Let live menus share capacity only under an arrival-cut proof (P)
- **Mechanism:** Bind several half-moves together only if every permitted joint B arrival pattern has a feasible assignment to reserved executors; store a cut witnessing why correlated demands cannot overload a deadline.
- **Novelty vs nearest prior art:** Hall-style matching and robust scheduling already cover assignment; beyond parent card 04's fixed-work overlap the candidate certificate underwrites task-dependent writes, not just named jobs.
- **Cheapest first test:** Enumerate three two-option handshakes on two executors with one forbidden arrival pair; re-enable the pair as a negative control. Compare per-menu maxima and an exact joint scheduler with identical peak resources.
- **Old-task retention check:** Serve ordinary A/C between completions and on the overloaded trace; require refusal before any prefix that could become stranded.

#### 06. Delete an option only with a checked replacement (P)
- **Mechanism:** An ordinary update may invalidate a finish while branch 1 is live only if the same transaction preserves coverage and a reservation for the replacement menu at the original deadline.
- **Novelty vs nearest prior art:** Make-before-break already covers switching assets; the candidate operation changes the live option coverage without making a fresh promise or extending the deadline.
- **Cheapest first test:** Have a third update retire one version token; first permit, then remove a substitute for the affected B class. Compare blocking version locks and complete recertification at the same validation and latency budget.
- **Old-task retention check:** Read A/C during option replacement and with a B at the invalidation boundary, including the denied update case.

#### 07. Compile a continuous menu into choices with certified overlap (I)
- **Mechanism:** Cover a continuous B descriptor with regions carrying fixed feasible finishes or certified local maps. Overlap at boundaries by enough to handle known descriptor error; bound the worst cost over the entire cover.
- **Novelty vs nearest prior art:** Explicit MPC and adjustable robust optimization already partition observations into policies; this improves how a live handshake represents continuous demand under noisy observation.
- **Cheapest first test:** Solve a piecewise-linear interval example exactly and introduce a narrow coverage hole. Compare uniform gridding and exact policy synthesis under equal storage and checking budgets.
- **Old-task retention check:** Evaluate ordinary A/C across the certified domain and exactly at cell boundaries using realized finishes, not the estimated descriptor alone.

#### 08. Separate finish legality from write placement (P)
- **Mechanism:** A menu entry binds a required effect and checked write footprint but not a particular executor or replica. A replacement can execute that entry only if it holds predelegated authority over the same version and can still meet the deadline.
- **Novelty vs nearest prior art:** Failover and parent card 05's single-action substitution are close. The candidate interface separates the choice of semantic effect at B arrival from where that effect is authorized to execute.
- **Cheapest first test:** Enumerate an executor failure before and after B selects an entry; introduce one replica that cannot implement the rare finish. Compare full replication and preassigned failover at matched capacity and state bytes.
- **Old-task retention check:** Read A/C between failure and dispatch and after the deadline; include stale and duplicate finish attempts in the admitted fault model or rule them out explicitly.

### Slot pairing that steers old momentum without blocking fresh B

#### 09. Steer the residual and certify the gradient channel separately (P)
- **Mechanism:** Search paired norm-preserving slot orientations at fixed weights. Constrain the residual-only old drift and require useful signed fresh-gradient response as well as retained B utility over a short shared suffix; retain feasible first moment norms instead of resetting.
- **Novelty vs nearest prior art:** This is parent card 14's reviewer seed. GEM/PCGrad change the update or gradient, while preview-aimed momentum already steers residuals; the candidate operation jointly preserves an old readout and a distinct fresh-gradient channel.
- **Cheapest first test:** Start with the heavy-ball fixture, then use short quadratic suffixes. Compare independent choices, GEM/PCGrad, reset, repeated projection and the #207 preview at equal gradient calls, with retention matched on realized B.
- **Old-task retention check:** Measure ordinary A/C throughout each suffix, including one with reversed B order; require success after nonzero B updates, not only at the intervention.

#### 10. Put a lower bound on adaptive gradient transmission (I)
- **Mechanism:** Reject orientations that pass an old-drift screen only by inflating adaptive denominators in B directions. Compare actual nonzero-gradient steps with zero-gradient shadows from the same slots and use a signed lower bound on their difference along admitted B descent directions.
- **Novelty vs nearest prior art:** Preconditioner conditioning and directional derivative bounds are known; the gain would be a better test for false slot wins under Adam's nonlinear denominator, not a new optimizer.
- **Cheapest first test:** Exhaust two-axis diagonal swaps with highly unequal variances and sweep B gradient scale. Compare exact shadow auditing, a denominator threshold and a reset plus projection at equal probe cost.
- **Old-task retention check:** Replay ordinary A/C after each accepted swap and fresh step; include cases with excellent A/C but negligible B transmission as rejected, not successful retention wins.

#### 11. Buy residual cancellation on different readers without using B's axis (P)
- **Mechanism:** Find orientations whose residuals cancel in distinct A and C observation directions but reinforce in a shared B direction; require each preconditioner's response to fresh B to be measured before merging as well as after.
- **Novelty vs nearest prior art:** Parent card 15 assigns reader directions and GEM projects gradients. The candidate object is a two-branch residual coupling that preserves useful branch-local gradient paths, not merely cancellation of the merged step.
- **Cheapest first test:** Enumerate signed permutations in a three-axis quadratic with two nonparallel older readers and one B direction. Compare exact joint search, one-branch steering and independent protected optimizers under equal state and probe budget.
- **Old-task retention check:** Measure both old readers at every prefix, including a merge perturbation and an unseen old input aligned with their combined directions.

#### 12. Orient for a suffix family without pretending to know its next gradient (P)
- **Mechanism:** Certify a paired residual orientation against a set of short B gradient sequences; record the smallest early horizon at which either old safety or fresh B transmission can fail rather than promising indefinitely.
- **Novelty vs nearest prior art:** Parent cards 17 and 18 already test decay and unseen families; the candidate certificate couples both to a causal prefix bound for the fresh channel, not an oracle gradient preview.
- **Cheapest first test:** Enumerate two quadratics with identical first gradient and diverging second gradients; vary momentum decay. Compare a lookahead controller with the same preview and a retention-matched one-step reset/projection stack.
- **Old-task retention check:** Score ordinary A/C at each step and after expiry; include a held-out third suffix and permit abstention rather than silently extending the promise.

#### 13. Keep a direction useful through both signs of B (I)
- **Mechanism:** Use a paired orientation only where its residual contribution does not dominate an opposing fresh gradient; declare the gradient scales and sign reversals under which the realized update remains descent for B.
- **Novelty vs nearest prior art:** Momentum restart methods already address overshoot. This audits paired steering against useful B learning when the first gradient is not representative.
- **Cheapest first test:** Use an alternating-sign scalar B gradient with a second old axis. Compare ordinary momentum tuning, adaptive restart and repeated projection at equal steps and gradient probes.
- **Old-task retention check:** Test A/C before and after the sign flip and after the momentum tail; compare retention only at common realized B when such a point exists.

#### 14. Pay for non-diagonal slot blocks only where they preserve transmission (I)
- **Mechanism:** Allocate the fixed byte budget to a small full second-moment block if the best diagonal approximation would close a necessary B channel; keep the rest of the optimizer unchanged.
- **Novelty vs nearest prior art:** Shampoo and parent cards 10–11 already motivate richer blocks; this evaluates a fresh-gradient criterion for deciding which induced off-diagonals justify their cost.
- **Cheapest first test:** Compare a rotated two-axis covariance and a cost-matched diagonal or low-rank preconditioner on nonzero-gradient quadratic steps, including exact transformed proposals and proposals after rounding.
- **Old-task retention check:** Compare A/C at each quantized step, including the old direction with the largest approximation error, at matched realized B.

#### 15. Stress the distinction between proposal mixing and pooled Adam (I)
- **Mechanism:** Hold weights and coefficients fixed and test the same paired orientation under two declared optimizers: mix their independently preconditioned steps, or pool raw slots using a specified rule and execute one Adam instance.
- **Novelty vs nearest prior art:** Parent card 12 already separates these rules. This audit adds a nonzero fresh-channel test in each; a gain in one is not evidence in the other.
- **Cheapest first test:** Try signed swaps with unequal variances and two nonzero B steps; compare per-rule tuned resets and joint slot search with the same storage, epsilon, counter and update rules.
- **Old-task retention check:** Report A/C prefix floors for each merge independently, including counterexamples where old cancellation transfers poorly across composition rules.

#### 16. Form a reusable interface between residuals and old reader contracts (P)
- **Mechanism:** Export a bound on the joint residual response of admitted orientations and a separate lower bound on B's fresh response. Compose certificates only while versioned reader maps and preconditioners satisfy the declared error budget.
- **Novelty vs nearest prior art:** Assume-guarantee contracts and OGD subspaces are close; a candidate slot interface lets the same orientation be checked against a changed set of reader contracts without storing raw old-task gradients or claiming arbitrary transfer.
- **Cheapest first test:** Derive bounds for two linear readers, then swap one reader and compare certificate reuse with full recertification and a stored basis at equal bytes and probes.
- **Old-task retention check:** Test ordinary A and both versions of C, including a reader change just beyond the declared error bound; require refusal on that change.

### Does putting slots in the menu change what's achievable?

#### 17. Reserve a finish as a write plus a slot contract (P)
- **Mechanism:** Each late B choice takes one versioned pair: a branch-2 write and an orientation whose short suffix is valid from that endpoint. Reserve the costliest complete pair; do not substitute a cheaper write or slot plan unless the pair remains certified.
- **Novelty vs nearest prior art:** Parent card 19 uses a slot-only window and contingent planners can already enumerate pairs. Candidate primitive: a typed finish whose endpoint and fresh-gradient guarantees are inseparable under independent write and slot authorities.
- **Cheapest first test:** Enumerate two B arrivals with different legal write/orientation pairs and add a crossed pair that breaks under the first B gradient. Compare exact joint search and a menu scheduler stacked with the best independently tuned protected optimizer at equal capacity.
- **Old-task retention check:** Read A/C from the actual half-state, both valid finishes, and the first two nonzero B steps; show where the crossed pair fails.

#### 18. Spend a delayed B observation to narrow the slot choice (P)
- **Mechanism:** At arrival, branch 2 binds a legal completion immediately but, where certified and reserved, the completion has a hole for the orientation supplied by a paid B-gradient probe before the same deadline. Never let the probe turn a mandatory finish into a hope.
- **Novelty vs nearest prior art:** Parent card 20 binds a gradient-use budget; this candidate discharges an orientation hole with an observation while preserving finish legality for every possible probe result. Adjustable policies with recourse are the expected tie.
- **Cheapest first test:** Enumerate two indistinguishable B arrivals with opposite probe directions and a probe timeout. Compare cached fully specified scripts and a stacked preview optimizer with identical probe access and waiting time.
- **Old-task retention check:** Check A/C while the probe is outstanding, after each finish and B suffix, and on a timeout where the reserved neutral finish provides no B credit.

#### 19. Let early slot-only service earn its place without counting it as B gain (P)
- **Mechanism:** Before B arrives, serve ordinary traffic from a live half-state with identical current predictions but altered slots. The finish menu covers required updates triggered by that traffic, including a declared maximum number of ticks before B arrives.
- **Novelty vs nearest prior art:** Parent card 19 uses a first-tick deadline; the candidate is an underwriting object for a whole bounded family of reader-triggered suffixes. Switched-system reachability and a scheduler with paid old-version routing are close controls.
- **Cheapest first test:** Put zero, one or two auxiliary updates between publication and B; use an example where two updates empty the menu unless they were underwritten. Compare atomic pre-staging plus the best slot control at equal ticks, latency and storage.
- **Old-task retention check:** Read A/C on the genuine exposed version at every auxiliary tick and after B; test refusal before exposure when allowed tick count exceeds coverage.

#### 20. Exchange slot authority without changing what the finish owes (P)
- **Mechanism:** If branch 2 loses the ability to mutate an optimizer shard, replace its menu with one using the surviving slot authority only when the new menu covers all promised B classes and preserves their fresh response bounds at the original deadline.
- **Novelty vs nearest prior art:** Failover and substitution are known; the candidate operation trades distinct optimizer-state authorities under a preserved behavioral contract rather than copying a failed executor's slots.
- **Cheapest first test:** Enumerate three signed permutations across two shards, then remove one shard's write right. Compare precomputed fallback scripts and a reset-capable scheduler at equal recovery and capacity costs.
- **Old-task retention check:** Use a C reader sensitive to the surviving shard; check A/C before failover, on the substitute suffix, and on an authority loss that requires pre-publication refusal.

#### 21. Test for an interaction rather than adding two independent gains (I)
- **Mechanism:** Look for B classes where pairing changes which finishes are feasible at fixed old floors, and late selection changes which orientation can be used. Factorially vary the two features; test against the best stack, not just either part alone.
- **Novelty vs nearest prior art:** Factorial comparisons are standard. This is the ledger's test for a combined operation, not itself a new primitive.
- **Cheapest first test:** Enumerate a two-write, two-orientation toy and a separable version with the same individual gains. Give the scheduler and protected optimizer the same observations, actions, deadlines and reservation costs; compare at the same attainable A/C and B operating points.
- **Old-task retention check:** Measure ordinary A/C at every served prefix and on independent suffixes; a gain that disappears when retention is matched counts as no interaction.

#### 22. Produce a witness that the menu cannot be underwritten (I)
- **Mechanism:** Return a reachable B observation and a time, resource, old-reader or fresh-gradient violation covering every finish in the menu. If exact search is too expensive, label a failed sufficient check as unknown rather than impossible.
- **Novelty vs nearest prior art:** Unsatisfiable cores and parent card 22's impossibility audit already exist; this improves diagnosis when the write menu is legal in isolation but all its slot suffixes are unusable.
- **Cheapest first test:** Exhaust small write/slot pairs with one deliberately unserviceable observation and one merely hard to certify; compare exhaustive search and separate write/slot verifiers at equal checks.
- **Old-task retention check:** Reproduce the actual A/C failures named by the witness; where only B transmission fails, report that separately and verify A/C still works after refusal.

## Ranked deeper questions

1. **Can a late-bound live menu beat an equally capable contingent scheduler plus atomic staging?** Start with cards 01, 02 and 05. Require a real zero-gain half-state, a missed-finish trace that harms old behavior, and proof that all admitted traces exclude it. Vary when B becomes observable, price the resource maximum and include out-of-domain/no-show cases. If cached plans or atomic staging tie under the same action and latency budgets, call it scheduling, not a new learning primitive.
2. **Does paired reorientation beat protected momentum steering at matched realized retention without weakening fresh B learning?** Start with cards 09–13 and nonzero-gradient suffixes. Separate residual lift from fresh response, compare reset, preview, GEM/PCGrad and repeated projection, and report whether a gain survives both mixing rules or only one. A zero-gradient success or a rotation explainable by an optimizer coordinate relabel is not enough.
3. **Does slot pairing buy a finish that a scheduler with the strongest slot baseline cannot offer?** Use cards 17, 18 and 21. Show an interaction on the same observations and action budget, with A/C safe through the live prefix and matched realized B across controls. Treat independent wins from better staging and better momentum as separate results.
4. **Can underwriting remain cheap once information and authority are partial?** Use cards 04–08, 16 and 20. Shift held-out B arrivals and fault schedules; compare proof bytes, checking, false refusals and held capacity against exact policies and paid fallback. Safety that depends on an unavailable distinguishing observation is not coverage.

**Verdict:** Keep both as conditional candidates. Start with refusal under a real availability failure and a paid scheduler that can tie the menu witness; separately try to falsify paired slot steering with nonzero-gradient, retention-matched controls. Keep the combined idea only if a certified live prefix and a preserved fresh-gradient path yield something the stacked controls cannot reproduce.
