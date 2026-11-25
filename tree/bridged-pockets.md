# Bridged pockets

**Status:** Ideas only; no training or GPU work. **Parent:** [Split-pocket park entry](pocket-park-entry.md) ([PR #270][parent]). **Review seeds:** [Flood triage][triage], #270 cards 03 and 16 (both score 3). **Read first:** [Idea ledger][ledger].

## Can due work merge two safe pockets, and can one update play opposite roles in them?

**Verdict: two candidate primitives, not a win.** (1) A B batch that learns a feature an old reader already accepts as a substitute can turn two disconnected safe pockets into one connected park, after which a single public clear is lawful on every history. (2) When the inherited carry lives in raw coordinates and the old readers and B live in lane-relative coordinates, the same B batch spends inward carry in one pocket and is helped by it in the other. Both are exact in the paper fixtures below. Neither beats its strongest control yet: the bridge ties a maintenance write of the substitute unless B was due anyway, and a momentum reset beats the live dual-role schedule on worst-pocket B residual.

**Nearest prior art.** [#270][parent] defines split entry and live braking; [#260][sealed] seals entry through the native optimizer; [#255][relation] has relation parks; [#242][landing] prices inherited velocity; [#234][gates] bounds the coast; [#244][parks] buys order freedom; [#248][complementary] and [#258][handoffs] study batches that only work together. Outside the tree: linear mode connectivity in continual learning ([Mirzadeh et al. 2010.04495][lmc]) finds low-loss paths between solutions but does not create them with a due task; trace partitioning ([Rival & Mauborgne][partition]) and [robust MPC][mpc] reason about disjunctive safe sets and timed modes; sequential funnel composition (Burridge, Rizzi and Koditschek 1999) chains basins with controller switches. On the optimizer side, [2610.03940][answermass] shows momentum carrying old gradients that remove answer mass, [2609.36738][outmom] relocates momentum from parameter to task coordinates, and [2608.24593][transport] measures delayed optimizer-state transport. None makes a due task's update merge safe components or relies on a raw-versus-task frame mismatch to give one update two roles.

## Contract and deciding controls

- Inherit the #270 contract: freeze the public observation, the lawful histories, the truthful C pool, the permitted B batches and windows, native optimizer semantics, the due readers, the B milestones and the final witness. One public action sequence for every history; branches exist only in the proof. No hidden tags, slot writes, maintenance batches or menu changes after commitment.
- **Bridge claims.** The old reader must already accept the substitute before B arrives (the relation is frozen, not edited). B must improve its own held-out witness, and the bridge must be opened by that same update, not by an auxiliary label chosen for steering. Report what the merge buys in reclaimed capacity (a lane freed for new work, a clear made lawful) and price it against (a) a maintenance batch that writes the substitute at equal cost, (b) a B batch with the same witness gain that leaves the substitute unusable (private head), (c) permanent separation, (d) an oracle merge that writes the substitute directly. If B is the precondition of the clear, call it forced precedence, not order freedom. Certify how long the bridge holds under later updates and live carry.
- **Dual-role claims.** Both pockets must have a genuinely needed effect: a threatened old read in the braked pocket, and progress or a deadline in the carried pocket that the carry actually helps. Mirror-symmetric pairs (the same effect in a relabelled frame) do not count. Controls: idle ticks, a raw-frame B batch that brakes both pockets, separate per-pocket batches at equal compute, #260/#270 single-branch braking, #242 landing, and a momentum reset at the same clock. A reset is a slot write and is not lawful, but the live schedule must beat it on worst-pocket service or on a second coordinate whose carry is needed.
- **Joint claims.** Cross bridge/no-bridge with dual-role/single-role at identical budgets, give the strongest lawful stack exact disjunctions and timed reachability, and require a coupled witness where removing either ingredient loses a different lawful trace. A factorized fixture (like both below) shows feasibility only.

## Exact paper checks

Heavy-ball updates `m′=m/2+g, w′=w−m′`, unit step, coordinatewise, no decay, atomic reads. Each named loss is a sum of half-squares on its named coordinates only. Lawful histories differ only in lane sign `s=±1`; the public observation is `x²=1` with equal clocks. Every number below was checked with exact fractions.

### F1. A due B batch opens the bridge (seed #270#03)

State `(x, z)`: lane `x=s` with zero slot, substitute `z=0` with zero slot. Old A reads `x²+z≥3/4`: at `z=0` the safe set is two pockets `|x|≥√3/2` separated at `x=0`; at `z≥3/4` it is connected. B is independently useful and targets `z=1`. New task D wants the lane back and targets `x=0` (the common clear). Installed C reads `z≤2`.

| Arm (identical on both lanes) | after first event `(x, z)`, A | after D `(x, z)`, A | three idle ticks |
| --- | --- | --- | --- |
| D alone | — | `(0, 0)`, **fails** | `x²` back above 3/4 only at tick 3 |
| B then D | `(s, 1)`, pass | `(0, 3/2)`, pass | `x: −s/2, −3s/4, −7s/8`; `z: 7/4, 15/8, 31/16`; all pass |
| B and D in one batch | — | `(0, 1)`, pass | `z: 3/2, 7/4, 15/8`; all pass |
| Private-head B (same witness gain, `z` untouched) then D | `(s, 0)`, pass | `(0, 0)`, **fails** | fails until tick 3 |
| D then B | — | `(0, 0)`, **fails** | — |

After B, one public D is lawful on both lanes and the lane's carry even crosses the former separator (`x` ends near `−s`) without a read failing, because the park is now connected. Without the bridge no lawful clear exists: D's target is the separator itself. Two caveats. D is admitted only after B, so this is forced precedence. And with no later B piece the carry pushes `z` past B's own target (`|z−1|` grows to `15/16`), so the bridge's B work needs its own brake; installed C holds only because the coast limit is exactly 2.

### F2. One B piece brakes one pocket and carries the other (seed #270#16)

State: fixed lane `x=s` and a raw coordinate `q=0` whose slot both histories inherit from the same public entry word, `m_q=+1/2` (`q` moving down). Readers and B are lane-relative in `q̃=s·q`: old A reads `q̃≥−1/4`, installed C reads `q̃≤1`, and B targets `q=s/2` (`q̃=1/2`), with witness `|q̃−1/2|` starting at `1/2` and a milestone `≤1/4` at tick 1. In lane coordinates the shared carry is `+1/2` toward A's floor in pocket `+` and `−1/2` away from it in pocket `−`.

| Schedule (ticks 1–4) | pocket `+` q̃ | pocket `−` q̃ | B residual at tick 2 (`+`, `−`) |
| --- | --- | --- | --- |
| idle, idle, idle, idle | `−1/4`, **`−3/8`** (A fails), … | `1/4`, `3/8`, `7/16`, `15/32` | `7/8`, `1/8` |
| B, idle, idle, idle | `1/4`, `3/8`, `7/16`, `15/32` | `3/4`, **`9/8`** (C fails), `21/16`, `45/32` | `1/8`, `5/8` |
| B, B, idle, idle | `1/4`, `5/8`, `13/16`, `29/32` | `3/4`, `7/8`, `15/16`, `31/32` | `1/8`, `3/8` |
| raw-frame B (targets `q=1/2`), idle, … | `1/4`, `3/8`, `7/16`, `15/32` | `−1/4`, **`−3/8`** (A fails), … | `1/8`, `7/8` |
| slot reset, then B, B, idle, idle | `1/2`, `3/4`, `7/8`, `15/16` | same | `1/4`, `1/4` |

The first B piece does what seed #16 asks: in pocket `+` its gradient reverses the inward carry (lane momentum `+1/2 → −1/4`) and saves A; in pocket `−` the carry adds to it (lane momentum `−1/2 → −3/4`) and both pockets meet the tick-1 milestone. The raw-frame batch that brakes both pockets breaks A in pocket `−`, so the frame mismatch is doing real work. But a single piece over-carries pocket `−` into installed C at tick 2; the second B piece brakes pocket `−` and carries pocket `+`, so the roles swap at piece 2. The live schedule passes every read, yet the reset matches its mean residual (`1/4`) and beats its worst pocket (`1/4` vs `3/8`). The fixture shows a dual-role update and a negative control that bites, **not** an advantage over reset: that needs a second coordinate whose carry an old reader needs in both pockets.

## Idea cards

### A. Bridges bought by due work

### 01. Merge two safe pockets only when a due B batch opens the bridge — primitive candidate
**Mechanism.** An old reader accepts either the lane feature or a substitute; a useful B batch learns the substitute, the safe set becomes connected, and one public clear discharges the two-pocket obligation. **Novelty vs nearest prior art.** This is the #270#03 seed made exact (F1); mode connectivity ([2010.04495][lmc]) finds existing low-loss paths, while here a due task's update creates the connection that a later clear needs. **Cheapest first test.** F1 on a two-feature MLP: an old classifier that can use feature x or substitute z, B a task whose labels require z; compare B-then-clear, private-head B, a maintenance write of z and permanent separation. **Old-task retention check.** Read old examples that rely only on x, only on z, and both, before and after the clear.

### 02. Price the bridge as the maintenance it avoided — primitive candidate
**Mechanism.** Count a bridge as a primitive only when the substitute would otherwise need a dedicated maintenance batch; the saving is that batch's compute, exposure and C budget. **Novelty vs nearest prior art.** [#255][relation] and [#260][sealed] treat safety as paid by entry words; this makes due B work the payer and asks for the exchange rate. **Cheapest first test.** On F1 and one nonlinear host, sweep B's usefulness (held-out witness gain) against bridge strength and report the cheapest lawful clear with and without B in the menu at equal total updates. **Old-task retention check.** Hold A and installed-C floors fixed across arms; count a refused clear as lost capacity, not retained accuracy.

### 03. Lease the bridge rather than own it — primitive candidate
**Mechanism.** A bridge holds only while the substitute stays above the threshold; publish a lease (latest tick before which the lane must be back inside a pocket or the clear finished) and certify every lawful later task against it. **Novelty vs nearest prior art.** [#234][gates] bound coasts of fixed gates; here the gate itself can close when later training reuses the substitute. **Cheapest first test.** Extend F1 with a later task E targeting `z=0`; enumerate E arrivals and find the earliest one that strands the lane at the separator. **Old-task retention check.** Fire A at every tick between D and E's arrival and after E, on lanes that coasted across the old separator.

### 04. Turn the merge into reclaimed capacity — primitive candidate
**Mechanism.** The payoff of merging is a lane freed for new work: after the bridge, a new task can write over the old lane coordinate on all histories with one action. **Novelty vs nearest prior art.** Recyclable units ([2609.38356][recycle]) and capacity reuse free units by gating; here freeing is earned by a substitute that due work installed, with no gate. **Cheapest first test.** Two-feature MLP, three tasks: measure new-task loss after D with and without a bridging B at equal parameters and updates. **Old-task retention check.** Old A accuracy on substitute-only inputs and on held-out mixtures after D trains the freed lane.

### 05. Let the carry cross the old separator only while bridged — primitive candidate
**Mechanism.** After a merge, inherited momentum may move the lane across the former separator (F1); certify such crossings as lawful only inside the lease and require the carry to stop before the lease ends. **Novelty vs nearest prior art.** [#242][landing] prices carry inside one region; this prices carry across a region that is safe only temporarily. **Cheapest first test.** F1 with a lease at tick 2 or 3; compare the live trajectory, a reset at D and a braking B piece. **Old-task retention check.** Read A exactly at the lease boundary and one tick after on every coast.

### 06. Narrow the separator instead of removing it — primitive candidate
**Mechanism.** A weak B batch raises the substitute below threshold, shrinking the unsafe band; a cheaper partial clear or a shorter entry word becomes lawful. **Novelty vs nearest prior art.** #270 treats pockets as connected or not; this grades the merge and asks whether partial bridges compose. **Cheapest first test.** F1 with B targets `z ∈ {1/4, 1/2, 3/4}`; tabulate the band `x² < 3/4 − z` and the cheapest lawful partial clear. **Old-task retention check.** Read A on lanes stopped inside the narrowed band and at both band edges.

### 07. Open a bridge that needs two due batches — primitive candidate
**Mechanism.** The substitute crosses threshold only with two B pieces whose contributions add, and neither alone opens the bridge; certify both orders and the gap between them. **Novelty vs nearest prior art.** [#248][complementary] and [#258][handoffs] find batches that only work together on slot gaps; here their joint product is connectivity. **Cheapest first test.** F1 with `z` needing `z₁+z₂≥3/4` from two B tasks; compare both orders, one piece, and a single strong maintenance batch. **Old-task retention check.** Read A between the two pieces, where the bridge is half-built.

### 08. Certify the bridge from public reads only — primitive candidate
**Mechanism.** The runtime must know the bridge is open without a private tag; admit the clear only when a public read of the substitute certifies the merge on every history. **Novelty vs nearest prior art.** #270 forbids hidden dispatch; this asks whether the merge signal is itself public, so admission stays history-free. **Cheapest first test.** F1 with noisy or partially observed z; compare public-read admission against an oracle that knows z exactly. **Old-task retention check.** Count false admissions (clear lands at the separator with bridge closed) as A failures.

### B. One update, two roles

### 09. Brake one pocket and carry the other with one B piece — primitive candidate
**Mechanism.** Same B batch, opposite needed effects: it reverses inward carry in one pocket and adds to useful carry in the other (F2, piece 1). **Novelty vs nearest prior art.** This is the #270#16 seed made exact; [#260][sealed] has a single-branch brake and [2610.03940][answermass] shows harmful carried momentum, not a carry that is harmful in one state and useful in another. **Cheapest first test.** F2 on a two-layer net where lane sign is a hidden-unit sign flip; compare idle, raw-frame B, per-pocket batches and reset. **Old-task retention check.** Worst pocket-by-tick A and installed-C margins after piece 1 and piece 2.

### 10. Use the raw-versus-lane frame mismatch as the resource — primitive candidate
**Mechanism.** Entry carry is written in raw parameter coordinates while readers and B are lane-relative, so a shared carry points inward in one pocket and outward in the other. **Novelty vs nearest prior art.** [2609.36738][outmom] moves momentum into task coordinates to remove frame effects; this exploits the mismatch instead. **Cheapest first test.** F2 against a frame-aligned null where the entry carry is lane-relative (mirror symmetry: both pockets get the same role, so no dual role exists). **Old-task retention check.** In both frames, read A at the first idle tick, where a mis-signed carry fails first.

### 11. Schedule role alternation across B pieces — primitive candidate
**Mechanism.** In F2 piece 1 brakes `+` and carries `−`, piece 2 the reverse; certify a B schedule where alternating roles land both pockets inside their windows without a maintenance step. **Novelty vs nearest prior art.** [#270 card 17][parent] swaps the threatened pocket by planning; here the swap arises from the native dynamics and must be predicted, not designed per pocket. **Cheapest first test.** Enumerate B/idle words of length 4 on F2 and on a variant with unequal pocket carry. **Old-task retention check.** Read the tight reader just before each role swap.

### 12. Reserve an over-carry allowance in the carried pocket — primitive candidate
**Mechanism.** The carried pocket can overshoot into installed C (F2, single piece); reserve a ceiling allowance at entry and certify that the next due B piece arrives before it is spent. **Novelty vs nearest prior art.** [#242][landing] budgets one excursion; this budgets the excursion that the dual-role update itself causes in the pocket it helps. **Cheapest first test.** F2 with the C ceiling swept in `[7/8, 3/2]` and the second B piece's window swept; map the lawful region. **Old-task retention check.** Installed-C read at each tick of the over-carry and at the coast limit.

### 13. Split the roles between Adam's numerator and denominator — primitive candidate
**Mechanism.** Under Adam, the same B gradient may brake one pocket through its first moment and slow the other through a shared second moment; certify both roles with one bias-corrected step. **Novelty vs nearest prior art.** [#270 card 09][parent] spends carry in the denominator for one pocket; here the two moments play different roles in different pockets. **Cheapest first test.** Exact-interval Adam on F2's two histories with two `v` levels; compare m-only and v-only offline ablations. **Old-task retention check.** Read A and C at the next tick, where bias correction changes most.

### 14. Serve both roles from an equal public observation — primitive candidate
**Mechanism.** The pockets share the observation and differ only in hidden lane sign; certify that the runtime's single public B schedule serves both without learning which pocket it is in. **Novelty vs nearest prior art.** [#270][parent] requires this for entry; here it must hold for every later B piece, including role swaps. **Cheapest first test.** F2 with a third history (smaller lane magnitude) that shares the observation; check that the same schedule still serves all three. **Old-task retention check.** Worst A and C reads over all three histories.

### 15. Beat the reset on a coordinate whose carry is needed — primitive candidate
**Mechanism.** Add a second coordinate whose inherited carry an old reader needs in both pockets; a reset zeros it and loses, while the live dual-role schedule keeps it. **Novelty vs nearest prior art.** Every #260/#270 fixture so far ties or loses to reset on its own coordinate; this is the deciding control. **Cheapest first test.** F2 plus `r` with `m_r` needed to reach an installed-C floor by tick 2; compare live B,B against reset+B,B. **Old-task retention check.** The `r` reader at its deadline and the `q̃` readers at every tick.

### C. Bridges and dual roles together

### 16. Let the bridge replace the brake — primitive candidate
**Mechanism.** The B piece that opens a bridge removes the separator that the carry threatened, so the braking obligation vanishes in the pocket that would have needed it. **Novelty vs nearest prior art.** #270 treats merging and braking as separate tools; this couples them in one update. **Cheapest first test.** Combine F1 and F2: carry pushes the lane toward the separator in one pocket, and B both learns the substitute and acts on the lane; compare to bridge-only, brake-only and the jointly tuned stack. **Old-task retention check.** A at the tick the lane crosses where the separator used to be.

### 17. Win the race between carry and bridge — primitive candidate
**Mechanism.** The bridge must open before inward carry reaches the separator; certify the latest lawful B arrival as a function of carry and bridge strength. **Novelty vs nearest prior art.** [#260 card 07][sealed] times braking; here the deadline is set by a topological change instead of a floor. **Cheapest first test.** F1 with initial lane carry toward 0; sweep B's arrival tick and z target. **Old-task retention check.** A at the tick before the bridge opens on the latest lawful trace.

### 18. Keep merged carry from stranding the lane when the bridge closes — primitive candidate
**Mechanism.** After merge, carry may leave the lane in the wrong pocket or at the separator when the bridge closes; certify that every history ends inside some pocket before the lease expires. **Novelty vs nearest prior art.** Combines 03 and 05 into the joint obligation; [robust MPC][mpc] has mode deadlines but no closing safe-set connection. **Cheapest first test.** F1 plus E (z back to 0) at ticks 2–5; record which arrivals strand which lane. **Old-task retention check.** A on every history right after E.

### 19. Hand a merged park to a successor learner — moonshot, primitive candidate
**Mechanism.** Export one connected obligation plus a lease instead of a pocket set; a successor can consume it without the prefix or pocket labels. **Novelty vs nearest prior art.** [#270 card 18][parent] composes pocket sets across builds; merging first may shrink the exported contract. **Cheapest first test.** Tabulate exported obligations with and without a bridge on two short grammars; pursue only if the merged summary stays sound and smaller on held-out compositions. **Old-task retention check.** A reader spanning the handoff, at the receiver's earliest and latest arrivals.

### D. Audits

### 20. Separate earned bridges from steering labels — improvement
**Mechanism.** Require the bridging B to improve a held-out B witness and compare with an equal-gain B that leaves the substitute unusable. **Novelty vs nearest prior art.** Independent utility is in [#260][sealed]; this audit targets labels chosen because they open a bridge. **Cheapest first test.** F1's private-head arm plus a B whose held-out witness fails but whose z moves. **Old-task retention check.** A and C on both arms; passing them does not count if B fails.

### 21. Check whether bridge and dual role factorize — improvement
**Mechanism.** Both fixtures factorize (separate coordinates); demand a coupled host where removing either ingredient loses a different lawful trace. **Novelty vs nearest prior art.** The ledger's merge rule requires stacked controls; this applies it to the two #270 seeds. **Cheapest first test.** Add a coupling term between `z` and `q` and exhaust B/idle words with and without it. **Old-task retention check.** Same worst A/installed-C floors across coupled and factorized arms.

### 22. Name the first obstruction: no bridge, late bridge, or over-carry — improvement
**Mechanism.** Enumerate short schedules to attribute a refusal to missing connectivity, a lost race, or over-carry in the helped pocket. **Novelty vs nearest prior art.** [#270 card 19][parent] diagnoses topology versus timing; this adds over-carry from a dual-role update. **Cheapest first test.** Plant each failure in F1/F2 variants and recover a witness trace or a bounded exhaustive obstruction. **Old-task retention check.** Name the first failing A/C read and report missed B milestones separately.

## Ranked deeper questions

1. **Does a due B batch buy reclaimed capacity by bridging, beyond a maintenance write at equal cost?** Start with 01, 02, 04 and 20. Require B's held-out witness gain, a lawful clear that is refused without the bridge, and new-task gain on the freed lane at matched A/C floors. If a maintenance write of the substitute ties at equal compute, the bridge is bookkeeping.
2. **Can dual-role updates beat a momentum reset?** Run 09, 10 and 15. F2 loses to reset on worst-pocket residual; the claim survives only if a coordinate whose carry is needed in both pockets makes reset lose, with the frame-aligned null showing no dual role.
3. **Do bridge and brake interact, or only stack?** Run 16, 17 and 21 on a coupled host. Retire the joint claim if the jointly tuned lawful stack with exact disjunctions and timed reachability ties.
4. **How long does an earned bridge hold under later training and live carry?** Run 03, 05 and 18. If leases are so short that every useful clear must finish before the next task, price that against permanent separation.

[parent]: https://github.com/manojbajaj95/cl/pull/270
[sealed]: https://github.com/manojbajaj95/cl/pull/260
[triage]: https://github.com/manojbajaj95/cl/blob/106d39d945a291827513b938711138c0535a4259/reviews/flood-triage.md#L387
[ledger]: https://github.com/manojbajaj95/cl/blob/106d39d945a291827513b938711138c0535a4259/reviews/idea-ledger.md
[relation]: https://github.com/manojbajaj95/cl/pull/255
[parks]: https://github.com/manojbajaj95/cl/pull/244
[landing]: https://github.com/manojbajaj95/cl/pull/242
[gates]: https://github.com/manojbajaj95/cl/pull/234
[complementary]: https://github.com/manojbajaj95/cl/pull/248
[handoffs]: https://github.com/manojbajaj95/cl/pull/258
[lmc]: https://arxiv.org/abs/2010.04495
[answermass]: https://arxiv.org/abs/2610.03940
[outmom]: https://arxiv.org/abs/2609.36738
[transport]: https://arxiv.org/abs/2608.24593
[recycle]: https://arxiv.org/abs/2609.38356
[partition]: https://doi.org/10.1007/978-3-540-31987-0_2
[mpc]: https://doi.org/10.1016/j.automatica.2004.08.019
