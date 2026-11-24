# Joint branch moves and rebase-preserving merge ranges

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Certified merge-weight ranges](merge-weight-ranges.md) ([PR #189](https://github.com/manojbajaj95/cl/pull/189)), cards 16 and 8. **Review seed:** [Flood triage row 296](https://github.com/manojbajaj95/cl/blob/bb41bb097fde79c9222c6de7f0dc417e79f8f412/reviews/flood-triage.md#L296), the two score-3 directions: prove a joint endpoint reached by safe paired moves or one atomic paired commit that frees merge-range headroom no single-branch move reaches; carry a certified merge range across a change of base via a verified map from promised coefficients to their new implementation, refusing rank-deficient changes that alias distinct choices. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/bb41bb097fde79c9222c6de7f0dc417e79f8f412/reviews/idea-ledger.md). Coded merge interference was killed against equal-budget direct search; read-pinning adapter ABIs were killed because pinning insertion activations pushes drift into downstream layers; forecast-weighted write selection died after retention matching; save/restore return points are exact by construction.

## Are paired range-freeing moves and choice-preserving rebases continual-learning primitives?

**Not as joint alignment, two-phase commit, or single-checkpoint task-vector transport.** [Git Re-Basin](https://arxiv.org/abs/2209.04836), [model soups](https://arxiv.org/abs/2203.05482), [linear mode connectivity](https://arxiv.org/abs/1912.05671), [task arithmetic](https://arxiv.org/abs/2212.04089), [TIES](https://arxiv.org/abs/2306.01708), [tangent-space task arithmetic](https://arxiv.org/abs/2305.12827) and [proximity-regularized merging](https://arxiv.org/abs/2609.32332) already align representations or smooth merge sensitivity. [Trans-LoRA](https://arxiv.org/abs/2405.17258), [Cross-LoRA](https://arxiv.org/abs/2508.05232), [fine-tuning transfer](https://arxiv.org/abs/2503.20110), [THESEUS](https://arxiv.org/abs/2602.12952), [ARIADNE](https://arxiv.org/abs/2610.32581), [gradient-sign transport](https://arxiv.org/abs/2510.09658) and [MUSCLE](https://arxiv.org/abs/2407.09435) already move one adapter or checkpoint across base versions. [Pacti](https://arxiv.org/abs/2303.17751), [CROWN](https://arxiv.org/abs/1811.00866), [Certified CL](https://arxiv.org/abs/2407.06697) and two-phase commit already handle assume-guarantee contracts, sound bounds and atomic publication.

**Conditional candidates:**
1. **Cooperative range-freeing moves:** certify both a joint endpoint $(d_1', d_2')$ in the product of solo-equivalent fibers $F_1 \times F_2$ and its execution mode (an escrowed safe serial route or an atomic paired commit) that strictly expands a certified late-choice range $S_0 \subsetneq S_1$ behind an **all-single-moves barrier**, without letting either branch unilaterally claim or spend the freed headroom.
2. **Choice-preserving rebase morphisms:** carry an entire certified family of late deployment choices $S$ across a base change $x_0 \to x_1$ via a verified map $\phi: S \to \mathcal{W}(x_1)$ that preserves both A/C retention (including declared post-merge suffixes) and **injectivity on the B-distinguishing readout**, emitting an explicit aliasing witness whenever $x_0 \to x_1$ is rank-deficient on choice-bearing or protected directions.

If independent projection, coordinate descent, joint Re-Basin alignment, task-arithmetic re-extraction or exact recertification from $x_1$ tie at matched information, solo scores, B utility and total proof cost, then both directions collapse to certified merging plus standard alignment and transactions.

### What must be proved, and what fails silently?

- **Separate deadlock from missed local moves.** A paired move only earns coordination credit when every legal single-branch move in $F_1$ or $F_2$ either violates A/C on $S_0$ or yields zero range expansion. Always distinguish (a) **atomic-only barriers**, where every axis-aligned half-step breaks $S_0$, from (b) **escrowed serial routes**, where branch 1's first move stays safe on $S_0$ with zero immediate gain and only pays off once branch 2 completes step 2.
- **Keep co-owned headroom from leaking.** When a paired move unlocks $\Delta S = S_1 \setminus S_0$, neither branch caused $\Delta S$ alone. Crediting $\Delta S$ to branch 1's local drift budget lets an uncoordinated B update immediately re-lock branch 2 or break A/C on $S_1$. Newly freed headroom stays jointly owned until explicitly partitioned back into product-valid local envelopes.
- **Refuse choice-aliasing rebases even when A/C loss drops.** A rank-deficient base projection $T$ can *reduce* old-task squared error by averaging coordinates while collapsing two distinct promised choices $(u_1, v_1) \neq (u_2, v_2) \in S$ onto the same merged output. A rebase certificate must therefore check *two* properties: A/C floors over $\phi(S)$ (and declared suffixes) **and** a quantitative separation floor on the B-distinguishing readout across distinct choices in $S$.
- **Preserve the evaluation contract.** Match solo weighted A/C curves, B utility, old-task access and total coordination/proof bytes across all arms. Report late B utility regret against exact feasible selection, certified set inclusion ($S_0 \subsetneq S_1$, not just area), blocked single moves, synchronization stalls, refusal precision/recall on rank-deficient rebases, and worst-prefix A/C retention on both declared slices and held-out old examples the certifier never sees.

### Two paper witnesses, not results

1. **An all-single-moves barrier with both atomic and escrowed-serial regimes.** Let each branch delta carry an untouched B-utility coordinate plus two 3D residual vectors $(p_A, p_C)$ and $(q_A, q_C)$ of fixed norm $1/5$ for protected old slices $A$ and $C$, with squared-error losses $L_A(u,v) = \|u p_A + v q_A\|_2^2$ and $L_C(u,v) = \|u p_C + v q_C\|_2^2$ on $u, v \in [0,1]$, under caps $L_A \le 3/25$ and $L_C \le 2/25$. Every state in $F_1 = \{p^{(0)} = \frac{1}{5}(e_1, e_2),\; p^{(1)} = \frac{1}{5}(e_2, e_3)\}$ and $F_2 = \{q^{(0)} = \frac{1}{5}(e_1, e_3),\; q^{(1)} = \frac{1}{5}(e_3, e_2)\}$ has **identical** weighted solo curves $L_A(u,0) = L_C(u,0) = u^2/25$ and $L_A(0,v) = L_C(0,v) = v^2/25$ for all $u,v \in [0,1]$.
   - At the start $(p^{(0)}, q^{(0)})$, $p_A \cdot q_A = 1/25$ and $p_C \cdot q_C = 0$, so $L_C \le 2/25$ holds on all of $[0,1]^2$ while $L_A = (u+v)^2/25 \le 3/25$ restricts the certified range to $S_0 = \{u+v \le \sqrt{3}\}$ (excluding $(1,1)$).
   - **Atomic-only regime:** moving branch 1 alone to $(p^{(1)}, q^{(0)})$ gives $p_A \cdot q_A = 0$ but $p_C \cdot q_C = 1/25$, breaking $L_C \le 2/25$ on $u+v \in (\sqrt{2}, \sqrt{3}] \subset S_0$. Moving branch 2 alone to $(p^{(0)}, q^{(1)})$ likewise gives $p_C \cdot q_C = 1/25$ and breaks $S_0$. Yet the **paired move** $(p^{(1)}, q^{(1)})$ has $p_A \cdot q_A = 0$ and $p_C \cdot q_C = 0$, certifying the full square $S_1 = [0,1]^2$ with both losses $\le 2/25$. No safe serial route exists; only an atomic paired commit crosses the barrier.
   - **Escrowed-serial regime:** add a fourth coordinate $e_4$ and one intermediate state $p^{(\text{mid})} = \frac{1}{5}(e_1, e_4)$ to $F_1$. Branch 1 moving $p^{(0)} \to p^{(\text{mid})}$ keeps $p_A \cdot q_A = 1/25$ and $p_C \cdot q_C = 0$: it stays safe on $S_0$ with **zero immediate expansion** (greedy coordinate descent rejects it), and unlocks branch 2's step $q^{(0)} \to q^{(1)}$, which immediately achieves $p_A \cdot q_A = p_C \cdot q_C = 0$ and certifies $[0,1]^2$.
2. **A rebase map that passes on a signed basis change and refuses a rank-deficient projection.** Take a linear host with certified range $S = [0,1]^2$ on base $x_0$, where late B preference $\beta_1$ rewards $(1,0)$ (high coordinate 1) and $\beta_2$ rewards $(0,1)$ (high coordinate 2), while old slice $C$ reads the difference coordinate $z_1 - z_2$.
   - **Positive rebase (full-rank non-orthogonal basis change):** $x_1 = T x_0$ with $T = \mathrm{diag}(2, -1/2, 1)$. Naive coefficient reuse $(u,v)$ without remapping distorts the merge path, whereas the verified coefficient map $\phi$ reproduces every merge output on $S$ and preserves both $\beta_1/\beta_2$ separation and $A/C$ floors. Adding a two-step diagonal-Adam suffix exposes a second failure mode: non-orthogonal $T$ rescales coordinate step sizes, so immediate-output equivalence passes while the suffix fails unless optimizer slots are transported or the suffix tube is re-proved.
   - **Negative rebase (rank-deficient projection):** $T_{\text{bad}}(z_1, z_2, z_3) = (\frac{z_1+z_2}{2}, \frac{z_1+z_2}{2}, z_3)$ projects out $z_1 - z_2$. Every $(u,v) \in S$ with the same sum $u+v$ collapses to one merged output, and squared error on $A$ can even decrease. An A/C-only checker falsely accepts; a choice-preserving certifier refuses and returns the explicit aliasing witness $(1,0) \neq (0,1)$ plus the erased $C$ direction.

## Idea cards

**P** denotes a candidate primitive, not a priority claim. **I** denotes an improvement, control, or audit. All first tests below are CPU-sized proposals, not runs.

### Paired moves when single-branch repair is trapped

#### 1. Certify an all-single-moves obstruction before paying for a paired move (P)
- **Mechanism:** Before initiating inter-branch synchronization, emit a compact obstruction certificate proving that every solo-equivalent move in $F_1$ or $F_2$ either violates A/C on $S_0$ or cannot expand $S_0$; trigger a paired commit only when that obstruction holds.
- **Novelty vs nearest prior art:** Coordinate descent and branch-and-bound detect local minima empirically, and Pacti checks contract feasibility. The candidate object is a reusable *deadlock witness* over solo-equivalent fibers that separates genuine cooperative headroom from unexploited single-branch slack.
- **Cheapest first test:** Mix 20 instances of Paper Witness 1 (half with a hidden single-branch escape, half with a true barrier); compare always-pair, greedy coordinate descent, exact joint recertification and obstruction-gated pairing at matched total queries and messages.
- **Old-task retention check:** Verify A/C on $S_0$ and $S_1$, all visible single steps and a shared B suffix; verify no false obstruction causes an unsafe local move or skips a valid single-branch repair.

#### 2. Escrowed serial handshakes with zero-gain first steps (P)
- **Mechanism:** Certify a two-step (or $k$-step) in-place serial route where branch 1 publishes a locally unproductive equivalent move $p^{(0)} \to p^{(\text{mid})}$ that preserves $S_0$ only against a bound obligation for branch 2 to execute step 2 and unlock $S_1 \supsetneq S_0$.
- **Novelty vs nearest prior art:** Two-phase commit hides intermediate states until atomic cutover, and coordinate descent requires monotone per-step gain. The candidate operation is a *live, non-monotone serial handshake* that avoids atomic locking while escaping greedy local traps.
- **Cheapest first test:** Run the escrowed-serial regime of Paper Witness 1 against greedy coordinate descent, independent projection, atomic paired commit and exact multi-step search; measure unlocked range, synchronization stall time and message bits.
- **Old-task retention check:** Check A/C on $S_0$ at the live intermediate pair $(p^{(\text{mid})}, q^{(0)})$, on $S_1$ after step 2, and through a shared suffix; also inject a delayed step 2 to confirm the intermediate state remains safe for deployment.

#### 3. Co-owned headroom ledgers that block unilateral spend (P)
- **Mechanism:** Record headroom $\Delta S = S_1 \setminus S_0$ freed by a paired move as a *jointly signed* right that neither branch may consume with an independent B update until an explicit partitioning step splits $\Delta S$ into product-valid local drift envelopes.
- **Novelty vs nearest prior art:** Assume-guarantee contracts (Pacti) and merge-aware budgets (#181) allocate local slack after a static split. The candidate object is a *co-owned capacity right* whose ownership matches the cooperative move that created it.
- **Cheapest first test:** After unlocking $[0,1]^2$ in Paper Witness 1, allow both branches to propose one further B update; compare crediting $\Delta S$ to branch 1, naive 50/50 heuristic splitting, exact joint recertification and co-owned ledger partitioning at matched B progress.
- **Old-task retention check:** Audit every pair of post-repair local B updates on A/C across all of $S_1$ and a shared suffix; count any unilateral spend that breaks a corner of $S_1$ as a retention failure.

#### 4. Abort-safe make-before-break paired commits (I)
- **Mechanism:** Structure paired handshakes so that if either branch aborts mid-protocol (crash, timeout or an urgent conflicting B batch), any already-published half remains certified on the old range $S_0$ without checkpoint rollback.
- **Novelty vs nearest prior art:** Transactional make-before-break and two-phase commit already guarantee abort safety; this audits which paired routes survive partial failure without relying on the ledger's killed save/restore return-point stack.
- **Cheapest first test:** Inject single-branch aborts after step 1 in both regimes of Paper Witness 1; compare atomic-only rollback, unguarded serial moves and make-before-break serial routes on recovery cost and availability.
- **Old-task retention check:** Score A/C on $S_0$ on the aborted half-published state and on subsequent B updates from that state; confirm zero drop below $S_0$ floors without reverting weights.

#### 5. Partial-subspace paired gauge exchanges (P)
- **Mechanism:** Execute a simultaneous symmetry transform (hidden-unit swap or signed orthogonal rotation) restricted to the free subspace orthogonal to a base-anchored old slice $C$, leaving both solo functions and $C$'s base anchor intact while canceling cross-branch interference on $A$.
- **Novelty vs nearest prior art:** Git Re-Basin aligns full layers across models without protecting a base-anchored third slice, and single-branch permutation misaligns the partner. The candidate operation is a *constrained paired gauge move* that preserves an asymmetric base anchor.
- **Cheapest first test:** Use a 3-unit ReLU host where unit 3 anchors old slice $C$ to $x_0$ while units 1–2 are misaligned relative to $x_0$ on both branches; compare full Re-Basin, single-branch swap, independent projection and partial-subspace paired swap.
- **Old-task retention check:** Verify exact solo function equality on all inputs, $A$ and $C$ across $S_1$, and a held-out old slice reading unit 3; verify full Re-Basin breaks $C$ while single-branch swap breaks $A$.

#### 6. Sketch-only paired move negotiation under private branches (P)
- **Mechanism:** Certify a paired endpoint $(d_1', d_2')$ and its expanded range $S_1$ by exchanging only a bounded bilinear interaction sketch (projections onto a shared A/C sensitivity frame), refusing whenever two private branch states share the sketch but disagree on $S_1$.
- **Novelty vs nearest prior art:** Joint alignment and exact joint recertification require full weights or shared data. The candidate operation is *privacy-preserving cooperative certification* with an explicit soundness check against sketch aliasing.
- **Cheapest first test:** Run Paper Witness 1 with private B coordinates and 2-bit vs exact A/C frame sketches, plus an adversarial pair with identical low-bit sketches and opposite $C$ signs; compare full-weight sharing, blind local repair and sketch-negotiated pairing at matched message bytes.
- **Old-task retention check:** Test A/C across all surviving private states consistent with the sketch on $S_0$, $S_1$ and the shared suffix; reject any paired commit whose sketch admits an unsafe counter-pair.

#### 7. Paired optimizer-slot realignment for suffix-only headroom (P)
- **Mechanism:** Hold both branches' immediate weights and merge outputs fixed while executing a paired move in their optimizer states (co-rotating or co-scaling momentum and second-moment buffers) so the post-merge shared suffix tube stays inside A/C caps over a strictly larger $S_1$.
- **Novelty vs nearest prior art:** Weight-space alignment ignores optimizer geometry, and single-branch slot resets discard useful curvature. The candidate operation is a *function-silent paired state move* whose range gain appears only after shared post-merge training.
- **Cheapest first test:** Construct a two-step quantized momentum recurrence where immediate weights certify $[0,1]^2$ on $A$ but opposite-signed branch moments push the merged suffix across an $A$ gate at $(1,1)$; compare partial slot reset, single-branch moment damping, exact joint search and paired moment realignment.
- **Old-task retention check:** Match immediate solo and merged outputs exactly, then verify A/C at every suffix step across $S_1$ and confirm B learning speed in the suffix does not collapse.

#### 8. Minimal-coalition cyclic moves for three or more branches (I)
- **Mechanism:** When three branches share pairwise certified ranges and no pair can unlock $S_1$ without breaking a third branch's range, certify a minimal 3-way cyclic move and prove no 2-branch move suffices.
- **Novelty vs nearest prior art:** Multi-party atomic commits and coalition search already handle $k$-way coordination; this audits whether paired moves suffice in multi-branch fleets or hide 3-way deadlocks.
- **Cheapest first test:** Extend Paper Witness 1 to three branches $(d_1, d_2, d_3)$ with a cyclic conflict across slices $(A, C_1, C_2)$ where every 2-branch move breaks one slice and only the 3-way rotation unlocks $[0,1]^3$; compare pairwise-only pairing, 3-way cyclic commit and exact joint recertification.
- **Old-task retention check:** Check $A, C_1, C_2$ on all pairwise faces and the 3-way interior across the unlocked region and shared suffix; confirm every 2-branch subset fails the declared floors.

#### 9. Separate atomic-swap barriers from discrete-grid artifacts (I)
- **Mechanism:** Audit any claimed all-single-moves barrier by refining the allowed solo-equivalent fiber from discrete permutations to continuous score-equivalent paths; authorize an atomic paired commit only when the barrier persists under the real continuous move set.
- **Novelty vs nearest prior art:** Mode connectivity already showed that discrete barriers can vanish along continuous curves; this prevents quantized toy witnesses from manufacturing artificial demand for atomic commits.
- **Cheapest first test:** Embed Paper Witness 1's discrete states in continuous $SO(3)$ rotations of $(p_A, p_C)$ vs a disconnected permutation fiber (two hidden units with opposite signs); compare continuous single-branch path search against atomic paired commit.
- **Old-task retention check:** Verify A/C along every point of any claimed continuous single-branch path (not just endpoints) on $S_0$ and $S_1$, plus a held-out directional old reader.

#### 10. Paired moves under asymmetric branch staleness (I)
- **Mechanism:** Certify a paired endpoint when branch 1 has admitted one B update ahead of the checkpoint branch 2 holds, binding the paired commit to a fenced version pair rather than freezing both branches to lockstep before coordinating.
- **Novelty vs nearest prior art:** Bounded-staleness synchronization and fenced receipts (#189#4) handle async local steps; this tests whether paired moves remain sound and cheaper than barrier synchronization under drift.
- **Cheapest first test:** Delay branch 2's view of branch 1 by one legal B write in Paper Witness 1; compare lockstep freeze-then-pair, blind async pairing and version-fenced paired commits at equal message and B-throughput budgets.
- **Old-task retention check:** Score A/C on every admitted asynchronous version pair across $S_0$ and $S_1$, including an adversarial B write inside the fence that tries to invalidate the paired endpoint.

### Carrying a certified merge range across rebases

#### 11. Choice-preserving rebase morphisms with non-aliasing witnesses (P)
- **Mechanism:** Transport a certified range $S$ from base $x_0$ to $x_1$ via a verified map $\phi: S \to \mathcal{W}(x_1)$ certified for both A/C retention and a quantitative **B-readout injectivity floor** separating every pair of distinct useful choices in $S$.
- **Novelty vs nearest prior art:** THESEUS, ARIADNE, Trans-LoRA and Git Re-Basin transport one checkpoint or adapter. The candidate object is a *parameterized family morphism* that proves late deployment choice itself survived the rebase, not just one merged point.
- **Cheapest first test:** Run Paper Witness 2 across full-rank signed basis changes, near-singular scalings and rank-deficient projections; compare naive coefficient reuse, task-arithmetic re-extraction, Git Re-Basin, full recertification from $x_1$ and verified $\phi$.
- **Old-task retention check:** Verify A/C on every mapped point $\phi(u,v)$ for $(u,v) \in S$, check B-preference separation between $\beta_1$ and $\beta_2$ after rebasing, and audit an independent held-out old slice.

#### 12. Minimal aliasing-witness refusal certificates (P)
- **Mechanism:** When a proposed rebase $x_0 \to x_1$ is rank-deficient on choice-bearing or protected directions, refuse transport and emit a minimal witness: two distinct promised choices $(u_1, v_1) \neq (u_2, v_2) \in S$ that collapse on $x_1$ (or a kernel vector read by old slice $C$).
- **Novelty vs nearest prior art:** Rank checks and linear-algebra diagnostics detect singular maps globally, not which promised late choices died. The candidate object is a *choice-level refusal certificate* that pinpoints the exact lost deployment distinction.
- **Cheapest first test:** Test Paper Witness 2 with three rebases: rank-deficient in an unused null direction (must accept), rank-deficient in the B-separating direction (must refuse with $(1,0)$ vs $(0,1)$), and rank-deficient in $C$'s direction (must refuse with $C$'s kernel witness); compare global full-rank gating against witness-backed refusal.
- **Old-task retention check:** Confirm zero false accepts when $A$ loss drops on a rank-deficient projection, and verify $A/C$ retention on accepted rebases whose dropped direction is genuinely orthogonal to $A$, $C$ and $B$.

#### 13. Partial-range rebase with explicit excision receipts (I)
- **Mechanism:** When $x_0 \to x_1$ is full-rank on a certified sub-region $S_{\text{kept}} \subset S$ and aliases only on $S \setminus S_{\text{kept}}$, transport $S_{\text{kept}}$ with a verified map while issuing an explicit revocation receipt for the excised choices.
- **Novelty vs nearest prior art:** Contract refinement and partial verification already shrink domains; this prevents an all-or-nothing rebase refusal from wasting valid choices while banning silent shrinkage.
- **Cheapest first test:** Construct a piecewise-linear ReLU rebase that saturates (aliases) for $u + v > 1$ while remaining full-rank on $u + v \le 1$; compare all-or-nothing refusal, silent full-$S$ claim, full recertification and partial transport with excision receipt.
- **Old-task retention check:** Verify A/C and B-choice separation on all of $S_{\text{kept}}$ and confirm every excised point is blocked from deployment and charged as lost coverage in late utility regret.

#### 14. Curved pullback maps across nonlinear rebases (P)
- **Mechanism:** When $x_1$ is related to $x_0$ by a nonlinear consolidation, LayerNorm shift or pruning step, verify a piecewise-affine or smooth pullback $\psi: S \to S'$ whose image on $x_1$ preserves A/C floors and the ordering of late B preferences across the entire continuous domain.
- **Novelty vs nearest prior art:** Linear task-vector transport fails under nonlinear base drift, and pointwise distillation re-fits one preference at a time. The candidate operation is a *certified nonlinear reparameterization of a choice continuum*.
- **Cheapest first test:** Apply a known monotone nonlinear warp (e.g. quantized LayerNorm gain/bias shift or 2-piece ReLU scaling) to $x_0$ in Paper Witness 2; compare linear remapping, sampled-point interpolation, full recertification and verified piecewise-affine pullback $\psi$.
- **Old-task retention check:** Verify A/C at all vertices, kink boundaries and worst interior points of $\psi(S)$ (not just sampled grid points), plus a shared B suffix on $x_1$.

#### 15. Behavior-indexed canonical range coordinates (P)
- **Mechanism:** Index the certified range $S$ by observable B-tradeoff coordinates (a canonical behavioral chart) instead of raw linear merge weights $(u,v)$, so a rebase only has to prove a verified surjection from new merge parameters onto the promised behavioral frontier.
- **Novelty vs nearest prior art:** Weight-space parameterization ties a promise to one base's linear geometry, while functional transport (THESEUS/ARIADNE) transfers one function. The candidate object is a *base-invariant coordinate system for late deployment choices*.
- **Cheapest first test:** Rebase Paper Witness 2 through two different non-orthogonal representations $T_1, T_2$ and compare weight-indexed $\phi$ against behavior-indexed surjection certificates on proof bytes, refusal accuracy and late B utility regret.
- **Old-task retention check:** Ensure every behavioral coordinate maps to an explicitly verifiable weight realization on $x_1$ that satisfies A/C floors and held-out old-slice checks, preventing "behavioral equivalence on B" from masking hidden A/C drift.

#### 16. Suffix-preserving rebase maps under non-orthogonal basis changes (P)
- **Mechanism:** Extend the rebase certificate from immediate merge outputs to the post-merge optimizer trajectory by transporting compatible optimizer slots across $T$ or proving the distorted post-rebase training tube still satisfies A/C across all $\phi(S)$.
- **Novelty vs nearest prior art:** Weight-space reparameterization preserves forward outputs under non-orthogonal $T$ while silently breaking diagonal Adam/RMSProp geometry. The candidate operation is *dynamics-preserving range transport* across a base change.
- **Cheapest first test:** Run the non-orthogonal $T = \mathrm{diag}(2, -1/2, 1)$ positive arm of Paper Witness 2 followed by two diagonal-Adam steps; compare forward-only $\phi$, untouched slots, transported/preconditioned slots and exact post-rebase suffix verification.
- **Old-task retention check:** Match immediate A/C and B outputs exactly after rebase, then evaluate A/C at every post-merge suffix step across $\phi(S)$; reject any rebase map whose suffix violates A/C even when step 0 is exact.

#### 17. Condition-number budgets for chained rebases (I)
- **Mechanism:** Compose sequential rebase maps $\phi_{k-1\to k} \circ \dots \circ \phi_{0\to 1}$ while tracking cumulative separation margin and Jacobian conditioning, refusing a locally full-rank rebase whose composition pushes distinct promised choices below the B-distinguishing floor.
- **Novelty vs nearest prior art:** Iterative composition of Lipschitz/condition bounds is standard in numerical analysis; this audits whether repeated "individually safe" rebases silently drift into numerical rank deficiency.
- **Cheapest first test:** Chain five slightly ill-conditioned rebases (each individually full-rank with condition number 2) on Paper Witness 2 under finite precision; compare per-hop checking, cumulative condition budgeting and periodic full recertification.
- **Old-task retention check:** Verify A/C floors and B-preference separation after each hop under quantized arithmetic; flag the exact hop where finite-precision aliasing breaks either A/C or $\beta_1/\beta_2$ separation.

#### 18. Audit whether a rebase hides an unregistered old reader in its kernel (I)
- **Mechanism:** Evaluate every accepted rebase map on an independent withheld old slice $C_{\text{held}}$ that the rebase certifier never saw, measuring how often a rebase that is full-rank on declared $A$ and $B$ still erases an undeclared old capability.
- **Novelty vs nearest prior art:** Scope-vs-generalization audits exist in certified CL; this specifically tests whether "non-aliasing on B" is strong enough to protect unregistered old tasks or only declared ones.
- **Cheapest first test:** In Paper Witness 2, test a projection that drops an unregistered fourth coordinate read only by $C_{\text{held}}$ while preserving $A$ and both B preferences; compare declared-scope refusal, randomized canary probes and full-rank base gating.
- **Old-task retention check:** Report declared A/C retention separately from $C_{\text{held}}$; never claim a choice-preserving rebase protects directions outside its verified scope.

### Coupling joint moves with rebases, and break-even audits

#### 19. Co-rebased joint branch moves that rescue a rank-deficient rebase (P)
- **Mechanism:** When a proposed base change $x_0 \to x_1$ would alias $S$ for the branches as currently represented, perform a paired pre-rebase move $(d_1, d_2) \to (d_1', d_2') \in F_1 \times F_2$ that rotates the branches' choice-bearing and protected directions *out* of the rebase's kernel before applying $x_0 \to x_1$.
- **Novelty vs nearest prior art:** Rebase refusal rejects rank-deficient base changes, and single-branch pre-alignment can break cross-branch A/C before the rebase completes. The candidate operation is *cooperative kernel avoidance*: a paired move that makes an otherwise choice-destroying rebase full-rank on $S$.
- **Cheapest first test:** Combine Paper Witnesses 1 and 2 so $T_{\text{bad}}$ drops coordinate $e_1$ (occupied by $p^{(0)}, q^{(0)}$) while keeping $(e_2, e_3)$ full-rank; compare refusing $T_{\text{bad}}$, single-branch pre-move, full retraining on $x_1$ and co-rebased paired move $(p^{(0)}, q^{(0)}) \to (p^{(1)}, q^{(1)})$ followed by $T_{\text{bad}}$.
- **Old-task retention check:** Verify solo A/C and B before and after the paired move, A/C across all of $\phi(S_1)$ after $T_{\text{bad}}$, B separation between $\beta_1$ and $\beta_2$, and a shared suffix on $x_1$.

#### 20. Rebase-triggered deadlock breaking (P)
- **Mechanism:** Piggyback an atomic paired branch move across an all-single-moves barrier onto a scheduled base migration $x_0 \to x_1$, combining the base switch and paired fiber swap into one verified cutover so branches pay synchronization cost once instead of twice.
- **Novelty vs nearest prior art:** Atomic schema migrations and coordinated checkpoints already bundle state transitions. The candidate operation is *amortized cooperative repair*: using an unavoidable base change to cross a single-branch barrier with zero extra coordination round.
- **Cheapest first test:** Schedule a base rebase alongside the atomic-only regime of Paper Witness 1; compare separate paired commit + rebase, full recertification on $x_1$ and bundled rebase-plus-paired-swap on total stall rounds, proof bytes and unlocked late B utility.
- **Old-task retention check:** Verify A/C on $S_0$ up to the cutover, on $S_1$ immediately after the bundled cutover, and through a shared suffix on $x_1$; test aborting the rebase to confirm clean fallback to $S_0$ on $x_0$.

#### 21. Credit attribution between paired headroom and rebase recertification (I)
- **Mechanism:** Decompose post-rebase late B utility gains into (a) headroom genuinely freed by the paired move, (b) coefficient remapping across $x_0 \to x_1$, and (c) tighter verifier bounds from a fresh base representation.
- **Novelty vs nearest prior art:** Ablation and mixed-difference decompositions already separate sources of gain; this prevents a cleaner rebased coordinate system from inflating the apparent value of a paired move.
- **Cheapest first test:** Run a $2 \times 2$ ablation on combined Witnesses 1 and 2 (paired move on/off $\times$ rebase map vs fresh recertification) at matched B utility and proof bytes; measure each component's exact share of late regret reduction.
- **Old-task retention check:** Hold A/C floors and held-out old-slice scope identical across all four cells; attribute zero paired-move credit if fresh recertification alone recovers the same $S_1$.

#### 22. Break-even accounting for paired coordination and rebase maps (I)
- **Mechanism:** Price obstruction checking, paired synchronization stalls, co-owned ledger overhead and rebase-map verification against full recertification from $x_1$, joint Re-Basin and fixed-weight re-extraction across rebase frequency, branch count and late preference count.
- **Novelty vs nearest prior art:** Amortized verification and direct search are the ledger's standard equal-budget baselines; this makes both score-3 claims falsifiable rather than assumed wins.
- **Cheapest first test:** Sweep rebase count ($1$ to $8$), late preference count ($2$ to $8$) and barrier frequency ($0\%$ to $100\%$) on exact CPU-sized instances of Witnesses 1 and 2; map the exact frontier where full recertification or fixed-weight re-extraction beats carried ranges and paired moves.
- **Old-task retention check:** Enforce equal A/C floors, equal held-out old-slice reporting and matched B progress across every point on the sweep; never subsidize coordination cost by relaxing old-task retention.

## Ranked deeper questions

1. **Do genuine all-single-moves barriers exist in real continuous solo-equivalent fibers, or are they artifacts of discrete permutations?** Start with Paper Witness 1 embedded in continuous vs disconnected fibers (cards 1, 2, 5, 9). Compare obstruction-gated paired commits and escrowed serial handshakes against continuous single-branch path search, coordinate descent and joint Re-Basin at matched solo curves, B utility and A/C floors. If continuous single-branch moves always find a safe path around the barrier, atomic paired commits collapse to a discretization artifact.
2. **When is a choice-preserving rebase morphism cheaper and safer than full recertification from the new base?** Test Paper Witness 2 across linear, non-orthogonal, nonlinear and chained rebases (cards 11–17, 22). Require both A/C retention (including a post-rebase diagonal-optimizer suffix) and quantitative B-choice separation, with explicit aliasing-witness refusal on rank-deficient maps. If re-extracting and recertifying from $x_1$ ties at equal proof bytes and late regret, the morphism is an engineering shortcut rather than a primitive.
3. **Can a co-rebased paired move actually rescue a rank-deficient rebase that neither single-branch moves nor rebase maps alone can survive?** Test the combined Witnesses 1 and 2 setup (cards 19–21) where $T_{\text{bad}}$ drops a coordinate occupied by the current branch orientation, while a paired move rotates both branches into the rebase's full-rank subspace without breaking A/C. Check whether full retraining on $x_1$ or simple rebase refusal + fresh B training ties at matched total cost.
4. **How should co-owned headroom from a paired move be re-partitioned so both branches can resume independent continual learning?** Start from the unlocked $[0,1]^2$ state of Paper Witness 1 (cards 3, 6, 10) and admit a stream of independent B updates under partial disclosure and asymmetric staleness. Measure whether a co-owned headroom ledger prevents unilateral re-locking better than heuristic 50/50 splits or periodic lockstep recertification without stalling B throughput.

**Verdict:** Keep both score-3 directions — and their synthesis in co-rebased paired moves — as conditional primitive candidates. Start with exact CPU-sized oracles on Witnesses 1 and 2 before touching neural networks: require a proved all-single-moves barrier (testing whether it survives continuous fibers), non-aliasing rebase transport that preserves post-merge suffix retention, and an explicit win over coordinate descent, joint Re-Basin, task-arithmetic re-extraction and full recertification at matched A/C retention and total evidence cost.
