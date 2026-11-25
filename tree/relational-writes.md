# Relational provisional writes

**Status:** Ideas only; no implementation, training runs, or GPU work. **Parent:** [Joint effect agreement](joint-effect-agreement.md) ([PR #265](https://github.com/manojbajaj95/cl/pull/265)), card 02. **Review seed:** [Flood triage, row 381](https://github.com/manojbajaj95/cl/blob/d060aace22c59ef1bc73c729d1144fc602e2013f/reviews/flood-triage.md#L381), score-3 idea: carry a linear coupling between outputs in the live weights, not a point, so a second view agreeing up to scale can still commit. **Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/d060aace22c59ef1bc73c729d1144fc602e2013f/reviews/idea-ledger.md).

## Keep the relation; let independent evidence supply the scale

**Verdict: a candidate write primitive, not a new constraint solver.** View 1 writes a nonzero direction (or a higher-rank coupling) into the live weights. It does not authorize or serve any particular B delta. Ordinary old-task work can intervene. View 2 independently proposes a *joint* B effect; only then may the learner commit its magnitude. For a rank-one relation the contract is `d = αu`, `α > 0`, where `u` is read from the pending weights and only its oriented ray matters. A linear equality such as `d₂ − 2d₁ = 0` by itself also admits zero and the opposite sign; neither is consent. For higher rank, require `L d = 0` **and** declared orientation and utility conditions. Noise tolerance, if any, is fixed before blind jobs. In every case the independently proposed effect must be semantically supported, finite, jointly realizable and safe. Never project an incompatible View 2 proposal onto the relation and treat the projection as confirmation.

**Nearest comparisons.** [Set-membership identification][smid] already stores and intersects constraints; [AND-mask][andmask] agrees on parameter-gradient signs, not output ratios. [Relational Knowledge Distillation][rkd] transfers relations to a student, [FROMP][fromp] protects prior function values, and [ROME][rome] realizes a particular edit with a rank-one update. [Orthogonal Gradient Descent][ogd] protects outputs using projected gradients; [Relation parks (PR #255)][parks] preserve a relation in weight/optimizer state during bounded old work, not a relation among possible effects that a later view can independently spend. These are nearest comparisons, not a fresh systematic prior-art search. A latent vector, scale invariance, output constraints, and algebraic projection are not novelty claims. The bet is that storing the relation **as part of the live actuator** preserves more usable independent consent per unit of memory or work than writing a point and/or keeping the relation as data. Even a clean scale-transfer win over an exact point is a null if a normalized **live point direction** or a compact external ray achieves the same result at matched cost. The ledger's effect-class distillation and coded recovery of sparse damage are not revived here: no teacher-matching objective and no assumption that forgotten items are sparse.

### First-test contract

- Freeze the B output chart (e.g., signed target-vs-rival gaps on canonical queries), epsilon, expiry, old schedule, read permissions and legal write menus. Calculate B effects from the state *after* the same due old work and before any commit. Admit only useful scales allowed by both views where View 1 has independent bounds; never infer an unrestricted ray from one observed point without evidence that the direction generalizes. Recheck achieved finite joint effect and old floors, not just a tangent prediction. On ambiguity, expired evidence or unsafe magnitude, abstain without a reset or extra rescue work.
- Blindly interleave same-ray/different-scale proposals, same-sign wrong ratios, opposite and near-zero proposals, and **on-ray junk** (passes geometry but lacks independent B support). Match norms, old-task starting margins and prior-driven alignment where possible. Require a second-view lawful semantic check independent of the stored relation and evaluate against held-out B behavior; include a filler/shared-prior adversary. When true and junk views are observationally identical at decision time, report non-identifiability or abstain, not perfect discrimination from geometry.
- Strongest control: identical provisional write, same due old work, best **quantized normalized ray or factored relation buffer** at equal peak bytes, and exact post-due fitting/actuation with the same observations and semantic checks. Also include the #252 point write at matched provisional B service, normalized live point, #241 marginal matching, AND-mask, and no-write-with-due-work. Report an oracle/full-information ceiling separately. Count carrier weights/slots, frozen decoders, metadata, external buffers, probes, legal action scans and update compute. Include a carrier-erasure control paired on pre-confirmation B output and old reads. Compare useful commitments and false confirmation at matched costs, prequential B service and latency; identical old work means identical data, timing and optimizer rule, not necessarily identical parameter deltas.
- Old-task rule for every card: run A (including due A₁ and untouched A₂) and previously committed C on held-out, starting-margin-matched items at provisional exposure, after due work, at commit/abstention/expiry, and at matched returns 1, 8 and 64. Report itemwise gaps and success, including near-boundary items. Allow no hidden debt: require acquisition-anchored floors and A₁ repayment to paired no-write parity. Cards add specific retention risks to this common check.

### W13 — exact scale selection with a tied buffer, not a learning result

Use weights `(p,q,r,s,g,z)`, live direction `u = (p−q,r−s)` and B read `y_B = g u`. Old reads are `A₁ = p+q`, `A₂ = r+s` and `C = z`. Start at `(1/2,1/2,1/2,1/2,0,3)`; View 1 shifts opposite members of the two pairs to `(3/4,1/4,1,0,0,3)`. This leaves all exposed reads identical to no-write, but realizes `u = (1/2,1)`. The due A₁ loss is `½(A₁−2)²`, with SGD step size `1/2`; it increases both `p,q` by `1/2`. So A₁ goes `1 → 2` in both arms, A₂ stays `1`, C stays `3`, B is still `(0,0)`, and the live `u` stays `(1/2,1)`. No-write still has `u = (0,0)`.

Let View 1 license positive scales `0 < α ≤ 1` on this representative and freeze the legal gate interval `[0,1]`. A lawful and independently supported View 2 proposing `(1/4,1/2)` matches with `α = 1/2`; setting only `g = 1/2` realizes it without changing A₁/A₂/C. The exact point `(1/2,1)` would refuse. Marginal intervals accept `(1/4,3/4)` but the ray refuses it (determinant `1/8`); it also refuses `(-1/4,-1/2)` by orientation and `(3/4,3/2)` by scale. On-ray junk proposing `(1/4,1/2)` has the **same** determinant, orientation and scale as the genuine offer: only separately provided support can distinguish them. A two-bit tag would suffice for a toy menu of three fixed representatives (null, slope 2 and slope 1/2) with shared known scale bounds; the exact buffered control can tie using the same actuator. The fixture stipulates coordinates, old-update gradients orthogonal to the carrier, and independent support; it shows no learning or memory advantage.

## Idea cards

### 01. Spend a live ray at a new magnitude — seed / primitive candidate
**Mechanism.** Use a shared weight contrast to set the B actuator's direction while a closed gate serves no unconfirmed effect. View 2 spends only the independently justified scale by opening the gate proportionally.
**Novelty / control.** A reusable pending actuator, not a rank-one target edit as in ROME. W13 alone ties a normalized point or buffered ray; the candidate is coupling a durable pending relation to actuation without paying twice to store and realize it.
**Cheapest first test.** Extend W13 to multiple slopes, hidden scales and wrong ratios, with identical due work and equal-byte compressed controls; score correct spends, rejects and actuator fitting cost separately.
**Old-task retention.** Check paired A₁ repayment and held-out A₂/C gaps across all gate values, including the largest admitted scale.

### 02. Transport an allowed scale interval, not just a direction — primitive candidate
**Mechanism.** Encode two endpoints of one authorized segment using two live responses of the same actuator; common drift moves the raw endpoints, but only the calibrated width and origin license a spend.
**Novelty / control.** Standard set-membership bounds already reject extrapolation. The candidate is a weight-carried admissible interval whose endpoints are also executable after ordinary updates; compare a ray plus two quantized scalars and a two-point live cache.
**Cheapest first test.** Blindly shift actuator gain between views; alternate near-endpoint offers inside and outside the permitted interval with the same ratio. Fail if buffering is as accurate and cheap.
**Old-task retention.** Compare A/C at both executable endpoints and at refusal just outside each endpoint; the smaller old margin, not the mean, limits the interval.

### 03. Use several independent generators without laundering their signs — primitive candidate
**Mechanism.** Let multiple pending live actuators represent a cone; accept an independently proposed effect only with nonnegative coefficients in a legal joint realization.
**Novelty / control.** Nonnegative least squares solves cone membership. The candidate is a composable set of provisional weight writes that assemble one consented effect without ever serving the unmatched generators. Compare exact buffered cone fitting and independently spent rays.
**Cheapest first test.** A 3-output, 2-generator linear head where a true proposal needs both directions and a matched fake lies in the span but needs a negative coefficient. Use overlapping A features instead of entirely disjoint B heads.
**Old-task retention.** Test A/C at joint spend, since separately safe generator values can jointly cross an old-task margin.

### 04. Store what must cancel in a live annihilator — primitive candidate
**Mechanism.** Reserve live readout rows for `L`; query `L d` on the proposed output delta to check cancellations, using the same rows as constraints on the finite actuator update.
**Novelty / control.** A nullspace basis and OGD projection are standard. The candidate is dual use of ordinary live readouts as pending-relation witnesses and as commit constraints. Compare a compact buffered basis chosen on the smaller primal or dual side.
**Cheapest first test.** Compare primal generators and annihilators on 4-output rank-3 cases with the same rank, byte cap and actuator. Include sign-matched violations visible only in a three-output combination.
**Old-task retention.** Check A/C served by the reserved rows while pending and after they are reused; include old items with weak evidence on those rows.

### 05. Make the relation readable after independent gains change — primitive candidate
**Mechanism.** Pair each pending carrier coordinate with a reference that experiences the same lawful gain. Read ratios in the frozen original chart only where the reference stays nonzero and its transport is identified.
**Novelty / control.** Ratiometric calibration is standard. The candidate is sharing gain references with live B actuators so normal old work can alter channels without requiring View 1 again. Compare buffered original-chart ratios plus the same calibration probes.
**Cheapest first test.** Let a due old task rescale two channels unequally; include a matched state with identical reference reads but a different action on B. Demand refusal in the aliased case.
**Old-task retention.** Measure uncalibrated A/C service as well as normalized gate reads so the reference cannot conceal real degradation.

### 06. Confirm a relation without a shared visible coordinate — primitive candidate
**Mechanism.** View 1 writes a relation over an overlapping query graph. View 2 measures only endpoints of a path; use intermediate live weights to predict their ratio, but require an extra independent observation to disambiguate if the path lacks rank.
**Novelty / control.** Eliminating latent variables is standard factor-graph algebra. The candidate is a cross-view query usable directly from the provisional weight graph, without storing or replaying the missing endpoints. Compare sparse buffered elimination with the same query budget.
**Cheapest first test.** Four-node chain with transported edge ratios; contrast a uniquely implied endpoint relation with a fork that agrees locally but leaves endpoint effects unidentifiable.
**Old-task retention.** Score held-out A/C at internal nodes as well as endpoints; refusal must not leave an intermediate update exposed.

### 07. Keep an exchange rate across different output units — improvement
**Mechanism.** Declare an explicit chart map from heterogeneous outputs (e.g., success gap and cost) to a common scale, and run the live relation check in that fixed chart with unit-aware tolerance.
**Novelty / control.** Dimensional analysis and weighted residuals are standard; this improves a gate rather than creating a new object. Compare raw cosine, weighted buffered constraints, and norm-matched fakes.
**Cheapest first test.** Rescale a cost output by 100, leaving the underlying tasks unchanged. Test whether true, near-ray and wrong-ratio offers have the same decisions across units; no pilot if simple calibration ties.
**Old-task retention.** Check old costs in physical units and old success separately; do not let unit conversion absorb a real violation.

### 08. Require a causal witness for two views on the same ray — primitive candidate
**Mechanism.** Use a bounded alternate B query whose response changes if View 2's evidence is replaced by matched filler. Require support under the original evidence and loss of that support when swapped, independently of ray membership.
**Novelty / control.** Counterfactual checks and filler controls are known. Candidate operation: combine a fixed live effect relation with an evidence-substitution test that permits scale consent without allowing a shared prior to vote twice. Compare buffered ray + identical substitution check and semantic-only gating.
**Cheapest first test.** A compositional B rule with true and filler views producing exactly the same proposed vector. A single legal held-aside query should separate the two; include a world where it cannot, requiring abstention.
**Old-task retention.** Hold A/C query frequency and compute fixed, including tasks powered by the same prior, to catch accidental suppression of valid old behavior.

### 09. Ask the one output that neither ray can fake — improvement
**Mechanism.** Use the geometry of the carried relation and its nearest rivals to choose a lawful confirmation query with the largest smallest separating residual, conditional on scale.
**Novelty / control.** Active experimental design already optimizes discriminating queries. This reduces probe cost for a relational write; compare a buffered relation plus the same query policy.
**Cheapest first test.** Three outputs where all candidate relations agree on two observed projections. Compare one chosen probe to a random and to a highest-variance probe, with a case no legal probe can disambiguate.
**Old-task retention.** Keep the ordinary A/C service schedule fixed; count probe time as latency rather than silently deferring old examples.

### 10. Localize which provisional relation ordinary work erased — primitive candidate
**Mechanism.** Give the same constraint two live realizations that are affected differently by due old updates. A disagreement invalidates whichever realization lacks an independent anchor; never repair from the other merely because it agrees with View 2.
**Novelty / control.** Replication and parity checking are known. Candidate operation: a pair of ordinary executable readouts that can isolate loss of *specific pending consent*, not sparse forgotten facts. Compare redundant buffered constraints and same-byte duplicated point carriers with anchors.
**Cheapest first test.** Apply one of two old steps that leaves A gain identical but erases a different live realization, plus a correlated eraser that destroys both. Blindly test localized refusal and correlated-failure abstention.
**Old-task retention.** Match A debt and inspect C sharing each replica's features; no apparent robustness may rely on freezing work on one side.

### 11. Allow relation drift only within the evidence class — primitive candidate
**Mechanism.** Carry a narrow set of admissible rays represented by two executable boundary directions. Ordinary work may rotate a chosen readout inside the set, but only the independently supported intersection licenses a spend.
**Novelty / control.** Robust cones and set intersections are old; the bet is that live boundary actuators can absorb drift without preserving an exact representative or inventing evidence beyond the original set. Compare the exact buffered cone and a fixed-ray tolerance band.
**Cheapest first test.** Alternate old updates that rotate the center versus updates that move one boundary outward. Reject same-sign offers just beyond the original interval, even if the new live cone contains them.
**Old-task retention.** Sweep A/C at the two edges and with center-to-edge spends; invariance of the center alone is not sufficient.

### 12. Transfer the direction across a lawful width change — primitive candidate
**Mechanism.** During an already scheduled split, duplication or merge, move the pending B direction to the successor channels through the same coordinate map used for old functionality. Require the map to be injective on the admissible B directions, not on all parameters.
**Novelty / control.** Network morphism/Net2Net preserves existing functions. The candidate transports an *unspent* relation that is invisible to the old-task equivalence test. Compare a frozen carrier and a buffered relation re-realized after morphism.
**Cheapest first test.** Two small linear layers with a split that preserves the ray, and a merge that preserves all old outputs but aliases two distinct pending rays. Blind confirmation must refuse at the alias.
**Old-task retention.** Audit old service before and after the morphism and on near-boundary items not used to define the map.

### 13. Choose a safe amplitude without squashing a second view into agreement — improvement
**Mechanism.** Compute a legal amplitude interval from finite A/C margins, intersect it with both views' *independent* scalar permissions, and spend the largest supported value; if View 2 authorizes only one unsafe scale, abstain.
**Novelty / control.** Constrained line search already chooses a safe step. The improvement is the explicit separation of evidence from safety; compare buffered ray plus exact safe line search and post-hoc clipping.
**Cheapest first test.** Give the same proposed scale to two offers, only one of which independently licenses a smaller alternative. Check that the other is refused rather than spuriously confirmed by clipping.
**Old-task retention.** Include a small-margin A/C item with an interior ReLU crossing so an endpoint-only audit would miss the damage.

### 14. Let fresh corroboration narrow a live relation without a commit — primitive candidate
**Mechanism.** Treat a valid partial view as a restriction on the pending relation, not as a spend. Rewrite live basis directions to preserve the intersection, then let a later independently sufficient view select a nonzero effect.
**Novelty / control.** Recursive set-membership estimation already narrows feasible sets. The candidate is an executable in-place restriction of a pending actuator, with no served provisional B delta and no reread of retired views. Compare incremental QR and a compact buffered intersection.
**Cheapest first test.** In three outputs, start with a plane; the second view narrows it to a ray but gives no scale. Test a third offer on the ray versus an equally plausible offer on a retired direction.
**Old-task retention.** Check A/C after narrowing even though B is still unserved; a pending-only rewrite can still damage old outputs.

### 15. Spend one direction without consuming another — primitive candidate
**Mechanism.** In a pending cone, allow a completed corroboration to spend one direction while retaining eligibility for a disjoint direction, with no double counting of the spent direction as later evidence.
**Novelty / control.** An incremental basis update or transaction ledger already marks a direction spent. The candidate is a live readout whose residual pending actions survive without copying already committed outputs into evidence. Compare buffered cone with explicit spent IDs and two separate slots.
**Cheapest first test.** Two independent directions, then a valid fresh offer for the unspent direction and a rephrased repeat of the spent one. Score duplicate refusal and subsequent B service at equal peak bytes.
**Old-task retention.** Recheck A/C and the first newly committed B skill as an old task after the second spend and after expiry of the remainder.

### 16. Detect a wrong association when two pending relations share weights — primitive candidate
**Mechanism.** Superpose two pending relations in shared weights only if predeclared readout queries can isolate them. Require View 2 to match the addressed query as well as the ray, so swapped addresses cannot corroborate each other.
**Novelty / control.** Keyed associative memory and low-rank superposition already share storage. The candidate is independent address and geometric consent for live actuators that can interfere at commit. Compare keyed factored buffers with the same readouts and byte count.
**Cheapest first test.** Cross two tasks' View 2 addresses at matched scale, angle and old margin, including an alias with identical readouts where the system must abstain.
**Old-task retention.** After each spend, test the older of the two B tasks once committed, as well as A/C on shared features; check that the other pending task is still independently resolvable.

### 17. Make commit commute with a real old update, up to calibrated scale — primitive candidate
**Mechanism.** Select a live relation for which both lawful orders (spend then due step, or due step then spend) realize the same authorized B effect after calibrating actuator gain. Audit both finite paths, not a commutator at initialization.
**Novelty / control.** Equivariance and reversible update composition are standard. The candidate is a pending relation usable under either legal event order with one stored consent, not a Lyapunov predictor of order dependence. Compare exact buffered refits in both orders and a freeze arm.
**Cheapest first test.** One nonlinear old update that alters B gain, then another with the same A improvement that rotates B. Require order tolerance on the first and refusal on the second when transport is not identified.
**Old-task retention.** Measure worst exposed A₁/A₂/C margin across both orders, even if their final A₁ losses coincide.

### 18. Carry signed ratios across a chart seam only with an overlap witness — primitive candidate
**Mechanism.** Use a shared output probe in two piecewise-linear cells to transport the relation through a known chart map. Treat an observed match of one coordinate as insufficient when the map's restriction to the whole direction is ambiguous.
**Novelty / control.** Chart transitions and #265's ReLU-opening handoff already exist. The candidate is preserving *scale freedom* through a verified relation-specific map, not opening a receiver or copying one feasible point. Compare the identical due step with a buffered original-chart fit.
**Cheapest first test.** A two-cell CPU ReLU head with one valid chart rescaling and one chart seam that matches the overlap coordinate but destroys a second joint effect coordinate.
**Old-task retention.** Audit A/C on both sides and at any exposed kink read, with a control matching the A gain but losing pending B orientation.

### 19. Lease a relation without snapshot rollback — primitive candidate
**Mechanism.** Refuse any spend after the expiry clock, then use the next already scheduled lawful update to make the expired weight-carried direction unreadable without undoing intervening old gains. A denied offer before expiry can leave the lease pending.
**Novelty / control.** Deleting a buffered record or restoring a snapshot is known and cheap. The candidate is selective expiration of actionable consent in shared live parameters without erasing ordinary learning; it must beat a byte-matched explicit expiry bit or be treated as inferior.
**Cheapest first test.** Insert useful old work during a two-view delay, then replay the same second offer immediately before and after expiry. Test a separate fresh relation in the same carrier afterward.
**Old-task retention.** Require A₁ parity after expiry and A₂/C preservation; additionally ensure the fresh relation did not resurrect the expired one.

### 20. Place a clean receiver behind a relational interference null — primitive candidate
**Mechanism.** Use the pending relation to identify the subset of receiver motions that keep a measured joint old-task interference read at zero. Accept a legal B spend only in that subset, without modifying the due old batch.
**Novelty / control.** OGD projects out interference, and #265 card 18 closes a nuisance ReLU while opening a receiver. This asks whether the **same** live direction can license a scaled B spend and cancel old interference in finite motion, without requiring either ReLU event. Compare matched post-due nullspace fitting with a buffered ray and ordinary projection.
**Cheapest first test.** Two receiver paths individually contaminate opposite old outputs: one pair cancels for the real B ratio and a same-sign wrong ratio fails. Include a finite-update case where tangent cancellation does not hold.
**Old-task retention.** Audit both old outputs separately and old near-margin items; averaging signed interference would hide damage.

### 21. Learn a relation that predicts withheld scales, not withheld points — primitive candidate
**Mechanism.** Permit the first write only after legal source micro-views identify a direction across multiple independently available amplitudes, then transfer only that direction into the live actuator.
**Novelty / control.** Identifying a low-rank model from multiple observations is standard. The candidate is an evidence-backed live write contract that licenses new scales without a stored target trajectory; compare SVD/normalized-point buffering and SVD used only for offline scoring.
**Cheapest first test.** Train a tiny CPU two-output learner whose source views contain two scales. Test an unseen scale with a new independently valid view, and a mixture with the same first observed point but a different direction at the second.
**Old-task retention.** Charge the repeated source micro-views against the same old schedule and measure A/C after fitting, waiting and spending.

### 22. Refuse an unobservable relation before borrowing capacity — improvement
**Mechanism.** Before writing, bound which distinct admissible rays become indistinguishable under the available quantization, lawful readouts and already scheduled due updates. Refuse a write if its true and junk distinctions lie in that ambiguity set.
**Novelty / control.** Observability and quantization analysis are standard; this is an admission guard, not the ledger's falsified forecast-weighted Gramian chooser. Compare exact rank/ambiguity enumeration and a simple precision floor at identical compute.
**Cheapest first test.** Enumerate quantized states of one two-output head; seed two different rays with identical post-due carrier reads and compare upfront refusal with late false confirms and safe timeouts.
**Old-task retention.** Compare the cumulative A/C service cost of early refusal, harmless late timeout and wrong commit at matched streams.

## Ranked deeper questions

1. **Does a live relation do anything that the best equally small ray buffer plus the same actuator cannot?** Start with cards 01–04 and 21. W13 is the tie sanity check. Use a blind CPU stream with overlapping features, lawfully retired View 1 data and independently varying slopes, scales and old-update histories. Match all costs, then measure useful scale-transferred commits at the same false-confirmation rate and old retention. If the normalized live point or strongest stack ties, keep the negative result and stop treating weight residency as a new primitive on this regime.
2. **When can two views distinguish genuine evidence from a shared-prior fake on the exact same ray?** Test cards 06, 08 and 09 at matched proposals and norms: vary only independent semantic information and include an information-matched impossible case. Separate semantic rejection from geometric rejection. If a lawful independent probe cannot beat matched filler, the deployment regime has no corroboration signal, regardless of carrier precision.
3. **What does mandatory old work preserve: direction, authorized scale interval, or neither?** Factor the ordinary update into gain change, chart transport and true aliasing (cards 02, 05, 10, 17 and 18). Compare paired erasers at equal A gain with the buffered post-due solver. Characterize when a live read recovers permission at the fixed chart versus fabricating permission from a coordinate change. Report pathwise old retention, not just the final read.
4. **Can relation operations compose without new evidence leakage or hidden old-task debt?** Combine narrowing, partial spend and expiry (cards 14–16 and 19) only after the one-write test passes. In a bounded stream, use crossed addresses, replayed confirmations and reused carriers; compare the stack of buffered intersection, spent-ID tracking and expiry at equal memory. A second spend that silently reuses the first view or degrades the first committed task falsifies the composition.

[andmask]: https://arxiv.org/abs/2009.00329
[fromp]: https://arxiv.org/abs/2006.13748
[ogd]: https://arxiv.org/abs/1910.07104
[parks]: https://github.com/manojbajaj95/cl/pull/255
[rkd]: https://arxiv.org/abs/1904.05068
[rome]: https://arxiv.org/abs/2202.05262
[smid]: https://doi.org/10.1016/0005-1098(91)90094-I
