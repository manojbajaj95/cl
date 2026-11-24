# Order relays: pre-paid teaching for blind importers and k-hop handoff chains

**Status:** Ideas only; no experiments, implementation, or GPU work. The two fixtures below are hand-checked rational sanity checks, not evidence.

**Parent:** [Order handoffs](order-handoffs.md) ([PR #205](https://github.com/manojbajaj95/cl/pull/205)).

**Review seeds:** [Flood triage, row 316](https://github.com/manojbajaj95/cl/blob/3986787b67293784f1997eac77d81626452f1a0f/reviews/flood-triage.md#L316) keeps two ideas at score 3: **#205#19**, pre-paid handoff teaching: the exporter places one schedule-preserving truthful example inside its executed prefix before serializing, so `N` blind importers with different arrival queues each keep at least two residual B schedules while paying zero teaching steps (controls: per-importer teaching, #195#19 at the importer, checkpoint plus replay at equal bytes, conformant planning over all importer queues, an importer whose queue no prefix example covers, A/C retention); **#205#04**, a multi-hop relay: chain `k` blind handoffs over nested down-sets with spent budget monotone and a residual width of at least two schedules at every hop, without re-reading earlier learners' states (controls: one-hop #195#07 repeated with full rechecking, Pacti sequential composition, a central scheduler, a hop where over-approximation collapses width to one).

**Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/3986787b67293784f1997eac77d81626452f1a0f/reviews/idea-ledger.md). Bounded-delay scheduling died against gradient accumulation at equal latency; the [replay-deadline null (PR #113)](https://github.com/manojbajaj95/cl/pull/113) demands a smooth no-cliff control; merge and stacked ideas must beat the union of their parts' baselines at equal bytes, checks and compute; ideas whose headline follows from linear algebra are killed, and every first test checks ordinary held-out old-task retention.

## What a relay would buy, and what already exists

The candidate primitive is a **relay invariant**: a constant-size public state `R_j = (I_j, Φ_pub, b_used^{(j)}, c_j, W_j, Π_j)` (down-set executed so far, public check, non-resettable spent budget, certified slot center and width, residual proof) that hop `j+1` can verify and extend from `R_j` alone, so a chain of `k` blind learners keeps `≥ 2` genuinely distinct B schedules open at every hop with per-hop checking cost independent of `j`. Its teaching companion is **pre-paid relay teaching**: one truthful example placed by the exporter before it retires, certified over every importer queue it will serve, so `N` importers pay zero teaching steps.

Prior art is heavy and must be conceded up front:
- **Budget conservation across delegation hops** is solved for agent authorization: [Fault-Tolerant Budget Conservation in Distributed Multi-Agent Delegation (2610.00349)](https://arxiv.org/abs/2610.00349) proves ledger conservation and descendant non-amplification for escrowed budgets moving through a delegation DAG, including timeout-refund double spends; Agent Contracts and Token Budgets (cited there) give parent-child conservation and affine ownership. A non-resetting scalar `b_used` across hops is therefore not new; only a budget tied to **hidden optimizer-slot carry** that the importer cannot observe could be.
- **Relay training** exists as a systems paradigm: [DeRelayL (2605.02935)](https://arxiv.org/abs/2605.02935) passes a model between permissionless trainers with incentives, with no schedule certificates or old-task guarantees. Sequential/split federated learning and verifiable split learning (2511.01356) relay models with integrity, not order freedom.
- **Chained contracts** are Pacti assume-guarantee composition ([2303.17751](https://arxiv.org/abs/2303.17751)), proof-carrying code and proof-carrying messages ([2610.39109](https://arxiv.org/abs/2610.39109)); **one item for many learners** is multi-learner teaching ([2311.10318](https://arxiv.org/abs/2311.10318)) and conformant planning ([1401.3468](https://arxiv.org/abs/1401.3468)); **set-valued state propagation** is interval/zonotope reachability and set-membership estimation.

So the only defensible content is what happens to **hidden optimizer state** under a chain of blind trainers: whether the uncertainty set the relay must carry stays bounded, whether truthful training examples can shrink it, and whether pre-paid teaching beats exporting a few bits of the hidden state.

## Paper fixtures (sanity checks, not evidence)

**Fixture R1: Pre-paid teaching, the Helly cut, and the one-bit export that beats it.** Reuse PR #205 Fixture 2's seam: importers see masked `w = 0` while the exporter's prefix left a hidden slot `h ∈ {1, 3}` (two prefix orders, probe-indistinguishable to importers). The truthful pool gives slot updates `v' = v − g`, `g ∈ {0, 1, 2, 3, 4}`. Each importer `i` has a fixed public pre-`G` B batch from its arrival queue with known drift `d_i`, then picks a residual schedule shifting `v` by `−1` (`σ_1`) or `+1` (`σ_2`) before `G`; the lease requires `|v_G| ≤ r`. Importer `i` keeps both schedules for both hidden histories iff `4 + d_i − r ≤ g ≤ d_i + r`, an interval of length `2r − 4`.
- With `r = 5/2` and importers `d ∈ {−1/2, 0, 1/2}`, the intervals are `[1, 2]`, `[3/2, 5/2]`, `[2, 3]`; the pre-paid item `g = 2` is the unique pool item that keeps two schedules for all three importers and both histories. Per-importer teaching would choose `{1, 2}`, `{2}`, `{2, 3}` respectively, so pre-paying saves `N − 1` teaching steps here.
- Add a fourth importer with `d = 1` (interval `[5/2, 7/2]`, pool item `3`). Its interval is disjoint from `d = −1/2`'s, so no pre-paid blind item exists; because the feasible sets are intervals on a line, Helly's theorem says checking pairs suffices (and in a `p`-dimensional slot with convex cells, checking `(p+1)`-tuples suffices, ignoring pool discreteness).
- **The falsifier:** if the exporter adds one bit to the packet, "my history is `h = 1`" or "`h = 3`", the feasible sets widen to `{1, 2}` (for `h = 1`) or `{3, 4}` (for `h = 3`), and one pre-paid item serves **all four** importers. One exported bit beats blind pre-paid teaching on the instance where blind teaching fails. Pre-paid blind teaching is therefore worth anything only when the exporter cannot export the slot class (privacy, an exporter that does not itself know its prefix order, or a slot class too high-dimensional to name in the byte budget).
- Also at `r = 2`, importer `d = −1/2` has no item even alone (its point interval `{3/2}` misses the integer pool), so "every importer keeps two schedules" can fail from pool discreteness before any relay effect.

**Fixture R2: Relay width is set by optimizer decay, and truthful examples only translate it.** Let each hop `j` execute a down-set extension with two legal prefix orders that leave identical public state but hidden slot increments differing by `δ = 1/2` (as PR #205 Fixture 1's `1/4` vs `1/2` split). The slot evolves `v ← β v + u_j` per hop with optimizer decay `β`. An importer that never reads earlier states must carry the interval width `W_{j+1} = β W_j + δ`, `W_0 = 0`, so `W_k = δ (1 − β^k)/(1 − β)`. With schedule shifts `±1` and safe radius `2`, two schedules stay open iff `W_k ≤ 2` (after centering).
- `β = 1/2`: `W_k → 1`, two schedules at every hop forever.
- `β = 3/4`: `W_k → 2` from below (`W_8 ≈ 1.80`), open forever but with vanishing slack.
- `β = 7/8`: `W_5 ≈ 1.95`, `W_6 ≈ 2.20`: width collapses to one schedule at hop 6.
- `β = 1` (pure accumulation, like an un-decayed carry or a spent-budget counter): `W_k = k/2`, collapse at hop 5.
- Under the additive slot update `v' = v − g` every truthful example moves all hidden states by the same `g`: it re-centers the interval but cannot shrink `W`. Only a non-affine update (gradient clipping, Adam's normalization, a ReLU gate on the slot) can contract the hidden set; for example `v' = clip(v − 2, −1, 1)` maps `{0, 3}` to `{−1, 1}` and `{−1, 0}` to `{−1}`. This is the reviewer's "linear algebra settles it" line: in an affine slot, the relay's fate is `δ/(1 − β)` against the slack, independent of any teaching.

## Idea cards

**P** = candidate primitive, conditional on beating the strongest stacked control; **I** = improvement, audit or falsification control. All first tests are proposed CPU-scale checks on toy hosts (rational fixtures, then a 2-layer ReLU MLP with Adam on a split stream).

### Pre-paid relay teaching (Seed A: #205#19)

#### 01. Pre-paid schedule-preserving example for `N` blind importers (P; restates #205#19)
- **Mechanism:** Before retiring, the exporter applies one truthful example `e` inside its prefix, chosen so that for every importer queue `q` in a declared family `Q` and every hidden history `h ∈ H(z)`, at least two genuinely distinct residual B schedules remain safe; the packet carries `(I ∪ {e}, Φ_pub, b_used, D \ I, Π_I)` and importers pay no teaching step.
- **Novelty vs nearest prior art:** Multi-learner teaching (2311.10318) teaches many learners toward one target; conformant planning finds one action safe across hidden states. The bet is amortizing one training update over importers whose residual *schedules* differ, measured in kept B-order freedom.
- **Cheapest first test:** Fixture R1 at `r = 5/2` with `Q = {−1/2, 0, 1/2}`, then a 2-layer ReLU/Adam host with 8 importers whose queues are sampled from 3 regimes. Compare against per-importer teaching (#195#19 at the importer), conformant planning over `H × Q × S`, checkpoint plus residual replay at equal bytes, and the one-bit export of card 03.
- **Old-task retention check:** Held-out A/C on every importer's chosen residual order and after the common suffix, plus on an importer that only ever runs the default order (pre-payment must not tax it).

#### 02. Helly cut: certify pre-paid feasibility from small importer tuples (P)
- **Mechanism:** When per-importer feasible sets in slot space are convex, a pre-paid item exists for all `N` importers iff every `(p+1)`-tuple of importers (with `p` the certified slot dimension) shares one; the exporter ships the tuple certificate, and a new importer joining later is admitted by checking only its tuples with the existing set instead of re-solving the whole product.
- **Novelty vs nearest prior art:** Helly-type theorems are classical and used in LP-type problems and robust optimization; applying them to make pre-paid teaching *open-world* (importers join after the exporter retires) is the new use.
- **Cheapest first test:** Fixture R1 plus importer `d = 1`: the pair `(−1/2, 1)` is the certificate of infeasibility. Then a 2-D slot (momentum and second moment) toy with 12 importers, measuring check cost for a late importer versus re-solving conformant planning, and the false-admission rate when pool discreteness breaks convexity.
- **Old-task retention check:** The late-admitted importer's A/C slices are evaluated on its residual orders; include a late importer whose clock cell is feasible but whose rare C slice fails, which the tuple check must refuse.

#### 03. One-bit history export versus blind pre-paid teaching (I; mandatory falsifier)
- **Mechanism:** Give the exporter `ℓ` bits to name its hidden history class instead of (or in addition to) teaching blind; sweep `ℓ` and report the number of importers served with two schedules per byte.
- **Novelty vs nearest prior art:** This is quantized state transfer, a plain baseline; its job is to kill blind pre-paid teaching wherever a few bits suffice.
- **Cheapest first test:** Fixture R1 with four importers: blind pre-paid serves 3, one bit serves 4. On the ReLU/Adam host, sweep `ℓ ∈ {0, 1, 2, 4, 8}` bits of quantized optimizer slots against blind pre-paid teaching. Kill blind pre-paid teaching wherever `ℓ ≤ 2` matches it.
- **Old-task retention check:** Matched A/C floors on all arms; check that coarse exported classes never admit an order that breaches a rare A slice inside the class.

#### 04. Prefix-blind exporter: teaching when the exporter does not know its own history (P)
- **Mechanism:** Restrict to exporters whose prefix ran asynchronously (data-parallel workers with nondeterministic reduction order, or a learner that discarded its own order log) so the exporter is as blind as the importers; then pre-paid teaching is the only way to keep schedules open without probes, and card 03's export is unavailable by construction.
- **Novelty vs nearest prior art:** Nondeterministic reduction order in distributed training is known as a reproducibility issue; treating it as a hidden-history class that a single truthful example must cover is new framing that gives Seed A a regime where the one-bit falsifier cannot apply.
- **Cheapest first test:** Simulate a 4-worker asynchronous prefix on the ReLU/Adam host (24 reduction orders), measure the hidden-slot spread, and compare pre-paid teaching against a paid probe that re-measures the slot (PR #179 pricing) and against synchronous reduction at matched wall-clock.
- **Old-task retention check:** A/C over all 24 prefix orders and both kept schedules; include a reduction order that leaves A one step from its floor.

#### 05. Queue-family covering: choose which importers to serve, not one item for all (P)
- **Mechanism:** When no single pre-paid item covers `Q`, the exporter issues the fewest truthful examples, each placed on its own packet fork, so that every importer queue falls into some fork's two-schedule region; this is a covering problem over the interval/convex family of card 02.
- **Novelty vs nearest prior art:** Interval piercing and set cover are classical; the CL content is forking a half-finished training state into a few certified packets instead of teaching each importer.
- **Cheapest first test:** Fixture R1 with `d ∈ {−1/2, 0, 1/2, 1}`: two forks (`g = 2`, `g = 3`) cover all four. On the host, compare fork count and total updates against per-importer teaching and against card 03's one-bit export.
- **Old-task retention check:** Each fork is a distinct training state: check A/C on every fork before and after each importer's suffix.

#### 06. Pre-paid teaching priced against importer-side latency (I)
- **Mechanism:** Charge pre-payment to the exporter's lease (it spends `b_used`) and compare against importer-side seam teaching (card 18 of PR #205), which spends each importer's queue time; report the break-even `N`.
- **Novelty vs nearest prior art:** Amortized issuance versus marginal checking is the economics of proof-carrying code; this card is the audit that says whether training amortizes the same way.
- **Cheapest first test:** Sweep `N ∈ {1, 2, 4, 8, 16}` on the ReLU/Adam host with both placements at equal total updates and B utility.
- **Old-task retention check:** A/C on the exporter's remaining work after it pre-pays (pre-paying spends lease the exporter might have needed).

#### 07. Pre-paid example that also widens the next exporter's window (P)
- **Mechanism:** Choose the pre-paid example so that it keeps two schedules for current importers *and* leaves the slot where the next hop's pre-payment remains feasible, i.e. teach for the relay rather than the single hop; this joins Seed A to Seed B.
- **Novelty vs nearest prior art:** Receding-horizon teaching and lookahead MPC choose actions with future feasibility; the content is a pre-paid training update certified for two hops of blind importers.
- **Cheapest first test:** Two-hop version of Fixture R1 where the greedy hop-1 item makes hop 2 infeasible and a non-greedy item keeps both; compare against greedy per-hop teaching and exact two-hop conformant search.
- **Old-task retention check:** A/C at both seams and after the common suffix for every importer on both hops.

### k-hop relays (Seed B: #205#04)

#### 08. Constant-size relay invariant with decay-bounded width (P; restates #205#04)
- **Mechanism:** Each hop forwards `R_j = (I_j, Φ_pub, b_used^{(j)}, c_j, W_j, Π_j)` and the next hop verifies `W_{j+1} ≤ β W_j + δ_j`, re-centers `c` with one truthful example, and admits residual orders iff the width fits the slack; the check reads only `R_j` and the hop's own updates.
- **Novelty vs nearest prior art:** Pacti chains static contracts and 2610.00349 conserves budgets; neither carries a hidden optimizer-slot uncertainty set whose growth is governed by the optimizer's own decay.
- **Cheapest first test:** Fixture R2 for `β ∈ {1/2, 3/4, 7/8, 1}` (predicted collapse hops: never, never, 6, 5), then a 6-hop relay on an 8-job ReLU/Adam poset where `β` is Adam's `β_1`. Compare against one-hop #195#07 repeated with full rechecking, Pacti sequential composition, a central scheduler that sees every state, and checkpoint relay.
- **Old-task retention check:** A/C at every hop boundary and after the final suffix, with a cumulative rare-C drift invisible at hop 1 that crosses its floor at hop 3 if spent budgets are not summed.

#### 09. Relay horizon law: predict the collapse hop from `(δ, β, slack)` (I)
- **Mechanism:** Predict the first hop where width drops to one schedule as `k* = ⌈log(1 − s(1 − β)/δ)/log β⌉` (slack `s`), and test it on hosts where `δ` and `β` are measured, not planted.
- **Novelty vs nearest prior art:** It is a geometric series; the reviewer would call the toy version linear algebra. The card earns a place only as the falsifier for card 08: if the measured collapse hop on a nonlinear host matches this formula, the relay invariant is bookkeeping, and if it does not, the residual is where card 10 or 11 must live.
- **Cheapest first test:** On the ReLU/Adam host, measure `δ` per hop from prefix-order pairs and compare the predicted `k*` to the observed collapse over 20 seeds, with a variance gate (collapse hop must vary more across `β` than across seeds).
- **Old-task retention check:** A/C at the predicted and observed collapse hops.

#### 10. Contractive teaching: a truthful example that shrinks the hidden set (P)
- **Mechanism:** Fixture R2 shows affine slots can only be translated. Search the truthful pool for examples that hit a non-affine part of the optimizer (clipping threshold, Adam's `√v` normalization, a dead-ReLU gate on a slot-coupled unit) so that the hidden interval contracts at the seam, re-opening schedules after a width collapse without exporting state.
- **Novelty vs nearest prior art:** Synchronizing words (PR #108 lineage) and #203#06 synchronizing batches merge aliased states; here the target is only enough contraction to keep two schedules, with the contraction purchased by a truthful example rather than a reset.
- **Cheapest first test:** Clipped-slot toy where `v' = clip(v − 2, −1, 1)` maps `{0, 3}` to `{−1, 1}`; then on Adam, find pool items whose second-moment effect shrinks the first-moment interval. Compare against an Adam state reset at the seam, card 03's export and #203#06 synchronizing batches.
- **Old-task retention check:** Clipping or saturation can freeze useful updates: check A/C and B utility on the step after contraction and after the suffix.

#### 11. Relay re-anchoring by a public probe every `m` hops (I)
- **Mechanism:** Every `m` hops, spend one paid probe to reset the uncertainty width to the probe's precision (spent budget is never reset); choose `m` from card 09's law.
- **Novelty vs nearest prior art:** Periodic resynchronization in state estimation; the audit question is whether it dominates contractive teaching (card 10) at equal cost.
- **Cheapest first test:** 12-hop relay at `β = 7/8`; sweep `m` and probe precision against card 10 and full rechecking at matched total cost.
- **Old-task retention check:** A/C during the probe step and on the re-opened schedules after it.

#### 12. Hidden-slot budget as a vector ledger across hops (I)
- **Mechanism:** Carry `b_used` as a per-channel occupancy vector (PR #205 #06) and conserve each channel across hops as 2610.00349 conserves escrow, so no hop can launder a half-armed channel by re-anchoring `Φ_pub`.
- **Novelty vs nearest prior art:** Budget conservation through delegation is 2610.00349; the only new piece is that channel occupancy is an inferred hidden-slot bound rather than an issued credit.
- **Cheapest first test:** Two-channel relay where scalar budget stays legal while channel 1 creeps to `5/4` of a `3/2` cliff over three hops; compare scalar, vector and full-state relays on false admissions per byte.
- **Old-task retention check:** Bind rare A to channel 1 and rare C to channel 2; scalar relays must be shown to admit a breach that vector relays block.

#### 13. Order-oblivious relays: hops that hide even which down-set extension they ran (P)
- **Mechanism:** Let hop `j` choose among several down-set extensions of equal public check and publish only their union's certified envelope, so later hops learn neither the extension nor its order; the relay invariant must remain sound over the union.
- **Novelty vs nearest prior art:** Extends PR #205 #02's prefix-oblivious handoff from orders to choices; the privacy angle resembles differential privacy over training order, but the guarantee is schedule safety, not indistinguishability.
- **Cheapest first test:** 4-hop relay where each hop picks one of two extensions; measure width growth versus the order-tagged relay and versus card 03's one-bit tag per hop.
- **Old-task retention check:** A/C over every extension combination (16 paths) at each hop.

#### 14. Branching relays: one packet, two concurrent importer chains, certified rejoin (P)
- **Mechanism:** Split the residual poset into two independent relay chains (PR #205 #05 escrow-split, extended over hops) whose widths grow independently; at rejoin, the combined width is the Minkowski sum of the chains' sets, certified before the common suffix.
- **Novelty vs nearest prior art:** Fork-join budgets are in 2610.00349 (DAG joins aliasing a lineage); here the join adds two hidden-slot uncertainty sets that interact only through shared carriers.
- **Cheapest first test:** Two 3-hop chains on an 8-job poset with one shared carrier; compare certified rejoin against serial relay and full joint recheck at equal bytes.
- **Old-task retention check:** A/C per chain and jointly at rejoin, with a rare C slice sensitive only to simultaneous carry from both chains.

#### 15. Width-maximizing hop order: which learner should go first (I)
- **Mechanism:** Given `k` learners with different `δ_j` (prefix divergence) and the same decay, order the hops so the largest-`δ` learner runs earliest, letting `β^{k−j}` damp it; certify the order rather than the content.
- **Novelty vs nearest prior art:** Exchange-argument scheduling (Smith's rule); kept as an audit because it is cheap and would explain any gain claimed by card 08.
- **Cheapest first test:** 5 learners with `δ ∈ {1/8, 1/4, 1/2, 1, 2}`; compare collapse hop under all 120 orders against the damped-first rule.
- **Old-task retention check:** The order that keeps width longest must not place an A-fragile learner after a large-`δ` one; check A/C under the chosen order.

#### 16. Relays across optimizer changes: hop `j` uses SGD, hop `j+1` uses Adam (P)
- **Mechanism:** When consecutive learners use different optimizers, the relay invariant must translate the uncertainty set through an optimizer-state map (momentum to first moment, no second moment to a fresh one); test whether a certified translation keeps two schedules without exporting slots.
- **Novelty vs nearest prior art:** Optimizer state transfer and resets on switching are engineering practice; certifying the hidden-set image across the switch is the new object, and #178 optimizer-slot splits is the nearest internal prior.
- **Cheapest first test:** 4-hop relay alternating SGD-momentum and Adam on the ReLU host; compare certified translation against an Adam reset at every switch and full checkpoint relay.
- **Old-task retention check:** A/C immediately after each switch, where resets cause the known spike.

### Joint relay × teaching and falsification controls

#### 17. Teach once, relay forever: a pre-paid example whose effect decays slower than width grows (P)
- **Mechanism:** Choose the hop-1 pre-paid example to place the slot center deep inside the safe region along the direction that decays slowest (largest `β` eigenvalue), so later hops need no teaching until width growth eats the margin; certify the no-teaching horizon.
- **Novelty vs nearest prior art:** Combines #205#19 and #205#04 with a decay-spectrum argument; the stacked control is per-hop seam teaching plus card 11 probes.
- **Cheapest first test:** 2-D slot relay with decays `(1/2, 7/8)`; compare the certified no-teaching horizon against per-hop teaching and per-hop probes at equal total updates.
- **Old-task retention check:** A/C at every hop, focusing on the hop where the margin is predicted to run out.

#### 18. Relay with merging importers: two half-finished chains handed to one learner (P)
- **Mechanism:** One importer receives two relay packets for disjoint residual posets and must schedule their union; the certified joint width is the product of the two sets, and pre-paid teaching from either exporter may be wasted or doubled.
- **Novelty vs nearest prior art:** Closest to #193/#204 fold and merge headroom and to OSR6 non-double-booking; the new part is merging two schedule rights rather than two weight branches.
- **Cheapest first test:** Two 2-hop chains merged at hop 3 on the ReLU host; compare against serial import, separate learners, and exact joint search.
- **Old-task retention check:** A/C from both chains' old tasks after the merged suffix.

#### 19. Smooth-world and gradient-accumulation null for relays (I; mandatory)
- **Mechanism:** Replace lease cliffs with smooth margin curves and compare every relay and pre-paid arm against gradient accumulation over each hop's remaining batches at matched latency, which removes order effects to first order.
- **Novelty vs nearest prior art:** The ledger's bounded-delay kill and PR #113's smooth null carried to `k` hops; 2606.29554 (cited in PR #197's node) says fixed-clock optimizer memory makes order effects `O(η)`, so accumulation must also be clock-matched.
- **Cheapest first test:** Run cards 01, 08 and 10 in smooth nonlinear MLP worlds with independent pools, including clock-matched accumulation and a no-relay control at matched B utility. Kill the primitive claim where smooth worlds tie accumulation.
- **Old-task retention check:** Matched pre-relay A/C margins across all arms, with old slices evaluated through every accumulation window.

#### 20. Equal-byte relay audit: invariant versus checkpoint relay plus replay plus cache (I; mandatory)
- **Mechanism:** Measure bytes, per-hop check time, false admissions and surviving schedules for the relay invariant against shipping the full checkpoint (with optimizer state) each hop plus residual replay and a cached checker.
- **Novelty vs nearest prior art:** The economic falsifier; a full checkpoint makes every hidden-state question disappear, so the relay must win on bytes or privacy, not on safety.
- **Cheapest first test:** Sweep `k ∈ {2, 4, 8}` and model size on the ReLU/Adam host; report the byte ratio at which the checkpoint relay overtakes the invariant.
- **Old-task retention check:** A/C on every admitted and refused path; count breaches by cause (budget reset, width under-estimate, unsound proof).

#### 21. Adversarial hop: one dishonest learner in the chain (P)
- **Mechanism:** Assume one hop may misreport `W_j` or skip a decay step; design the invariant so a later honest hop detects the inconsistency from public data alone (a width that is too small for the public update magnitudes) before admitting a residual order.
- **Novelty vs nearest prior art:** Byzantine-robust relays and authenticated chains (2611.30473, PCM 2610.39109) authenticate messages; detecting under-reported *training-state uncertainty* from public updates is the new check.
- **Cheapest first test:** 5-hop relay with one hop that under-reports width by half; measure detection rate and false-alarm rate against trusting every hop and full rechecking.
- **Old-task retention check:** A/C along the path the dishonest hop tried to admit, which must be refused.

#### 22. Relay as continual learning: does the chain keep the first learner's skill? (I; required end-to-end check)
- **Mechanism:** Treat each hop as a new task learner; measure whether the first hop's skill survives `k` hops of blind continuation when the only guarantee carried is the relay invariant, versus sequential fine-tuning with the same data.
- **Novelty vs nearest prior art:** This is ordinary sequential-learning forgetting; the card ties the relay's schedule guarantees back to the retention metric the program cares about.
- **Cheapest first test:** Split-MNIST-style 5-task stream on a small MLP with Adam, one hop per task; compare relay-certified orders, unconstrained orders, replay and EWC at matched compute.
- **Old-task retention check:** Accuracy on task 1 after every hop, plus worst protected slice per task.

## Ranked deeper questions

1. **Does pre-paid blind teaching beat a few exported bits anywhere real?** Cards 01, 03 and 04: Fixture R1 already shows one bit serving four importers where blind teaching serves three. The question is whether prefix-blind exporters (asynchronous reductions) produce hidden-slot classes too large or too private to name, where pre-paid teaching keeps two schedules for `N ≥ 8` importers at lower cost than per-importer teaching, a paid probe, or `ℓ ≤ 2` exported bits.
2. **Is relay collapse fully predicted by `δ/(1 − β)` against slack?** Cards 08 and 09: if the measured collapse hop on a nonlinear Adam host matches the geometric law, the relay invariant is bookkeeping (and the honest result is a short negative). Any systematic residual is where a primitive could live.
3. **Can truthful examples contract hidden optimizer uncertainty, not only translate it?** Card 10: under affine slots they cannot (Fixture R2). Find pool items that use clipping, normalization or gating to shrink the hidden set enough to reopen a collapsed schedule, and beat an optimizer reset, a probe and #203#06 synchronizing batches at matched B utility and A/C retention.
4. **Do relay guarantees survive smooth dynamics and clock-matched gradient accumulation?** Cards 19 and 20: if smooth worlds tie accumulation or a checkpoint relay matches at modest bytes, stop calling the relay a primitive and keep Fixtures R1/R2 as the record.

**Verdict:** Both seeds are conditional. Pre-paid teaching (#205#19) has a crisp structural result, Helly-type tuple checks for open-world importers, but Fixture R1 shows a one-bit export beats it, so it matters only for exporters that cannot name their own history. The k-hop relay (#205#04) carries budget conservation that 2610.00349 already proves; its new content is the hidden-slot width, whose affine fate is set by optimizer decay and cannot be changed by truthful teaching. The joint candidate worth piloting is contractive teaching (card 10) inside a relay, and only against reset, probe, export, checkpoint and accumulation controls with A/C retention checked at every hop.
