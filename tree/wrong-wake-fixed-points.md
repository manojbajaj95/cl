# Wrong wake fixed points: when an idempotent wake settles on the wrong old answer

**Parent:** [Rented constraints](rented-constraints.md) ([PR #145](https://github.com/manojbajaj95/cl/pull/145)), developing its card #10 (wrong fixed points), card #11 (contraction certificate) and ranked question 2. **Grandparent:** [Bounded burial](bounded-burial.md) ([PR #142](https://github.com/manojbajaj95/cl/pull/142)) #11. **Triage:** [flood-triage.md rows 230–232](https://github.com/manojbajaj95/cl/blob/devin/1795531716-reviewer-verdicts/reviews/flood-triage.md#L230) (bounded burial, crossed evidence, cross-pool round 29; BCE4 "a wake must not wake the old world" is the stale-answer half of this node). **Status:** Ideas only; no experiments run; no GPU.

**Node question:** A wake-up `W` is a short, frozen, label-free training continuation on public data. It is *idempotent* when `W(W(θ)) ≈ W(θ)` on task outputs, so it can be issued blindly. How can we tell, without A's labels, when `W` has settled on a **wrong** answer (constant, polarity-flipped, mixed with another skill, or absorbed into B) or a **stale** one (an answer A had before it was revised)? And which wake dynamics **provably** settle only on the true, current old skill?

## Root cause: a public-data fixed point cannot know A's answer

`W` only sees public inputs and the host state `θ`. Its fixed set `Fix(W)` is wherever the public objective stops pulling. Whether A is right at a fixed point depends on information about A's labels, and the only place that information lives is the state the lease left behind. Four consequences follow.

1. **Symmetric twins are indistinguishable to `W`.** If a label symmetry `σ` (polarity flip of A, a permutation of A's classes) maps hosts to hosts and leaves the public data unchanged, then `W` is σ-equivariant. If `θ*` is a fixed point, so is `σθ*`. Idempotence, small displacement, output entropy and calibration are all identical at the two. **No label-free statistic of the fixed point alone can tell a flipped A from a correct A.** Only something that breaks `σ` can: a surviving payload in the host, a co-resident skill whose answers are tied to A's, or stored bits.
2. **Correctness is a property of the basin, not the fixed point.** A wake is correct for a host when the host lies in the basin of the fixed point that matches the host's own surviving payload. Detection must therefore look at the **path into** the fixed point (where it came from, what it passed through) or at the **neighbouring fixed points** (how many there are, how they were born), not at the end state.
3. **Gradient wakes seek depth, not recency.** If `W` descends a public energy, it goes to the deepest reachable basin. An answer A held for a long time before it was revised (`A_v1`) can leave a deeper basin than its short-lived revision (`A_v2`). Energy-seeking wakes then revive the stale answer. This is the BCE4 failure and the relapse in [benign relearning](https://arxiv.org/abs/2406.13356) and [syntax-driven relearning](https://arxiv.org/abs/2602.03379), seen as a basin race.
4. **"Stable" is not "right".** Convergence of the learning signal does not identify the external objective ([Stable but Wrong, 2603.21491](https://arxiv.org/abs/2603.21491)); self-generated signals destabilize test-time training ([2610.05076](https://arxiv.org/abs/2610.05076)); continual TTA collapses to a few classes ([2603.03796](https://arxiv.org/abs/2603.03796)). Those papers diagnose collapse in prediction space. Here the dynamics act in weight space on a buried skill, and the failure that matters most (the σ-flip and the stale revival) produces **no** collapse signature.

So the provable class has a specific shape. Split the host state into **payload** coordinates `p` (where the A distinction itself is stored; parent card 2) and **access** coordinates `a` (readout and interface alignment that B disturbs). A wake settles only on the true skill when:

- **(P1) Payload invariance.** `W` does not write `p`, or writes it only by a σ-equivariant contraction toward its current sign: `sign(p ∘ W) = sign(p)`.
- **(P2) Unique access completion.** For each payload, the public objective has exactly one fixed point in access coordinates inside the lease region (a contraction or strictly convex problem in `a` given `p`).
- **(P3) Proximal, not depth-seeking.** `W` returns the fixed point nearest the lease-end state in a declared metric, so a deeper but older basin does not win.

Then `Fix(W)` restricted to the lease region is a graph `a*(p)`, and the wake is correct exactly when the payload survived. P1–P3 are each testable on a CPU MLP and each can be partly certified. The negative controls from the parent bind every card: in a linear least-squares host no public wake can restore A's polarity after B overwrites `P_A`; a wake that resets stored coordinates is PackNet/saved deltas.

## What would count

The PR #142 and PR #145 contracts bind every card (randomized dormancy at fixed size; A passes when learned, may fail during the lease, must pass after `W`; frozen `W` on disjoint development histories; costs charged; baselines GPM/TRGP/SGP/FS-DGPM, EWC with the same `W`, PackNet with release, equal-byte saved deltas, DER++). This node adds:

- **Wrong-answer taxonomy, scored separately.** For every post-wake host report the fraction of A queries that are (i) correct, (ii) flipped (σ-image of correct), (iii) constant/collapsed, (iv) mixed with another co-resident skill (Hopfield-style mixture, [2610.40060](https://arxiv.org/abs/2610.40060)), (v) absorbed into B's answer, (vi) **stale** (the retired `A_v1` answer on inputs where `A_v1 ≠ A_v2`). A detector that only catches (iii) is an anti-collapse TTA method ([CAMA 2611.28461](https://arxiv.org/abs/2611.28461), [2611.12242](https://arxiv.org/abs/2611.12242)), not a contribution.
- **Twin families are required in every test.** σ-twins (A⁺/A⁻ hosts), revision twins (`A_v1→A_v2` hosts versus hosts that only ever learned `A_v2`, at equal total steps and matched `A_v2` margin), and A-naive hosts. A wake or detector that behaves identically on members of a twin pair cannot claim to detect that failure.
- **Detectors are label-free on the live host.** Development hosts may use labels to freeze thresholds; the live decision may not. Any stored bits (fingerprints, anchors) are charged and the same bits are given to replay baselines.
- **The decisive comparison** is post-wake A correctness at matched B progress and wake cost: the proposed dynamics or detector versus plain `W`, `W` plus an output-marginal anti-collapse check, `W` with random restarts and majority vote, and an equal-bit replay buffer.

## Idea cards

Shared toy unless a card says otherwise: width-64 ReLU MLP host; tasks A, then C, then B with overlapping features; lease of A's GPM directions to B as in parent card 1; `W` = 4 frozen public SGD steps; 16 development and 16 held-out histories; A⁺/A⁻ σ-twins and `A_v1→A_v2` revision twins; linear-host negative control. "Retention" always includes C and the untouched parts of A.

### A. Telling a wrong fixed point from the right one without labels

#### 1. Fixed-point census by perturbed restarts (primitive)

- **Mechanism:** From the lease-end state, launch `W` from K perturbed copies (random directions within the lease radius, plus permuted public batch orders). Cluster the end states by their A output pattern on public inputs (up to σ). One cluster means the host sits in a single basin; several clusters mean the wake is ambiguous here, whatever the main run's displacement says. The decision rule is multiplicity, never the answer itself.
- **Nearest art / delta:** Random restarts and ensembling in optimization; Hopfield retrieval studies count spurious attractors by restarts ([2609.07757](https://arxiv.org/abs/2609.07757)). Here the census is over a **repair operator's** fixed points in weight space and is used as a lease-level go/no-go, with σ-twins to show its blind spot.
- **Cheapest first test:** K ∈ {4, 16}; report AUROC of "multiplicity > 1" for wrong-after-wake versus correct-after-wake on held-out histories; compare with displacement-only and output-entropy detectors at equal forward/backward cost. Prediction from the root cause: it catches mixtures, collapse and stale revivals that compete with the true basin, and is blind to pure σ-flips where only the flipped basin is reachable.
- **Old-task retention check:** The census runs on forks; the live host keeps A, C and B unchanged. Report C and B at each clustered end state to check that the "majority" basin is not a B-collapsed one.

#### 2. Bifurcation alarm along the lease path (primitive)

- **Mechanism:** Wrong fixed points are usually **born** during the lease: as B moves θ, a fold or pitchfork bifurcation of `W` creates a new fixed point or swaps which one the host flows to. Track the smallest singular value of `I − J_W(θ_t)` (the Jacobian of one wake application, by power iteration on public inputs) along B's lease path. A near-zero dip marks a bifurcation; a pitchfork (symmetric dip) marks the onset of polarity ambiguity. End the lease before the first dip.
- **Nearest art / delta:** Bifurcation theory of modern Hopfield equilibria ([2609.07757](https://arxiv.org/abs/2609.07757)) studies how stored patterns split and merge with temperature; parent card 4 monitors wake displacement drift, which only rises after the basin has already changed. This card watches the **operator's spectrum** for the event that creates the wrong answer.
- **Cheapest first test:** On the MLP, record `σ_min(I − J_W)` every 10 B steps; label each lease end as correct or wrong after wake; test whether dips precede wrong outcomes by more steps than displacement drift does, at equal monitoring cost. Gate: dips must be larger than seed variance (ledger predictor gate).
- **Old-task retention check:** Leases ended by the alarm versus fixed-term leases: A per twin and revision family after `W`, C throughout, B at lease end.

#### 3. Path-continuation wake: follow the fixed point back (primitive)

- **Mechanism:** Before the lease, the host is at an awake fixed point `θ_0*`. As B moves θ, track that particular fixed point by numerical continuation (one Newton correction on `θ − W(θ)` per checkpoint, warm-started from the previous one). The wake then returns the **continued** fixed point, not whichever one plain `W` falls into. If the continuation fails (singular Jacobian, card 2), the lease is declared broken.
- **Nearest art / delta:** Homotopy continuation is standard in numerical analysis; parent cards 3 and 11 bound basin radius. Using continuation to keep the identity of an old skill's fixed point through another task's training is new, and it is label-free: identity is carried by continuity, not by A's answers.
- **Cheapest first test:** Compare continuation wakes with plain `W`, multi-round `W` and card 1's majority vote on the full wrong-answer taxonomy, at equal total Jacobian-vector products. Linear-host control: continuation must still fail there if B overwrote the payload.
- **Old-task retention check:** A per σ-twin and revision twin after the continued wake; C; B kept after wake (continuation must not give B's progress back).

#### 4. Answer-flip count along the wake path (improvement)

- **Mechanism:** Record A's argmax answers on public inputs after each inner step of `W`. A correct wake moves answers monotonically toward one pattern; a wake caught between two attractors flips some answers twice or more. The flip count is a cheap path statistic that needs no labels.
- **Nearest art / delta:** Prediction churn and forgetting-event counts (Toneva et al.) count flips over training; here flips are counted inside a repair operator to detect attractor competition.
- **Cheapest first test:** AUROC of the flip count for wrong-after-wake, compared with final displacement and card 1, on held-out histories. Report it per failure type; expect it to catch stale and mixture outcomes and miss σ-flips.
- **Old-task retention check:** No extra intervention; report C and B alongside each scored wake.

#### 5. Independent-wake intersection (primitive)

- **Mechanism:** Freeze two wakes `W_1`, `W_2` on disjoint public sources and different update rules (for example SGD on text-like inputs versus a feature-alignment objective on random inputs). The true skill should be a fixed point of both; a spurious fixed point of one is unlikely to be a fixed point of the other unless the failure is shared. Accept a wake only if `W_2(W_1(θ)) ≈ W_1(θ)` on A outputs.
- **Nearest art / delta:** Co-training and multi-view agreement (Blum & Mitchell 1998) agree on labels; [IGN](https://arxiv.org/abs/2311.01462) uses idempotence of one map. Intersecting the fixed sets of two independent weight-space repairs is new. Key weakness, stated up front: collapse to a constant and σ-flips are shared fixed points of every public wake, so diversity must be shown on development hosts.
- **Cheapest first test:** Compare intersection acceptance with single-wake idempotence at equal total steps, per failure type. Report the measured overlap of `Fix(W_1)` and `Fix(W_2)` on development hosts.
- **Old-task retention check:** A after the accepted wake, C, and B after both wakes (two wakes must not cost twice the B loss).

#### 6. Response fingerprint at burial (primitive)

- **Mechanism:** When A is learned (before any lease), store a few bytes of **label-free** linear-response statistics at the awake fixed point: the top eigenvalues of `J_W`, the singular values of the A-input Jacobian of the hidden layer, the spectrum of public-output covariance. After the wake, compare. Wrong fixed points of the same symmetry class can share outputs but usually not the local response geometry; stale fixed points carry the response of an older, longer-trained state.
- **Nearest art / delta:** Basin-geometry signatures detect memorization in diffusion models ([2610.11670](https://arxiv.org/abs/2610.11670)); linearized response is used to match twins in PR #136 / [2608.19762](https://arxiv.org/abs/2608.19762). Here the fingerprint is a charged, label-free certificate of which fixed point the wake reached.
- **Cheapest first test:** Fingerprint sizes {16, 64, 256} bytes. Compare detection AUROC and post-wake A (wake, check, else retry with a different public batch) against an equal-byte replay buffer and an equal-byte saved delta. Prediction: σ-flips are invisible (the fingerprint is σ-invariant), stale revivals are visible.
- **Old-task retention check:** A per failure type after accepted wakes, C, B.

#### 7. Partition invariance on A inputs (improvement; audit)

- **Mechanism:** Before the lease, record (charged, few bytes as a hash) the partition of a fixed set of unlabeled A-like inputs induced by the host's hidden clustering. After `W`, require the same partition up to relabeling. This catches collapse, mixtures and B absorption, and provably misses σ-flips, which preserve the partition. It is the right **floor** detector for every other card.
- **Nearest art / delta:** Cluster-consistency checks in source-free adaptation; PR #126's label-free detection node. The new part is using it as a strict lower bound that separates "the wake kept A's distinction" from "the wake kept A's answers".
- **Cheapest first test:** Run it alongside cards 1, 4, 6 on the same histories; it should match them on collapse and lose to them on stale outcomes.
- **Old-task retention check:** As in card 1.

### B. Stale answers: when the wake revives a retired version

#### 8. Basin-depth race between versions (primitive; audit)

- **Mechanism:** Train `A_v1` for `T_1` steps, revise to `A_v2` for `T_2` steps (changing the answer on a known subset), then lease and wake. Hypothesis: the probability that `W` revives `A_v1` on changed inputs grows with `T_1/T_2`, because energy-seeking wakes go to the deeper basin. This is a direct test of root-cause point 3.
- **Nearest art / delta:** Benign relearning and relearning attacks ([2406.13356](https://arxiv.org/abs/2406.13356), [2605.11685](https://arxiv.org/abs/2605.11685)), the forget–retain alignment gap ([2608.25429](https://arxiv.org/abs/2608.25429)) and binding-specific relearning savings ([2610.22381](https://arxiv.org/abs/2610.22381)) measure revival of deleted or weakened knowledge under fine-tuning. None measures a **wake operator's** choice between two versions of the same skill as a function of version age.
- **Cheapest first test:** Grid `T_1/T_2 ∈ {1/4, 1, 4, 16}` × 8 seeds. Ledger margin rule: match `A_v2` margin before the lease across grid points, else the effect is margin, not depth. Report stale fraction versus `T_1/T_2` with seed CIs.
- **Old-task retention check:** `A_v2` on unchanged inputs (must stay correct), C, B.

#### 9. Proximal wake (primitive)

- **Mechanism:** Replace plain descent with a proximal continuation: each inner step minimizes the public wake objective plus `‖θ − θ_lease-end‖²/2τ` with `τ` frozen on development. The wake then reaches the fixed point **nearest** the lease-end state, which satisfies P3. Recency is protected because the revised `A_v2` basin is the one B displaced the host from.
- **Nearest art / delta:** Proximal point methods and trust-region continuations are standard; L2-SP and EWC anchor to the pre-task state during training. Anchoring the **repair** to the lease-end state (not to a stored old checkpoint) is the new use, and it costs no stored bytes.
- **Cheapest first test:** On card 8's grid, compare proximal wakes at three `τ` with plain `W` and with an L2-SP anchor to the pre-lease state (which needs stored weights and is charged). Claim dies if proximal wakes lower the stale fraction only by also lowering correct recovery.
- **Old-task retention check:** `A_v2` correct and `A_v1` absent on changed inputs, C, B after wake.

#### 10. Voronoi lease radius (primitive)

- **Mechanism:** With a proximal wake (card 9), correctness has a clean geometric condition: the wake is correct if the lease-end state lies closer (in the wake's metric) to the `A_v2` fixed point than to any other. Estimate on development hosts the distance `d(A_v1*, A_v2*)` between the two version fixed points and cap the lease displacement at `d/2`. This turns parent card 3's empirical radius into a recency-safe radius.
- **Nearest art / delta:** Parent card 3 (basin radius) and card 11 (Banach contraction) ignore competing versions. Voronoi cells of attractors are standard in dynamical systems; using the version-to-version distance as a write budget is new.
- **Cheapest first test:** Sweep lease radius multipliers {0.25, 0.5, 1, 2}·`d/2` with proximal and plain wakes; the prediction is a stale-revival knee near 1 for the proximal wake and none (or an earlier one) for plain `W`.
- **Old-task retention check:** As in card 9, per multiplier.

#### 11. Revision-twin certification of the wake (improvement)

- **Mechanism:** Certify a frozen `W` on development revision twins: hosts that learned `A_v1→A_v2` and hosts that learned only `A_v2`, at equal total steps and matched `A_v2` margin. `W` passes only if it produces the same `A_v2` answers on both after identical leases. This is BCE4's admission rule made into a certificate class, the stale-answer analogue of parent card 17's σ-twin certificate.
- **Nearest art / delta:** BCE4 (round 29) proposes the scoring; PR #139 card 10 is the A-naive control. The delta is using revision twins as a transferable licence for leases and reporting how it fails on held-out rule generators.
- **Cheapest first test:** Freeze certification on development rule generators; test on held-out generators. Compare leases licensed by the certificate with unlicensed leases and with an oracle that sees live `A_v2` labels.
- **Old-task retention check:** `A_v2` per twin, `A_v1` absence, C, B.

#### 12. Era-cue sensitivity of the reached fixed point (primitive)

- **Mechanism:** Public data often carries era cues (formats, vocabulary, distribution of a period). A stale fixed point is more sensitive to old-era public inputs than a current one. After the wake, apply one extra public step on old-era-shaded versus new-era-shaded public batches (both unlabeled) and compare how far A outputs move. Asymmetric sensitivity flags a stale basin.
- **Nearest art / delta:** Syntax as the driver of benign relearning ([2602.03379](https://arxiv.org/abs/2602.03379)) shows public structure revives old content; this turns that sensitivity into a detector. Requires an era signal, so it is only valid where the public stream has one (stated scope).
- **Cheapest first test:** Toy: `A_v1` and `A_v2` trained with distinct input-style mixtures; measure detection AUROC for stale outcomes against cards 4 and 6 at equal cost. Control: hosts that never learned `A_v1` must show no asymmetry.
- **Old-task retention check:** The probe step runs on a fork; report live A, C, B.

#### 13. Retirement scar: write the revision so stale basins are shallow (primitive)

- **Mechanism:** When A is revised, do not only train `A_v2`; also run a short "daydreaming" phase that suppresses the `A_v1` attractor under the frozen `W` (run `W` from states near `A_v1*` and push those end states toward `A_v2` using the revision data that is available at revision time). Future wakes then have no stale basin to fall into.
- **Nearest art / delta:** The Daydreaming algorithm reinforces stored patterns while suppressing spurious attractors in Hopfield networks ([2604.19258](https://arxiv.org/abs/2604.19258)); relearning-robust unlearning targets revival under fine-tuning ([2605.11685](https://arxiv.org/abs/2605.11685), [2610.31075](https://arxiv.org/abs/2610.31075)). Here the suppression is **of a wake operator's** stale fixed point at revision time, not of a forget set under arbitrary fine-tuning.
- **Cheapest first test:** On card 8's grid, compare scarred revisions with plain revisions and with relearning-robust unlearning of `A_v1` at equal revision steps; score stale fraction after lease and wake.
- **Old-task retention check:** `A_v2` and unchanged A inputs right after revision (the scar must not damage them), C, and B after the later lease.

### C. Wake dynamics with a checkable "only the true skill" guarantee

#### 14. Payload-frozen, access-contracting wake (primitive)

- **Mechanism:** Implement P1 and P2 directly: `W` updates only access coordinates (the parent card 2 split, frozen on development), and its public objective is strictly convex in those coordinates given the payload (for example least-squares realignment of a readout or interface map against public consistency targets). Then for each payload there is one access completion, and the wake is correct exactly when the payload survived.
- **Nearest art / delta:** Transport keys ([2606.02860](https://arxiv.org/abs/2606.02860)) realign interfaces from stored paired anchors; spurious-forgetting repair ([2610.08718](https://arxiv.org/abs/2610.08718)) removes one shift direction. This builds the uniqueness into the wake's write set, with no stored key.
- **Cheapest first test:** Compare with plain `W` and parent card 9's retraction-trained wake on the full taxonomy. Two kill conditions: the access/payload split mislabels payload as access (then flips appear), or the restricted wake recovers less A than plain `W` at equal steps.
- **Old-task retention check:** A per σ-twin and revision twin, payload decodability from hidden features (to check the payload truly survived), C, B.

#### 15. Interval-Newton uniqueness certificate (primitive)

- **Mechanism:** For the restricted wake of card 14 in a small MLP, apply the Krawczyk operator (interval Newton) to `a ↦ a − W_a(p, a)` on a box around the post-wake access state. If the operator maps the box into its interior, the box provably contains exactly one fixed point. Combined with P1, this is a computer-assisted proof that the wake settled on the only completion of the surviving payload.
- **Nearest art / delta:** Krawczyk's operator and interval analysis (Moore) are classical; interval bound propagation certifies input robustness. Parent card 11 bounds Lipschitz constants for a basin radius; this proves **uniqueness**, which is what excludes wrong fixed points of the same payload. Scope: tiny hosts and access layers only; LLM scale is a moonshot.
- **Cheapest first test:** Width-16 and width-64 access layers; report certificate success rate and box size versus the empirical uniqueness from card 1's census. The claim dies if certificates succeed only on boxes too small to contain the lease-end state.
- **Old-task retention check:** A, C and B on certified versus uncertified wakes; certified wakes must have near-zero wrong outcomes on held-out histories.

#### 16. σ-equivariant wakes that preserve payload sign (primitive)

- **Mechanism:** Train or constrain `W` so that it is exactly σ-equivariant (`W(σθ) = σW(θ)`, achievable by symmetrizing the public batch and update rule) and so that its flow never crosses the payload sign boundary (a barrier term on `|p|`). By root-cause point 1 an equivariant wake cannot create a flip on its own; the barrier stops it from following one created by B. Flips then come only from payload loss, which card 7's floor detector catches.
- **Nearest art / delta:** Equivariant networks enforce symmetry on inputs; control barrier functions certify forward invariance ([Ames et al. 2019](https://arxiv.org/abs/1903.11199)), as cited by the parent. Here the symmetry is a **label symmetry of a weight-space repair**, and the barrier protects the payload sign.
- **Cheapest first test:** Compare with plain `W` on σ-twins: report flip rate after wake per lease radius. Control: a non-equivariant wake with the same barrier, and an equivariant wake without it.
- **Old-task retention check:** A per twin, C, B; payload sign before and after the lease (the barrier must not freeze B out of the leased directions).

#### 17. Monotone wakes with ordered fixed points (primitive; moonshot-leaning)

- **Mechanism:** If `W` is a monotone (order-preserving) map in suitable coordinates, its fixed points are ordered, and starting above the payload threshold converges to the greatest fixed point below the start (Hirsch / Tarski-style arguments). Choose coordinates where A's correct answer corresponds to "payload above threshold" and constrain `W` (non-negative interaction Jacobian, cooperative dynamics) so the order holds. Then wrong fixed points can only be reached from states that already lost the payload.
- **Nearest art / delta:** Monotone dynamical systems theory is classical; monotone networks exist for interpretability. Using cooperativity of a repair operator to order its fixed points by correctness is new.
- **Cheapest first test:** Two-skill toy where cooperativity can be enforced exactly; measure whether the ordered-fixed-point guarantee holds empirically under leases and how much B capacity the monotonicity constraint costs versus plain `W` and GPM.
- **Old-task retention check:** A, the second skill and B on the same post-wake copy.

#### 18. Abstaining wake (improvement)

- **Mechanism:** Combine the census (card 1), the bifurcation alarm (card 2) and the fingerprint (card 6) into a frozen rule: the wake either returns a state or abstains and requests a small labelled refresh, whose labels are charged. Score risk–coverage: wrong-answer rate on accepted wakes versus abstention rate.
- **Nearest art / delta:** Selective classification ([Geifman & El-Yaniv 2017](https://arxiv.org/abs/1705.08500)) abstains per input; this abstains per **wake**, at the skill level, and charges the fallback labels so the comparison with replay is fair.
- **Cheapest first test:** Risk–coverage curves against "always wake", "always request labels" and DER++ given the same label budget.
- **Old-task retention check:** A, C, B per coverage level, including hosts where the wake abstained and the refresh ran.

### D. Breaking the symmetry: anchors and bits

#### 19. Minimum anchor bits for uniqueness (primitive; audit)

- **Mechanism:** By root-cause point 1, a pure σ-flip is invisible without symmetry-breaking information, but only `log2 |G|` bits break a symmetry group `G` (one bit for polarity). Store at A's learning time the sign of A's output on a handful of public inputs (charged), and let `W` minimize its objective subject to agreeing with those signs. Measure the bits needed to make the correct fixed point unique versus the bits replay needs for the same post-wake A.
- **Nearest art / delta:** Equal-bit replay is the direct control; PR #139's carrier hitting sets and parent card 5 (collateral) store state, not symmetry-breaking bits. The claim "uniqueness costs `log |G|` bits while retention costs many more" is the new, falsifiable statement.
- **Cheapest first test:** Bits {1, 4, 16, 64} with anchored `W` versus replay of the same number of labelled A examples (16 labels ≈ 16 bits for binary A). The card dies if equal-bit replay ties at every size.
- **Old-task retention check:** A per σ-twin after anchored wake, C, B; anchored inputs excluded from scoring.

#### 20. Cross-skill anchors from co-resident C (primitive)

- **Mechanism:** If C's answers are tied to A's by a declared relation on some inputs (for example C reads A's output as a feature, or A and C share a readout), then C, which is not leased, breaks A's σ symmetry for free. Add C-consistency to the wake's objective and choose which tasks share structure so that every leased skill has a live anchor.
- **Nearest art / delta:** The ledger killed composition contracts as training ("composing atomic outputs labels hybrids for free, so it is SFT on generated labels"). Here the relation is used only to **select among fixed points of a wake**, not to train A, so the SFT equivalence does not apply; the strongest control is still SFT of A on C-generated labels at equal steps, which must be beaten.
- **Cheapest first test:** Host with A and C sharing a readout; compare C-anchored `W` with plain `W` and with SFT on C-derived A labels at equal steps, on σ-twins.
- **Old-task retention check:** C must not be distorted by being used as an anchor (C before and after wake), A per twin, B.

#### 21. B as an anchor: wake inside B's own constraint (improvement)

- **Mechanism:** One wrong outcome is A absorbed into B. Require the wake's fixed point to keep B's outputs on B inputs within a band (B is live and its data is available), which removes B-absorbed fixed points from `Fix(W)` and narrows the remaining ambiguity to A's own symmetry.
- **Nearest art / delta:** Parent card 6 keeps B's gain inside the post-wake image; here B's constraint is used to **prune** wrong A fixed points, measured per failure type.
- **Cheapest first test:** Compare B-constrained `W` with plain `W` on the absorbed-into-B rate and on the other failure types; control: a B replay term of equal weight without the constraint form.
- **Old-task retention check:** A per failure type, C, B after wake.

### E. Cost and audits

#### 22. Wrong-fixed-point census of the parent's lease designs (audit)

- **Mechanism:** Run the full taxonomy (correct, flip, collapse, mixture, absorbed, stale) on every lease variant the parent proposes (cards 1, 2, 3, 8, 13) with plain `W`. This produces the base rates that decide whether the detectors and dynamics above are needed at all.
- **Nearest art / delta:** Parent card 10 searches adversarially for wrong fixed points; this measures how often ordinary leases produce them, per type.
- **Cheapest first test:** 16 histories × 5 lease variants × σ-twins and revision twins; report per-type rates with seed CIs. If wrong outcomes are below seed noise at useful radii, cards 1–7 become cost savers only and the node's main question is answered "rare".
- **Old-task retention check:** This card is the retention audit; include C and B.

#### 23. Break-even: provable wake versus saved delta (audit)

- **Mechanism:** The guarantees above cost something: restricted write sets (cards 14, 16, 17), certificates (card 15), anchors (cards 19, 20), census forks (card 1). Sum them in bytes, steps and latency and find the region, if any, where a provably correct wake plus lease beats release plus an equal-byte saved delta and GPM at matched post-wake A/C floors.
- **Nearest art / delta:** Parent card 20 does this for leases with plain `W`; this card adds the price of correctness.
- **Cheapest first test:** Same sweep as parent card 20, with each correctness mechanism added in turn.
- **Old-task retention check:** A after restore versus after the certified wake, C, B.

## Ranked deeper questions

1. **How often do ordinary leases end in a wrong or stale fixed point, by type?** Cards 22, 8 and 7. Without base rates, everything else is a solution in search of a problem. The sharpest sub-question is whether stale revival tracks version age at matched margin (card 8), which would make recency, not idempotence, the property a safe wake needs.
2. **Is there a label-free signal that catches wrong fixed points beyond collapse?** Cards 1, 2, 4 and 6 against an output-marginal anti-collapse check and equal-bit replay. Root-cause point 1 predicts every label-free detector is blind to pure σ-flips; the question is whether it catches stale, mixture and absorbed outcomes well enough to license leases, and whether the bifurcation alarm warns before the failure exists in outputs.
3. **Can a wake be built whose fixed point is provably the only completion of the surviving payload, at a cost that still beats a saved delta?** Cards 14, 15, 16 and 23. Payload invariance plus unique access completion (checked by an interval-Newton certificate on small hosts) is the cleanest "only the true skill" guarantee available; it fails if the access/payload split is unreliable or if restricting the wake costs more than storing the delta.
4. **How few stored bits make the correct fixed point unique, compared with the bits replay needs?** Cards 19 and 20. If one to a few anchor bits (or a live co-resident skill) remove σ-ambiguity while replay needs many more labels for the same post-wake A, symmetry breaking is a cheap new primitive; if equal-bit replay ties, it is not.
5. **Do proximal wakes and retirement scars stop stale revival without stopping recovery?** Cards 9, 10 and 13. Depth-seeking wakes should prefer old, deep versions; proximal wakes should prefer the current one within a Voronoi radius. A clean knee at `d/2` for proximal but not plain wakes would be a concrete, testable law for recency-safe leases.
