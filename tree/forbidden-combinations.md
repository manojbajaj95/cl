# Forbidden update combinations: protecting old skills with clauses, not slots

**Status:** Ideas only; no experiments, code, or GPU. **Parent:** [Forgetting as unregistered dependence](unregistered-dependence.md), [PR #150](https://github.com/manojbajaj95/cl/pull/150), card 4. **Review seed:** [flood-triage row 242](https://github.com/manojbajaj95/cl/blob/9c5ab08efb7eb8daf0e8c160506e7c1c84e9d37d/reviews/flood-triage.md#L242), score 3: store forbidden combinations of read changes ("do not change both fallback channels") instead of the union of slots, so each change stays allowed alone; bound the interaction order and leave higher orders uncertified.

## What the hypothesis claims

Every common protection object is a *conjunction*: EWC and masks protect each important slot, GPM/OGD forbid every direction in a retained subspace, and replay pushes back on the old loss as a whole. A **combination constraint** (a *clause*) is a different object. It names a set of channels C and per-channel tolerances τ, and forbids only the realized writes that move *every* channel in C beyond its tolerance on A's protected domain. Each channel can still change on its own. A k-of-n group generalizes this to "at most n−k of these n channels may move." A clause is about *write effects* (how much a channel's contribution to A changes on A's inputs, as the parent defines it), not about weight distance.

**Why slot and subspace methods cannot express it.** Take a fallback pair: A's output is y = OR(a, b), and both channels are on for A's inputs. The safe set {δ_a = 0} ∪ {δ_b = 0} is a union of two subspaces. The smallest subspace containing it is the whole plane, so any linear projector has three choices: freeze one channel (a hitting set), freeze both (what GPM does when both read old activations, overprotecting), or freeze neither (losing A). A clause keeps all safe writes and can switch which channel it keeps over time.

**Why local importance scores miss it.** For a smooth OR, y = 1 − (1 − s_a)(1 − s_b) with both channels saturated at s ≈ 1, ∂y/∂s_a = 1 − s_b ≈ 0. The Fisher, EWC importance, per-unit ablation effect and first-order output sensitivity of *both* channels are near zero. The whole effect is the interaction term, which only shows up under a finite joint change. This is the blind spot that [Conditional Co-Ablation](https://arxiv.org/abs/2607.01940) (CoAx) states for circuits: a perfectly dormant backup looks the same as an irrelevant component to intact-state per-unit scores. The [Hydra effect](https://arxiv.org/abs/2307.15771) and [backup/counterweight analyses](https://arxiv.org/abs/2610.02173) show that such redundancy occurs in trained LMs. Replay has the same blind spot for a different reason: while one backup survives, A's loss is flat, so the replay gradient does nothing to stop B from erasing the second backup. Replay *repairs* after the first break; a clause *prevents* it.

**What would make this a protection object and not a relabelled interaction score.** (i) It is checked on the realized finite write, not on a Taylor expansion. (ii) It leaves B strictly more feasible writes than the union mask or the GPM subspace at equal protection. (iii) Every clause includes its consumer: per the [#117 kill](https://github.com/manojbajaj95/cl/pull/117), a pinned producer means nothing if the OR gate itself moves. (iv) It must specify how it changes over time: the kept literal may move, but only after the other one is verified intact.

**What would constitute a proof.** Suppose channels C feed a consumer g that is a k-of-n threshold over channel contributions, g is fixed on the protected domain D, and A's margin on D exceeds the worst output shift that within-tolerance channels can produce. If a write leaves at least k channels within tolerance on D, A's output on D is unchanged. The statement is conditional on the channel decomposition being exact and the consumer being frozen, and it gives no guarantee for clauses of higher order than were registered. Without an order bound (card 14), "no clause violated" is evidence, not proof.

**Where clauses should win and where they should lose.**

| Regime | GPM / OGD | Matched replay | Clauses |
|---|---|---|---|
| Redundant k-of-n channels, and B needs some of them | Overprotects (freezes all) or misses (backups invisible) | Acts only after the last backup breaks; worst prefix is bad | Should win: B borrows n−k channels and A never breaks |
| Series structure (every channel necessary) | Fine | Fine | Collapses to singletons; ties at best |
| High-order or rotated redundancy | Fine | Fine | Clause count or channel naming explodes; likely loses |
| Graceful (unsaturated) dependence | Sees it | Sees it early | No advantage |
| Dense writer moving every channel a little | Fine | Fine | Every clause fires; becomes a veto; loses |

The claim is only as large as the first row's share of real hosts. Card 15 measures that share, and card 17 is the required falsifier.

## Common CPU test and controls

- **Shared world:** The parent's toll world, plus an enumerable Boolean/threshold circuit and a small gated MLP with planted structure: a 2-of-2 fallback pair (OR), a 2-of-3 vote, a 1-of-3 triple, an XOR pair (changing *both* is safe, changing one is not), and the reviewer's planted three-way exception. B is a new region whose cheapest solution reuses the redundant channels. C is unrelated. Cross redundancy degree, clause order, B's overlap with redundant channels, basis rotation of the channels, saturation, and learning rate.
- **Arms:** Unconstrained SGD; EWC/Fisher; singleton-ablation mask and union mask at equal bytes; tuned [GPM](https://arxiv.org/abs/2103.09762), [OGD](https://arxiv.org/abs/1910.07104), [TRGP](https://arxiv.org/abs/2202.02931) and [SGP](https://arxiv.org/abs/2302.01386); [SPACE-LoRA](https://arxiv.org/abs/2609.34453), [DUET](https://arxiv.org/abs/2611.29269) and [CABA](https://arxiv.org/abs/2610.40740) acceptance; replay and DER logits given the clause registry's bytes plus discovery compute; CoAx-ranked "freeze the backups" (the strongest interpretability control); a BOCS-style sparse second-order surrogate used as a write gate (the ledger's coded-merge kill); random clauses of equal count and size; the oracle clause set.
- **Decision rule:** A/C retention against *matched attained* B progress (as in the parent), plus first break and worst prefix on an independent old holdout. Count registry bytes, discovery queries (charged as replay storage or compute), rejected writes and false-safe writes. Start with the oracle clause set in the planted regime: if it does not beat tuned GPM *and* matched replay on worst prefix at matched B, stop. If it only wins with axis-aligned planted channels, do not claim it for learned hosts.

**Ledger screen.** The [idea ledger](https://github.com/manojbajaj95/cl/blob/9c5ab08efb7eb8daf0e8c160506e7c1c84e9d37d/reviews/idea-ledger.md) shapes the cards below as follows.
- **Coded merge interference (killed as BOCS).** Fitting a sparse pairwise surrogate from group evaluations is prior art. No card here claims that; BOCS-as-gate is a control, and discovery cards must beat it at equal queries.
- **Sparse-write certificates (killed) and functional syndromes (falsified: damage was dense).** No card assumes sparse damage; the cards assume sparse *redundancy structure*. Where damage is dense, the regime table predicts a loss.
- **#117 read pinning (killed).** Every clause includes its consumer.
- **Gramian forecasts (killed).** No card uses a Gramian.
- **Sibling parent cards.** [PR #150](https://github.com/manojbajaj95/cl/pull/150) cards 15 (finite safe region), 16 (certificates that do not compose) and 18 (impossibility witnesses) cover neighbouring ground; cards below that overlap them say what differs.
- **Interpretability prior art not built for continual learning.** CoAx, [WISE/JuntaLearner](https://arxiv.org/abs/2610.04017), [CFS](https://arxiv.org/abs/2609.39259), [neuron-subset necessity](https://arxiv.org/abs/2611.13885) and [closure-validated circuits](https://arxiv.org/abs/2606.09607) all find interacting component sets. None of them uses those sets to gate later writes.
- **CL work closest in spirit.** [Pathway protection](https://arxiv.org/abs/2505.18568), [IGFA](https://arxiv.org/abs/2607.09202) and [functional compatibility](https://arxiv.org/abs/2608.22462) are the nearest. None of them stores a disjunctive constraint.

## Idea cards

### What a combination constraint is

#### 1. Disjunctive gradient projection: keep a hitting set, not a span
- **Mechanism:** Each clause needs at least one literal kept within tolerance. At each step (or block), choose the hitting set of frozen channels that removes the least of B's gradient mass (weighted minimum hitting set, exact for small clause sets), then project B's update onto the corresponding union-of-subspaces component.
- **Novelty vs nearest prior art:** GPM, TRGP and SGP project onto one fixed subspace complement (TRGP relaxes it inside a trust region, still a single convex region). This projects onto a subspace *arrangement* and re-chooses the component as B's needs change.
- **Cheapest first test:** 2-of-2 and 2-of-3 toys where B's gradient lands on channel a early and on channel b later. Compare against GPM, union mask and EWC at matched B loss.
- **Old-task retention check:** Exhaustively evaluate A after every step, including inputs where only one channel is active. Report the steps where the chosen hitting set changed.

#### 2. Cardinality budgets for k-of-n redundancy
- **Mechanism:** Register one counter per redundancy group: "at most n−k channels may be out of tolerance." This stores n + 1 numbers instead of C(n, n−k+1) clauses, and admission is a counter check on the realized write.
- **Novelty vs nearest prior art:** k-out-of-n reliability and N−1 security in power grids (the system must survive any single outage) use exactly this budget. No CL method found here budgets *how many* redundant channels may move rather than *which*.
- **Cheapest first test:** 2-of-3 and 3-of-5 votes inside a gated MLP. Compare the counter against the enumerated clause list, union mask and GPM on B progress at equal A retention.
- **Old-task retention check:** Evaluate A on inputs that activate only k channels; this is where an over-generous budget breaks first.

#### 3. Required co-changes: anti-clauses
- **Mechanism:** Some pairs are safe only *together*: an XOR pair, a producer scale and its consumer's inverse scale, a sign flip on both sides of a ReLU-free path. Register "either neither or both" and admit coordinated writes that a singleton or subspace rule would reject.
- **Novelty vs nearest prior art:** Function-preserving symmetries (rescaling, Net2Net) are known and the parent's card 1 protects producer–consumer pairs. The new part is that a constraint *language* containing both clauses and anti-clauses can admit writes that every conjunctive protector forbids.
- **Cheapest first test:** XOR pair and ReLU rescaling pair in the toy. Count how many of B's useful writes each arm admits; GPM must forbid both singletons and the pair.
- **Old-task retention check:** Check A after admitted pair writes and when one half of the pair lands late (a write that interleaves with another B step).

#### 4. Rotating custody of the kept channel
- **Mechanism:** The literal that guards a clause may move from a to b only through a hand-off: verify b intact on A's domain, change the guard, then release a. Over a long stream B can use every redundant channel in turn, never all at once.
- **Novelty vs nearest prior art:** Rolling upgrades and two-person rules in operations; PackNet and other static allocation methods keep allocations fixed. Parent card 10 retires an obligation once a replacement exists; this keeps the obligation and moves its carrier.
- **Cheapest first test:** A sequence of B tasks that each want a different member of a 1-of-3 group. Compare custody rotation against a static hitting set, union mask and matched replay.
- **Old-task retention check:** A at every hand-off, including a hand-off where the verification set misses an input only the old guard served.

#### 5. Product barriers: soft clauses for smooth hosts
- **Mechanism:** Replace the hard clause with the penalty Π_{i∈C} min(d_i/τ_i, 1), where d_i is channel i's measured change. The penalty is zero while any channel stays put and grows only as all of them move.
- **Novelty vs nearest prior art:** EWC with a full Fisher, or a Hessian penalty, is quadratic and evaluated at θ0, where the redundant cross-term is ≈0 (see above). The product barrier is non-local and non-convex by design.
- **Cheapest first test:** Soft-OR host swept from saturated to unsaturated. Compare against full-Fisher EWC, a Hessian penalty and the hard clause; find the saturation level where the barrier stops helping.
- **Old-task retention check:** A's margin distribution, not just accuracy, so a barrier that lets every channel drift to just under tolerance shows up.

#### 6. Clauses over learned subspaces, not named units
- **Mechanism:** Channels are subspaces U_1…U_n found by A-domain interventions. The clause says "not all of these subspaces move," and channel identity is checked for gauge stability under refits.
- **Novelty vs nearest prior art:** GPM and SPACE-LoRA protect one merged basis; parent card 5 transports relations across relabelling. Here, redundancy that is not aligned with the axes gets its own subspaces, and the safe set is their arrangement.
- **Cheapest first test:** Apply a random orthogonal rotation to the 2-of-2 toy's channel space. Compare subspace clauses against unit clauses (which should fail), GPM and replay.
- **Old-task retention check:** A after B under several rotations; report how much of the advantage over GPM survives as the rotation angle grows.

### How clauses are discovered

#### 7. Conflict-driven clause learning from broken writes
- **Mechanism:** When a sandboxed B write breaks A, the set of channels it moved is a *nogood*. Shrink it to a minimal core by deletion-based reverts (QuickXplain/MUS style: undo half the moved channels, see if A still breaks) and register the core.
- **Novelty vs nearest prior art:** CDCL SAT solvers and minimal-unsatisfiable-subset extraction; parent card 3 repairs induced forgetting channel by channel. The new part is turning every observed break into a minimal joint constraint that gates future writes.
- **Cheapest first test:** Sacrificial B writes on the planted circuit. Count reverts per recovered clause and compare against CoAx, the BOCS surrogate and exhaustive pairwise ablation at equal queries.
- **Old-task retention check:** Retention on fresh B streams whose writes hit different channel subsets than the ones that produced the cores.

#### 8. Turn conditional co-ablation into write gates
- **Mechanism:** Run CoAx: remove a primary set, find components whose effect grows, and register the clause (primary ∪ backups, consumer). Unlike freezing the CoAx top-k, B may still change the primary *or* the backups.
- **Novelty vs nearest prior art:** CoAx and JuntaLearner find backups for explanation. Using them as a disjunctive write gate, and measuring the capacity that freeing one side gives back to B, is untested.
- **Cheapest first test:** On the toy and on a CPU GPT-2-small task with known backup heads (IOI name movers), compare CoAx clauses against CoAx freeze-top-k and GPM on a small fine-tune.
- **Old-task retention check:** The CoAx task's logit difference plus a held-out battery that uses the same heads, so a clause tuned to one behaviour is not credited for all.

#### 9. Adaptive group testing over write channels
- **Mechanism:** Find every minimal cut set of size ≤ k among n channels with pooled reverts: perturb groups, split positive groups, and use noisy group-testing decoding, aiming at O(k log n) queries per clause instead of n^k.
- **Novelty vs nearest prior art:** Group testing and Fourier-sparse set-function learning (Stobbe & Krause; Shapley interaction estimators such as [Faith-Shap](https://arxiv.org/abs/2203.00870) and [SVARM-IQ](https://arxiv.org/abs/2401.13371)) estimate interactions; BOCS fits a surrogate. The target here is exact minimal cut sets with a declared false-negative rate, which is what gating needs.
- **Cheapest first test:** Planted circuits with 1–20 cut sets of order 2–3 among 64 channels. Query count against BOCS and SVARM-IQ at equal recall of cut sets.
- **Old-task retention check:** Gate B with the recovered sets; count A breaks caused by cut sets the test missed.

#### 10. Free clause discovery from training-time dropout
- **Mechanism:** Dropout and stochastic depth already run thousands of joint ablations while A trains. Log masks and per-example A loss, and fit clauses to loss spikes that appear only when certain sets are co-dropped, at no extra forward passes.
- **Novelty vs nearest prior art:** Dropout is used as regularization or as an ensemble; nothing found uses its masks as a free interaction census for later protection.
- **Cheapest first test:** Train the gated MLP with dropout p ∈ {0.1, 0.3}; compare recovery of planted clauses against group testing at equal *extra* queries (zero for this arm).
- **Old-task retention check:** Gate B with dropout-derived clauses; A at matched B. Watch for clauses that dropout created by changing the host (card 12 is the deliberate version of this).

#### 11. Compile clauses from a known structure
- **Mechanism:** When A is partly programmed (compiled circuits, [programs-in-weights](https://github.com/manojbajaj95/cl/pull/39) style), read its fault tree and compute minimal cut sets exactly (e.g. [Fast-MCS](https://arxiv.org/abs/2602.16686)), then check them against the host by intervention.
- **Novelty vs nearest prior art:** Fault-tree analysis is standard reliability engineering; as a CL registry it is a borrowed tool and the oracle for cards 7–10.
- **Cheapest first test:** Compile the toll rules into a threshold circuit with deliberate fallbacks; compare compiled cut sets to learned clauses after A is fine-tuned (the host may have drifted from the compiled structure).
- **Old-task retention check:** A after B under compiled versus learned clauses, plus rare rule branches the compiled structure says are covered.

#### 12. Build redundancy so its clauses are known at birth
- **Mechanism:** Train A with structured group dropout so it implements a declared k-of-n code over designated channel groups. The clause is registered with no discovery, and B may borrow up to n−k channels per group.
- **Novelty vs nearest prior art:** Emergent redundancy (Hydra) and [LiteLoRA](https://arxiv.org/abs/2606.28117)'s adapter redundancy are found after the fact. This plans redundancy as *lendable capacity* and charges its cost at A training.
- **Cheapest first test:** Width-matched hosts: planned 2-of-3, emergent (plain dropout), none. Measure total A+B accuracy after B at equal parameters.
- **Old-task retention check:** A's accuracy at acquisition must match the non-redundant host; no credit for redundancy bought with worse A.

#### 13. Clauses relative to a writer
- **Mechanism:** Only test combinations the declared writer can reach (e.g. rank-r LoRA in layers 3–4). A clause that no feasible write can trigger is dropped, and the registry is invalidated when the writer family changes.
- **Novelty vs nearest prior art:** Parent card 2 does this for singleton reads; for clauses it also prunes the exponential order space, which is where the saving would be.
- **Cheapest first test:** Two LoRA writers with different layer placements; registry size and discovery cost per writer, then cross-applied to detect stale-registry false passes.
- **Old-task retention check:** A after held-out writes inside the family, and after a switch to the other writer with the stale registry.

#### 14. Certify every order above a bound without enumerating it
- **Mechanism:** If the consumer is a thresholded sum with margin m and each channel's maximum contribution change on D is c_i, every set whose Σ c_i < m is safe. A knapsack check therefore certifies most high-order combinations, and only the rest need clauses or tests.
- **Novelty vs nearest prior art:** Interval bound propagation and CABA bound endpoints. Using a margin knapsack to *bound clause order*, which the reviewer asked for, is the specific new use.
- **Cheapest first test:** Fraction of the 2^n channel subsets certified safe by the knapsack versus exhaustive enumeration on 16–24-channel hosts, as margin and contribution spread vary.
- **Old-task retention check:** Run B gated by knapsack + low-order clauses; any A break caused by a certified-safe set refutes the bound.

### When clauses beat GPM and replay

#### 15. Redundancy census of real hosts
- **Mechanism:** For each old behaviour, measure the share of joint-ablation effect not explained by singleton effects, at orders 2 and 3, over a declared channel family. This share is the ceiling on what clauses can add.
- **Novelty vs nearest prior art:** Hydra, CFS and [2611.13885](https://arxiv.org/abs/2611.13885) measure redundancy and subset necessity for interpretability. Tying the census to a predicted CL gain is the falsifier this node needs.
- **Cheapest first test:** Small MLPs trained with and without dropout, then a CPU GPT-2-small pass over IOI and two factual-recall tasks with head-level channels.
- **Old-task retention check:** Not a training run; the check is whether census mass predicts card 17's gap over GPM across hosts (rank correlation with a CI).

#### 16. Prevention versus alarm: clauses against replay
- **Mechanism:** Show that replay's corrective gradient is ≈0 while one backup survives, so replay responds after the break. Clauses refuse the second write. Predict clause wins on first break and worst prefix, ties at end of stream.
- **Novelty vs nearest prior art:** Replay and MIR ([1908.04742](https://arxiv.org/abs/1908.04742)) choose *what* to replay by current interference. A flat old loss gives MIR nothing either, which is the testable claim.
- **Cheapest first test:** Saturated 2-of-2 toy, learning-rate sweep, replay and MIR at the registry's byte budget. Plot A loss over time.
- **Old-task retention check:** Worst-prefix A accuracy and the number of steps A spends broken; end-of-stream accuracy alone hides the effect.

#### 17. Break-even map against GPM (required falsifier)
- **Mechanism:** Sweep redundancy degree n, clause order, B's overlap with redundant channels, rotation angle and saturation. Plot where *oracle* clauses beat tuned GPM, OGD and matched replay at matched B, then where learned clauses do.
- **Novelty vs nearest prior art:** Parent card 24 maps read-set protection against replay; this maps the disjunctive object specifically. It is a falsifier, not a method.
- **Cheapest first test:** Enumerable threshold hosts over a 5 × 5 grid of (overlap, rotation), 10 seeds each.
- **Old-task retention check:** A and C at the same B error across the grid; require a region where the oracle wins clearly, and report where it ties or loses.

#### 18. Spend replay only where one backup is left
- **Mechanism:** Use clauses to find A inputs where all but one literal of a clause have already moved. Those inputs carry all of A's remaining risk, so put the replay budget there instead of on uniformly sampled A inputs.
- **Novelty vs nearest prior art:** MIR and GSS pick samples by loss change or gradient diversity, which is near zero for these inputs until the last backup goes. The selector is structural.
- **Cheapest first test:** Equal-byte replay: uniform, MIR, GSS, clause-guided, on the 1-of-3 toy with B gradually consuming channels.
- **Old-task retention check:** A on single-support inputs, plus overall A and C, to catch a selector that starves ordinary inputs.

#### 19. Series–parallel decomposition: subspaces for series parts, clauses for redundant parts
- **Mechanism:** Fit a reliability block diagram to A's dependency: necessary blocks get GPM-style subspace protection, parallel blocks get clauses or budgets. Each part uses the object that represents it exactly.
- **Novelty vs nearest prior art:** SPACE-LoRA allocates subspace protection by module sensitivity; no method picks the *type* of protection per block.
- **Cheapest first test:** Mixed host with one series path and one 2-of-3 group. Compare decomposition with pure GPM, pure clauses and union mask.
- **Old-task retention check:** A on inputs that use each block alone, and C.

### Bigger bets

#### 20. Common-mode backups across old tasks
- **Mechanism:** When A and C both name the same backup channel, the shared backup is a common-cause failure point. Merge their clauses into the conjunction and flag channels that guard many tasks, which B should never claim.
- **Novelty vs nearest prior art:** Common-cause failure analysis in reliability. GPM merges activation bases across tasks but cannot tell a shared *backup* from a shared primary.
- **Cheapest first test:** A and C with disjoint primaries and one shared fallback; protect per task versus merged clauses, at matched B.
- **Old-task retention check:** A and C when B first claims A's primary and then the shared backup.

#### 21. Self-healing from the surviving channel
- **Mechanism:** After B moves channel a, re-teach a's *A-function* (or a fresh free channel) from the surviving backup b on unlabelled inputs, before b may move. A clause then becomes "not both, *within T steps of each other*."
- **Novelty vs nearest prior art:** Self-repair (Hydra) is passive. Distillation from a stored teacher needs storage; here the in-model backup is the teacher, so no old data or old model is kept.
- **Cheapest first test:** 2-of-2 toy and a stream where B wants both channels in turn; compare against custody rotation (card 4), replay and a stored-teacher distillation at equal bytes.
- **Old-task retention check:** A after each heal and after b is finally released; any A loss on inputs only a used to serve shows the heal was partial.

#### 22. Keep the redundancy level: re-replicate before it runs out
- **Mechanism:** Treat k-of-n as a storage code: when B's writes drop a group to its minimum, regenerate a replica into free capacity (repair bandwidth = A-domain distillation queries), as distributed storage re-replicates lost blocks.
- **Novelty vs nearest prior art:** Regenerating codes and HDFS re-replication; the [developmental-growth node](https://github.com/manojbajaj95/cl/pull/127) regenerates tissue. The new part is a CL invariant ("never fewer than k live copies") plus a repair cost.
- **Cheapest first test:** Long B stream on a 2-of-3 host; compare re-replication with no repair and with replay at equal compute and bytes.
- **Old-task retention check:** A over the whole stream, especially just after each repair and after a repair that copied an already-drifted replica.

#### 23. Shape A so its clauses are low order and writer-aligned
- **Mechanism:** During A training, penalize redundancy that is high order or spread across writer channels, and reward redundancy that aligns with units the writer can address. Clauses then stay short and cheap to check.
- **Novelty vs nearest prior art:** Parent card 6 shapes cheap read cuts; card 12 plants redundancy. This shapes the *form* of the clauses that emerge, without fixing them in advance.
- **Cheapest first test:** Compare shaping with plain dropout and card 12's planted code on registry size, discovery cost and B capacity after training.
- **Old-task retention check:** A at acquisition and after B; penalize shaping that hides dependence in a consumer the clauses do not cover.

#### 24. Fallback clauses for agent harnesses
- **Mechanism:** "Do not change both fallback channels" is literal in agents: a retry prompt and a backup tool, two retrieval paths, two skill files. Gate harness edits (prompt, tool, memory) with clauses learned from paired with/without runs.
- **Novelty vs nearest prior art:** Skill re-validation work ([harness self-testing node](https://github.com/manojbajaj95/cl/pull/65); SkillApt, SkillDelta) tests each skill alone. A joint fallback constraint on edits was not found there.
- **Cheapest first test:** A small tool-use agent with two planted fallbacks; an editing loop that rewrites one component per step. Compare clause gating with per-skill regression tests and a full replay suite at equal runs.
- **Old-task retention check:** Old task success when the primary tool fails (the case only fallbacks serve), plus normal success.

## Ranked deeper questions

1. **Is enough of A's dependence singleton-invisible for clauses to matter, and does the oracle clause set beat GPM and replay there?** Run the census (15) and the break-even map (17) first, with the replay-alarm test (16). Kill the direction for a host family if census mass is small or the oracle ties tuned GPM and matched replay on worst prefix at matched B.
2. **Can minimal clauses be found with fewer queries than the bytes replay would need?** Compare conflict-driven cores (7), group testing (9) and free dropout logs (10) against the BOCS surrogate and CoAx at equal queries. Report missed cut sets as false-safe risk, not only recall.
3. **Do clauses survive redundancy that is not aligned with named units?** Subspace clauses (6) and shaping (23) against rotation. If the advantage vanishes once channels are rotated, the object is a property of planted toys, not of learned hosts.
4. **Does disjunctive protection buy capacity over a long stream, not just one task?** Hitting-set projection (1), custody rotation (4), self-healing (21) and re-replication (22) against union masks and replay, scored by cumulative B progress at a fixed A floor. This is where "combination constraints are a new protection object" would be shown or refuted.
5. **Can the order bound be certified?** Knapsack certification (14) is what turns "no registered clause fired" into a guarantee; without it the registry is triage, not protection.
