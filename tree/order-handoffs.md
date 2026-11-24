# Order handoffs: transferring partial execution and multi-schedule teaching

**Status:** Ideas only; no experiments, implementation, or GPU work.

**Parent:** [Safe order families](safe-order-families.md) ([PR #195](https://github.com/manojbajaj95/cl/pull/195)).

**Review seeds:** [Flood triage, row 302](https://github.com/manojbajaj95/cl/blob/1c3db4db61fb5088def38b8efcff34e9b8262a7f/reviews/flood-triage.md#L302) keeps two ideas at score 3: **#195#07**, hand off a partially executed update order by serializing the executed down-set, a public state check, the budget already spent and a conditional proof for every remaining extension so a blind importer picks any residual order without source activations or a lease reset; **#195#19**, pick one truthful example verified jointly over the full history-by-order product so the blind importer keeps at least two genuinely different B schedules open.

**Read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/1c3db4db61fb5088def38b8efcff34e9b8262a7f/reviews/idea-ledger.md). Bounded-delay scheduling died against gradient accumulation at equal latency; the [replay-deadline null (PR #113)](https://github.com/manojbajaj95/cl/pull/113) requires a smooth no-cliff control; every candidate primitive must beat the best baselines stacked at equal bytes, checks and compute, and every first test must check ordinary held-out old-task retention.

## What the handoff object would buy

The candidate primitive is a **resumable, budget-honest schedule right**: an exporter executes a prefix of a certified partial order, retires without sharing source activations or private trajectories, and hands off a bounded packet `(I, Φ_pub, b_used, D \ I, Π_I)` that lets a blind importer choose any remaining legal order of `D \ I` without reopening the prefix proof or resetting the lease. Its teaching companion is a **schedule-preserving universal update**: one independently truthful example verified across the full `H(z) × LinExt(D \ I)` product so that at least two genuinely distinct B schedules remain open after the update, without decoding or coalescing hidden optimizer histories. Typestate and session types, assume-guarantee contracts ([Pacti](https://arxiv.org/abs/2303.17751), [GR(1) contracts](https://arxiv.org/abs/2610.37534)), proof-carrying code, order-ideal verification, [conformant planning](https://arxiv.org/abs/1401.3468) and [multi-environment machine teaching](https://arxiv.org/abs/2607.08647) are established prior art. If a checkpoint plus residual replay and a cached contract checker match the coverage and cost, this is an improvement at best.

- **Half-finished handoff:** Fix the frozen bridge, suffix proof, named batch instances, optimizer law, certified start envelope and allowed continuations from PR #195. After executing down-set `I ⊆ D`, serialize: (i) `I`, (ii) a public state check `Φ_pub` evaluable without private slots or source activations, (iii) non-resettable spent budget `b_used` (tracking armed hidden-to-visible carry channels, not only a scalar), and (iv) a conditional residual proof `Π_I` covering every linear extension of `D \ I` from every hidden state consistent with `(I, Φ_pub, b_used)`. Because two distinct linearizations of `I` can pass the same `Φ_pub` while diverging in private slots, `Π_I` must either quantify over all legal prefix orders of `I` or carry a public prefix-equivalence tag.
- **Schedule-preserving universal teaching:** For a fixed public transcript `z` (at start or at a handoff seam), let `H(z)` contain all legal hidden optimizer histories consistent with `z` (or a sound overapproximation), and let `S ⊆ LinExt(D \ I)` contain at least two schedules that genuinely differ in B update order (not commuting no-ops). Choose one independently truthful example `e` from the frozen pool, applied under the ordinary optimizer, certifying `∃ e ∀ h ∈ H(z) ∀ σ ∈ S ∀ legal continuations: safe(e, h, σ, continuation)`. No hidden-state labels, per-history execution branches, or uncharged slot probes. Successor slots across `H(z)` need not coalesce.
- **Equal-resource accounting:** Fix the truthful pool, B utility bands (loss and accuracy), old-task floors, external arrival constraints and read precision. Report useful safe imports, false admissions, missed safe imports, surviving distinct B schedules, transfer bytes, issuance and importer-side checking work, updates and queue delay. Evaluate ordinary held-out A/C performance plus worst protected slices before handoff, across every residual prefix, through bridge execution and after the common suffix (and on refusal fallbacks); held-out tests never enter selection or proofs.

**Nearest controls:** Full recheck from scratch; transferring a full checkpoint plus residual replay and a semantic proof cache at equal transfer bytes; [Pacti](https://arxiv.org/abs/2303.17751) residual contracts; [certificate entry ports (PR #171)](https://github.com/manojbajaj95/cl/pull/171) and [leakage leases (PR #176)](https://github.com/manojbajaj95/cl/pull/176); [CABA](https://arxiv.org/abs/2610.40740), [Certified CL](https://arxiv.org/abs/2407.06697) and [sample-compression self-certification](https://arxiv.org/abs/2503.10503). For teaching, compare against an item safe across `H(z)` for only one order, an item safe across ≥2 orders on a point-estimate history, conformant planning over `H(z) × S` ([0706.2619](https://arxiv.org/abs/0706.2619), [1401.3468](https://arxiv.org/abs/1401.3468)), [single-swap unlocking (PR #187 #11)](https://github.com/manojbajaj95/cl/pull/187), same-pool [MTT](https://arxiv.org/abs/2203.11932), [multi-learner teaching](https://arxiv.org/abs/2311.10318), and a paid slot probe plus specialist teaching ([PR #179](https://github.com/manojbajaj95/cl/pull/179)). The hardest deployable control stacks residual replay, cached Pacti/entry-port checks and cached belief-level teaching at equal bytes and compute.

## Paper fixtures (sanity checks, not evidence)

**Fixture 1: Half-finished handoff with prefix divergence and a spent-budget near miss.** Take PR #195's six jobs `E, T, G, M, X, Y` with masked weight `w = 0` on the public transcript and initial private slot `v_0 = 2`. `E` sets the bridge reservation to `1` and adds carry drift `v → v + 1/2`. `T` applies one truthful unit-rate step with `g = 1` under `v' = v/2 − g`, leaving `w` masked. `G` is the frozen launch test (requires reservation `1`, unrevoked `G ≺ M`, and lease condition `|v| < 3/2` at `G`, with at least one update after `G`); `M` revokes new launches and sets a rare C output to `1 − w_X` (floor `1/2`, requiring `M ≺ X`). `X, Y` update independent B heads, and `Y` adds `3/4` to `v` if executed before `G`. Learner 1 executes down-set `I = {E, T}` and retires. The two legal prefix orders leave identical public state (`w = 0`, reservation `1`) yet different hidden slots: `E, T` gives `v = (2 + 1/2)/2 − 1 = 1/4`, while `T, E` gives `v = (2/2 − 1) + 1/2 = 1/2`. The residual poset `D \ I = {G, M, X, Y}` with edges `G ≺ M ≺ X` has `4!/6 = 4` linear extensions (`G,M,X,Y`, `G,M,Y,X`, `G,Y,M,X`, `Y,G,M,X`), preserving both B-head orders (`X ≺ Y` and `Y ≺ X`). Even when `Y` runs before `G`, `v` reaches `1` (from `E,T`) or `5/4` (from `T,E`), both `< 3/2`. Now test a careless importer that resets `b_used ← 0` (treating `v` as `0`) and inserts a benign-looking pre-`G` update `Z` adding `+1` to `v`: from `0` it predicts `1 < 3/2`, from `E,T` it lands at `5/4 < 3/2`, but from `T,E` it hits `3/2`, silently breaking the lease. Carrying `b_used` bounded over all prefix orders of `I` blocks the near miss without exporting Learner 1's private order or activations.

**Fixture 2: The 2×2 history-by-order diagonal trap (positive and non-factorable negative).** At a handoff seam, the public transcript shows masked `w = 0` while two probe-indistinguishable hidden histories hold `h_1: v = 1` and `h_2: v = 3`. Two genuinely distinct remaining B schedules differ in which B head runs before `G`: `σ_1` (`X` before `G`, then `M, Y`) shifts `v → v − 1` before `G`, while `σ_2` (`Y` before `G`, then `M, X`) shifts `v → v + 1` before `G`. Lease safety at `G` requires `|v_G| ≤ 2`. The model predicts `w x_1` against teacher `y = x_2` under half-squared error, giving gradient `g = −x_1 x_2` at `w = 0` and slot update `v' = v − g` (leaving `w` masked). Freeze the truthful pool to `(x_1, x_2) ∈ {(0,0), (1,−1), (1,−2), (1,−3), (1,−4)}` (`g ∈ {0, 1, 2, 3, 4}`). Then:
- `g = 1` (`e_point`) passes both orders on `h_1` (`−1, 1`) and `(h_2, σ_1)` (`1`), but fails `(h_2, σ_2)` (`3 > 2`) → false admission if chosen from a point estimate.
- `g = 3` (`e_singleton`) passes both histories on `σ_2` (`−1, 1`), but fails `(h_1, σ_1)` (`−3 < −2`) → collapses the importer to a single schedule.
- `g = 2` (`e_joint`) passes all four cells `{h_1, h_2} × {σ_1, σ_2}` with `v_G ∈ {−2, 0, 0, 2}` while keeping successor slots distinct (`−1` vs `1`).

Now widen the hidden class to `h_1: v = 0`, `h_2: v = 4` (same `σ_1, σ_2`, same `|v_G| ≤ 2`). Every row and every column still has a truthful solution: `g = 1` makes `σ_1` universal (`−2, 2`), `g = 3` makes `σ_2` universal (`−2, 2`), `g = 0` opens both schedules for `h_1` (`−1, 1`), and `g = 4` opens both for `h_2` (`−1, 1`). Yet no `g ∈ ℝ` covers all four cells because `(4 + 1) − (0 − 1) = 6 > 4`. Single-axis checks cannot certify the product.

## Idea cards

**P** = candidate primitive, conditional on beating the strongest stacked control; **I** = improvement or falsification control. All first tests are proposed CPU-scale checks.

### Half-finished order handoffs (Seed A: #195#07)

#### 01. Export the residual poset with spent-budget continuity (P; inherits #195#07)
- **Mechanism:** Serialize `(I, Φ_pub, b_used, D \ I, Π_I)` after executing down-set `I`, binding every remaining linear extension of `D \ I` to the non-resettable spent lease and public state check so a blind importer picks any residual order without source activations.
- **Novelty vs nearest prior art:** Pacti contracts and PR #171 entry ports verify static interfaces; the bet is transferring live mid-order scheduling freedom with monotonic budget continuity across a blind handoff.
- **Cheapest first test:** Run Fixture 1 with two blind importers preferring opposite B-head orders (`X ≺ Y` vs `Y ≺ X`) plus the planted reset-budget near miss `Z`. Compare against full recheck, full checkpoint transfer, and residual replay plus cache at equal transfer bytes.
- **Old-task retention check:** Evaluate held-out A/C before handoff, at every residual prefix, and after the common suffix, including the rare C slice `1 − w_X` that fails if `b_used` is reset or `M ≺ X` is dropped.

#### 02. Prefix-oblivious handoff over all legal linearizations of `I` (P)
- **Mechanism:** Quantify `Π_I` over the union of hidden states reachable by *all* legal prefix orders of down-set `I` matching `Φ_pub`, allowing the exporter to keep its execution order of `I` private while remaining sound for every residual extension.
- **Novelty vs nearest prior art:** Order-ideal abstract interpretation computes reachable sets over down-sets; the candidate is a privacy-preserving handoff contract that separates down-set completion from prefix-order disclosure.
- **Cheapest first test:** In Fixture 1, hide whether Learner 1 ran `E, T` or `T, E` (same `I`, same `Φ_pub`, different `v ∈ {1/4, 1/2}`) and inject `Z`. Compare prefix-oblivious `Π_I` against order-tagged handoff, full recheck and a checkpoint at equal bytes.
- **Old-task retention check:** Plant a rare A slice vulnerable only from `T, E` after `G`; verify prefix-oblivious `Π_I` blocks unsafe residual orders without hurting safe `Y ≺ X` coverage.

#### 03. Mid-crossing bridge handoff after launch latches (P)
- **Mechanism:** Hand off *after* `G` has latched the bridge reservation but before the crossing finishes: `M` can no longer revoke launch, while the importer inherits an active, non-pausable lease countdown and chooses among remaining post-launch orders.
- **Novelty vs nearest prior art:** Entry ports (PR #171) target pre-entry arrival; transferring an already-latched crossing tests whether post-launch ordering freedom is safely portable without pausing or rolling back the bridge.
- **Cheapest first test:** Split a 7-job bridge right after `G` with two post-launch B batches (`X, Y`) and a second lease-sensitive read `G_2` before exit. Compare mid-crossing handoff against waiting until bridge exit, checkpoint+replay, and full recheck under arrival delay.
- **Old-task retention check:** Check A/C at the mid-crossing seam, between `G` and `G_2`, and after exit; include a C slice that breaks if the importer delays bridge exit by one extra B step.

#### 04. Multi-hop relay handoff preserving ≥2 schedules across `k` blind importers (P)
- **Mechanism:** Chain `k` sequential blind handoffs (`I_1 ⊂ I_2 ⊂ ... ⊂ I_k`), updating `b_used` monotonically and enforcing a residual-width invariant (`≥ 2` distinct B schedules) at each hop without ever re-reading earlier learners' private states.
- **Novelty vs nearest prior art:** Sequential assume-guarantee composition (Pacti) chains static components; here each hop consumes part of a shared poset and tests whether over-approximation tax collapses schedule freedom to 1 before hop `k`.
- **Cheapest first test:** Run a 3-hop chain on an 8-job poset with hidden slot drift at each hop. Measure surviving distinct B schedules, false admissions, and cumulative proof bytes vs per-hop full recheck and cached replay.
- **Old-task retention check:** Evaluate A/C at every hop boundary and after the final suffix; include a cumulative rare-C drift that stays invisible at hop 1 and crosses the floor at hop 3 if budgets are not summed.

#### 05. Escrow-split handoff for parallel importers finishing disjoint residual branches (P)
- **Mechanism:** Partition `D \ I` along an independent cut into two sibling handoff packets with split remaining lease budgets (`b_1 + b_2 ≤ b_rem`) and a certified rejoin check before the common suffix, letting two blind importers schedule their branches concurrently.
- **Novelty vs nearest prior art:** Assume-guarantee decomposition and PR #181 merge-aware budgets allocate partner headroom; the candidate is splitting an already half-executed partial order into concurrent residual schedule rights.
- **Cheapest first test:** Split a 6-job residual poset into two 2-job branches plus a shared suffix, with one cross-branch carry interaction. Compare escrow-split handoff against serial handoff, Pacti resource splitting, and full joint recheck at equal bytes.
- **Old-task retention check:** Check solo A/C on each branch and joint A/C at rejoin, planting a rare C slice sensitive only to simultaneous carry from both branches.

#### 06. Non-resettable spent-budget witness against hidden-slot near misses (I)
- **Mechanism:** Represent `b_used` as a minimal per-channel carry occupancy vector (bound on each armed hidden-to-visible path) rather than a single scalar, so an importer cannot launder a half-armed slot by resetting step counters or re-anchoring `Φ_pub`.
- **Novelty vs nearest prior art:** PR #176 leakage leases track scalar perturbation quotas; this audit tests whether scalar `b_used` systematically admits near misses when two channels carry opposite signs or different expiry horizons.
- **Cheapest first test:** Build a 2-channel version of Fixture 1 where total scalar budget matches but one channel sits at `5/4` of a `3/2` cliff. Compare vector `b_used`, scalar `b_used`, and full state export on false admissions per byte.
- **Old-task retention check:** Bind a rare A slice to channel 1 and a rare C slice to channel 2; verify scalar budgets falsely admit a swap that breaks channel 1 while vector `b_used` catches it.

#### 07. Seam-conflict detector for public checks that hide a prefix-order split (I)
- **Mechanism:** Audit whether two legal prefix orders of `I` satisfy identical `(Φ_pub, b_used)` yet induce incompatible residual safe sets in `D \ I`; when found, emit the concrete prefix-pair witness to force either a finer public check or a narrower residual DAG.
- **Novelty vs nearest prior art:** Counterexample-guided refinement (CEGAR) and PR #107 footprint counterfeits already find indistinguishable states; this measures how often realistic half-finished cuts suffer hidden prefix splits.
- **Cheapest first test:** Enumerate all cuts `I` of a 6-job nonlinear ReLU toy with masked momentum; count cuts with identical `Φ_pub` but diverging residual safe sets, and compare seam-conflict tightening against naive full-prefix logging.
- **Old-task retention check:** Require the detected seam conflict to correspond to a genuine held-out A/C failure on at least one residual extension, not a spurious over-approximation gap.

#### 08. Rollback-free abort at the handoff seam via certified residual fallback (P)
- **Mechanism:** Pair every multi-order handoff packet with one certified zero-choice fallback completion inside `D \ I` that requires no source weights or prefix rollback, so an importer whose arrival queue violates every multi-order branch exits safely in place.
- **Novelty vs nearest prior art:** Safe fallback policies exist in reach-avoid and simplex control; the CL bet is binding a source-free residual fallback into the same handoff budget so refused imports never pay checkpoint-restore cost.
- **Cheapest first test:** Feed blind importers both in-scope queues and out-of-scope delayed queues after handoff at `I`. Compare residual-fallback handoff against checkpoint rollback plus replay and conservative refusal at equal bytes and latency.
- **Old-task retention check:** Measure A/C along the fallback path itself and after the common suffix, ensuring fallback never trades old-task retention to avoid rollback.

#### 09. Cut-placement audit: where in `D` does handoff maximize residual freedom per byte? (I)
- **Mechanism:** Sweep the handoff cut `I` from empty prefix to pre-launch to mid-crossing, pricing packet size, residual schedule count, and blind-importer acceptance rate to identify whether mid-execution handoffs beat handing off only at clean task boundaries.
- **Novelty vs nearest prior art:** Checkpointing and pipeline-cut placement are standard systems engineering; this is a falsification audit checking whether mid-order handoffs actually earn their overhead over boundary-only handoffs.
- **Cheapest first test:** Sweep all legal down-sets `I` on 6- and 8-job posets under varied queue arrivals; compare mid-order cuts against start-only (`I = ∅`) and post-bridge cuts at matched total bytes and B utility.
- **Old-task retention check:** Track worst-prefix A/C across all tested cuts to ensure high-freedom cuts do not sit on fragile transient retention valleys.

### Schedule-preserving universal teaching (Seed B: #195#19)

#### 10. Certify one truthful example over the full history-by-order rectangle (P; inherits #195#19)
- **Mechanism:** Select one independently truthful example `e` from the frozen pool and certify `safe(e, h, σ)` jointly over `H(z) × S` with `|S| ≥ 2` genuinely distinct B schedules, guaranteeing blind multi-order choice without decoding `h`.
- **Novelty vs nearest prior art:** Conformant planning encodes `H(z) × S` and multi-learner teaching handles unknown learners; the candidate is a reusable CL teaching receipt that preserves schedule breadth across hidden optimizer histories.
- **Cheapest first test:** Run Fixture 2's positive case (`H(z) = {1, 3}`, `S = {σ_1, σ_2}`). Compare `e_joint` against `e_singleton`, `e_point`, conformant planning, PR #187 #11 single-swap unlocking, and same-pool MTT at matched B utility.
- **Old-task retention check:** Audit A/C on every cell of `H(z) × S`, specifically verifying the cross-pair `(h_2, σ_2)` that both single-axis baselines miss.

#### 11. Anti-diagonal teaching without slot coalescence (P)
- **Mechanism:** Explicitly search for truthful examples that keep all cross-pairs `(h, σ)` inside the two-clock safe region *without* forcing successor slots across `H(z)` to merge, testing whether non-coalescing examples unlock schedules that coalescence-seeking teachers cannot reach.
- **Novelty vs nearest prior art:** Synchronizing/reset words (PR #108) collapse hidden state; here the teaching update leaves hidden slots distinct while making their future schedule-safety cones overlap.
- **Cheapest first test:** Construct a 2-slot masked momentum toy where every coalescing truthful item violates A retention or collapses `|S| = 1`, while a non-coalescing truthful item keeps `|S| ≥ 2`. Compare against coalescing-only teaching and exact belief search.
- **Old-task retention check:** Verify A/C separately on each non-coalesced successor history and confirm no rare slice is silently traded away to force coalescence.

#### 12. Teach for incomparable B-arrival regimes, not raw permutation count (P)
- **Mechanism:** Score candidate truthful examples by how many mutually incompatible external arrival-queue constraints (e.g., `X`-must-precede-`Y` vs `Y`-must-precede-`X`) their certified family serves, preventing vacuous gains from commuting or redundant swaps.
- **Novelty vs nearest prior art:** Partial-order teaching (PR #186, #195) counts linear extensions; weighting by incomparable B-arrival regimes ties schedule breadth directly to real blind-importer utility.
- **Cheapest first test:** Add two commuting decoy batches to Fixture 2 so a singleton-B-order example still has 4 raw extensions while `e_joint` serves both `X`-first and `Y`-first queues. Compare permutation-count vs arrival-regime selection on blind-importer acceptance.
- **Old-task retention check:** Check A/C on both arrival regimes and on a forced-delay queue where neither regime matches and the importer must refuse.

#### 13. Non-factorability witness when every row and column succeeds but the product fails (I)
- **Mechanism:** When no truthful example satisfies `H(z) × S` even though every single `h` has a multi-order item and every single `σ` has a universal item (Fixture 2's negative case), emit the minimal 2×2 (or `k`-cell) product obstruction to justify collapsing to `|S| = 1` or buying a probe.
- **Novelty vs nearest prior art:** Minimal unsatisfiable cores and PR #190 #09 coalition obstructions already witness infeasibility; this is a diagnostic separating true product non-factorability from an incomplete search.
- **Cheapest first test:** Run Fixture 2's widened class `H(z) = {0, 4}` alongside a decoy class where one extra truthful example makes the product feasible. Compare against cached exact solvers and single-axis heuristic checks.
- **Old-task retention check:** Include a truthful item that satisfies both clocks on all 4 cells but breaches rare C on `(h_2, σ_1)`; the obstruction must reject it and preserve A/C on the fallback.

#### 14. One-example vs two-example teaching frontier for unlocking residual schedules (I)
- **Mechanism:** Map the Pareto trade-off between spending 1 truthful example (keeping `|S| = 1` or `2`) versus 2 truthful examples (unlocking a wider residual poset) at fixed total update budget and B utility, charging the extra teaching step's latency against queue gains.
- **Novelty vs nearest prior art:** Machine teaching complexity (teaching dimension) already studies sample count; this prices extra truthful updates specifically against blind-importer scheduling flexibility.
- **Cheapest first test:** On an 8-job nonlinear toy with 3 hidden histories, compare 0-, 1-, and 2-example universal teaching against same-budget replay and MTT on admitted blind queues and B utility.
- **Old-task retention check:** Verify that the second teaching example does not erode A/C margins on earlier prefixes or trigger an earlier lease expiry.

#### 15. Retention-coupled universal teaching across diverging B-head prefixes (I)
- **Mechanism:** Require the universal example `e` to keep rare A/C slices above floor across *every* unlocked B-order prefix when different orders expose different intermediate B heads to `M`, blocking examples that buy clock safety at the expense of one branch's retention.
- **Novelty vs nearest prior art:** Certified retention (CABA `2610.40740`, PR #195 #01) checks fixed prefixes; this tests whether universal teaching over `H(z) × S` systematically shifts retention risk onto the unfavoured schedule.
- **Cheapest first test:** Couple rare C to `w_X` on `σ_1` and to `w_Y` on `σ_2` in Fixture 2; compare retention-coupled selection against clock-only universal teaching plus post-hoc pruning at equal compute.
- **Old-task retention check:** Measure worst-slice A/C across all `(h, σ)` pairs and confirm zero hidden retention regressions on the secondary schedule.

#### 16. Interior-schedule soundness: does certifying two extreme orders cover their interleavings? (I)
- **Mechanism:** Test whether a truthful example certified for two extreme schedules (`σ_1, σ_2`) remains safe for intermediate linear extensions in the same poset, or whether nonlinear ReLU/momentum interactions create an unsafe interior schedule between two safe endpoints.
- **Novelty vs nearest prior art:** Convexity/monotonicity checks in interval verification and PR #152 gate-crossing bounds address interior failures; this is a falsifier against certifying `D \ I` by testing only extremal permutations.
- **Cheapest first test:** Build a 4-batch ReLU toy with one gate flip occurring only on an intermediate interleaving `σ_mid` between safe `σ_1` and `σ_2`. Compare extremal-order teaching against full-ideal checking and exact enumeration.
- **Old-task retention check:** Place the rare A/C failure specifically on `σ_mid` so extremal-only checks report 100% retention while the interior schedule breaches the floor.

#### 17. Blind multi-order teaching versus one paid probe plus specialist teaching (I)
- **Mechanism:** Directly price the cost of insisting on a single blind example over `H(z) × S` against spending one lawful probe to split `H(z)` (as in PR #179) and then issuing a history-specific multi-order example.
- **Novelty vs nearest prior art:** Value of information (EVSI) and PR #179 already trade examples against probes for single replies; this maps the exact break-even when the objective is preserving ≥2 schedules rather than 1.
- **Cheapest first test:** Sweep probe cost and probe delay on Fixture 2 (both `H = {1, 3}` and `H = {0, 4}`). Compare blind universal teaching, probe-then-specialize, and exact costed POMDP planning at matched total budget.
- **Old-task retention check:** Evaluate A/C during probe execution delay, on both post-probe branches, and on a noisy probe outcome that forces refusal.

### Joint handoff × multi-order teaching & falsification controls

#### 18. Seam-time universal teaching to reopen collapsed residual schedules (P)
- **Mechanism:** When Learner 1's executed down-set `I` consumes enough lease budget that `D \ I` collapses to a single safe schedule, apply one independently truthful example `e` *at the handoff seam*—certified over `H(z_I) × LinExt(D \ I)`—to restore ≥2 distinct residual B schedules for the blind importer without resetting `b_used`.
- **Novelty vs nearest prior art:** Neither static handoff (#195#07) nor pre-execution universal teaching (#195#19) rescues a half-spent poset mid-flight; the bet is using one truthful update at the seam to buy back scheduling freedom that the prefix spent.
- **Cheapest first test:** Start from Fixture 1 after a heavy prefix `I` that leaves only `σ_1` safe; apply one truthful seam example from the frozen pool to reopen `σ_2` across both `E, T` and `T, E` hidden states. Compare against stacked #195#07 + #195#19, checkpoint rollback, and full recheck at equal bytes and updates.
- **Old-task retention check:** Verify A/C before the seam, immediately after `e`, across both reopened residual schedules, and after the common suffix; include a seam example that reopens `σ_2` for clocks but breaks rare C.

#### 19. Pre-paid handoff teaching: exporter teaches once so `N` blind importers pay zero teaching steps (P)
- **Mechanism:** Place the schedule-preserving universal example `e` inside the exporter's executed prefix `I` before serialization, so the exported packet `(I ∪ {e}, Φ_pub, b_used, D \ I, Π_I)` already guarantees ≥2 distinct residual schedules to every downstream blind importer at zero importer teaching latency.
- **Novelty vs nearest prior art:** Amortizing proof generation over multiple consumers is standard proof-carrying code; the CL candidate is amortizing a *training* update across independent blind importers with distinct arrival queues.
- **Cheapest first test:** Fork 8 blind importers with randomized B-arrival queues from one half-finished exporter state. Compare pre-paid exporter teaching against per-importer seam teaching, cached belief planning, and full checkpoint+replay at matched total updates and bytes.
- **Old-task retention check:** Check A/C on every forked importer's chosen residual order and confirm that pre-paying `e` does not degrade A/C for importers that only ever execute the default order.

#### 20. Lease-surplus transfer: convert unused prefix budget into multi-order teaching feasibility (P)
- **Mechanism:** When Learner 1 finishes `I` strictly under its nominal lease allocation (`b_used < b_plan`), export the verified surplus `Δb = b_plan − b_used` inside the handoff packet to widen the admissible residual slack for `e`, turning an infeasible 2×2 `H(z_I) × S` teaching problem into a feasible one without resetting the lease.
- **Novelty vs nearest prior art:** Slack/budget carry-over exists in real-time scheduling and PR #176 leases; the joint bet is coupling verified prefix surplus directly to universal teaching feasibility across hidden histories and orders.
- **Cheapest first test:** In Fixture 2's negative class (`H = {0, 4}`, safe radius `2`), let Learner 1's conservative prefix earn a verified surplus `Δb = 1` (widening residual safe radius to `3`), making `g = 2` universally safe on all 4 cells (`v_G ∈ {−3, −1, 1, 3}`). Compare against fixed-budget handoff, scalar-only leases, and exact joint re-planning.
- **Old-task retention check:** Verify that spending `Δb` to widen clock slack never relaxes the held-out A/C floors, using a planted rare C slice whose margin does not scale with `Δb`.

#### 21. Equal-byte handoff amortization audit: handoff packet vs checkpoint + residual replay + cache (I)
- **Mechanism:** Freeze the handoff packet, retire the exporter, and measure total transfer bytes, importer check time, false admissions, and surviving distinct B schedules across `N` independent blind importers with unseen queues and hidden histories.
- **Novelty vs nearest prior art:** Proof-carrying code and witness caching already trade issuance cost for marginal checking; this is the economic falsifier testing whether handoff packets beat a simple checkpoint plus residual replay and cache.
- **Cheapest first test:** Sweep `N ∈ {1, 4, 16}` blind importers and out-of-scope queue fraction on 6- and 8-job nonlinear toys. Compare handoff packets against full checkpoints, residual replay plus semantic cache, and Pacti contracts at equal transfer bytes.
- **Old-task retention check:** Evaluate A/C on every admitted and refused importer path; count retention breaches separately by budget-reset bugs, scope misses, and unsound proofs.

#### 22. Smooth-world and gradient-accumulation null for handoffs and multi-order teaching (I)
- **Mechanism:** Replace the discrete launch/lease cliffs with smooth margin and carry curves, and compare every multi-order handoff and universal-teaching arm against gradient accumulation over the same remaining B batches at matched update latency and public launch opportunities.
- **Novelty vs nearest prior art:** Directly carries forward the ledger's bounded-delay kill against gradient accumulation and PR #113's smooth no-cliff null; a gain that only exists on planted step-function cliffs is not a CL primitive.
- **Cheapest first test:** Run Cards 01, 10, and 18 on both the discrete-cliff fixtures and smooth nonlinear MLP worlds from independent pools, including gradient accumulation and a no-import control at matched B utility. Kill the primitive claim if smooth worlds tie the stacked baseline or accumulation.
- **Old-task retention check:** Match pre-handoff A/C margins across all arms and evaluate vulnerable old slices throughout accumulation delay, mid-order handoff, and post-suffix continuation.

## Ranked deeper questions

1. **Does a half-finished order handoff preserve genuine blind scheduling freedom without resetting the lease or losing to a checkpoint plus residual replay?** Start with Cards 01, 02, 06, and 21 on Fixture 1 and a small nonlinear host: require `≥ 2` genuinely distinct residual B orders, zero false admissions on hidden-slot near misses, and a real bytes-or-check win over checkpoint + residual replay + cached Pacti at matched B utility and A/C retention.
2. **When does one truthful example strictly beat single-axis teaching on the full `H(z) × S` product?** Start with Cards 10, 11, 12, and 13 on Fixture 2 and a nonlinear ReLU/momentum host: isolate the 2×2 diagonal trap, require non-coalescing successor slots and incomparable arrival regimes, and test whether the gain survives against conformant planning and a paid slot probe (Card 17).
3. **Can seam-time or pre-paid universal teaching rescue a half-spent handoff in a way stacked #195#07 and #195#19 cannot match?** Start with Cards 18, 19, and 20: test whether one truthful example at (or just before) handoff reopens collapsed residual schedules or converts prefix lease surplus into multi-order feasibility across `N` blind importers at lower total work than rolling back or re-proving.
4. **Do handoff freedom and multi-order teaching survive smooth dynamics, multi-hop relays, and gradient accumulation?** Cross Cards 04, 16, and 22: if over-approximation tax collapses `|S|` to `1` within two blind hops, or if smooth no-cliff worlds and gradient accumulation erase the order advantage, keep the failure witnesses and stop calling the handoff a primitive.

**Verdict:** Keep half-finished handoff continuity (Seed A) and history-by-order universal teaching (Seed B) gated against their own stacked baselines—especially checkpoint+replay+cache, conformant planning, and gradient accumulation—before claiming a joint primitive. The combined seam-teaching handoff earns primitive status only if it transfers reusable multi-schedule choice across blind importers in smooth nonlinear dynamics without surrendering B utility or ordinary old-task retention.
