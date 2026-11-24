# Certified merge-weight ranges: keep the choice open while learners train

**Status:** Ideas only; no experiments, code, or GPU work. **Parent:** [Merge-aware budgets](merge-aware-budgets.md) ([PR #181](https://github.com/manojbajaj95/cl/pull/181)), cards 9 and 14. **Review seed:** [Flood triage row 286](https://github.com/manojbajaj95/cl/blob/77f6bb2847e1efc4b511f25baaa7c483b600851b/reviews/flood-triage.md#L286), the two score-3 directions: certify an entire range of coefficients that can be chosen late while both learners keep training; repair the mixed interaction inside a verified task-equivalent region without changing either solo score. **Ledger read first:** [Idea ledger](https://github.com/manojbajaj95/cl/blob/77f6bb2847e1efc4b511f25baaa7c483b600851b/reviews/idea-ledger.md). Coded merge interference was killed against equal-budget direct search; a fitted interaction score is not evidence. Forecast-weighted write selection failed after retention matching; compare useful progress at matched retention, not against weaker or less informed learners.

## Is keeping a future merge choice open a continual-learning primitive?

**Not as a flat interpolation curve or an interference-reducing edit.** [Model soups](https://arxiv.org/abs/2203.05482), [linear mode connectivity](https://arxiv.org/abs/1912.05671), [task arithmetic](https://arxiv.org/abs/2212.04089), [TIES](https://arxiv.org/abs/2306.01708) and [proximity-regularized merging](https://arxiv.org/abs/2609.32332) are the starting controls for compatible weights or coefficient sensitivity. [Git Re-Basin](https://arxiv.org/abs/2209.04836) and [tangent-space task arithmetic](https://arxiv.org/abs/2305.12827) already use representation alignment or disentanglement to make weights easier to combine. The novel claim cannot be “equivalent models merge differently.” For proofs, [Pacti](https://arxiv.org/abs/2303.17751), [CROWN](https://arxiv.org/abs/1811.00866) and [Certified CL](https://arxiv.org/abs/2407.06697) supply contract, bounding and retraining controls; none needs to be reinvented for this test.

**Conditional candidate:** keep a versioned set of future deployment choices valid across independently admitted writes, then recover an excluded choice by making a proved repair that does not pay for the recovery with solo behavior. A late B-side preference should be able to choose between at least two genuinely different useful merges from the certified set without querying old tasks again. The point is not to beat exact recertification in safety or coverage, but to achieve useful late choice and continued training at lower total evidence cost. If the strongest conventional stack ties, call it certified merging with ordinary contracts and repair.

### What is actually promised?

- **Quantify over choices and paths.** Fix an old-task reference before forking, protected old-task slices A and C (neither trained on during the fork), new-task utility B, a merge rule, a nontrivial coefficient set S, eligible merge times, and permitted training/optimizer transitions before and after merge. For every admitted pair of branch prefixes, every authorized merge time, every coefficient in S, and every permitted suffix prefix, require the declared A/C floors on the resulting deployment. Check the required branch-local floors too. A path that can't reach the promised merge window with useful B is a missed delivery, not a safe success. Only claim safety for the declared tasks and transitions; a proof over finite witnesses does not certify a task population. Audit generalization separately on held-out old examples that the certifier never sees.
- **Separate the two obligations.** On the additive delta merger, for a scalar old-task statistic L at base x, write `J(u,v) = L(x+u*d+v*e) - L(x+u*d) - L(x+v*e) + L(x)`. The signed residual plus the two solo changes is the exact change in L. Upper-bound harmful J separately for each old slice when L is a loss (or reverse signs for margins). The formula is for the named merger and statistic, not an identity for TIES, joint normalization, or a different loss. A checkpoint proof is not automatically valid at the next write: independently issued checks must imply the joint property for their full product of admitted states, or require a new paired receipt before exposing the update.
- **Repair, then reissue.** Name a verified equivalence predicate before proposing a repair: preserve both branches' solo scores (including weighted solos for the claimed range when using J to assign credit), the declared B behaviors, and any optimizer/state conditions needed for the suffix. An unchanged aggregate alone is not equivalence; distinguish exact output equivalence from exact equality of declared per-slice scores. Verify every visible repair prefix, then prove a smaller harmful interaction envelope under the same reference and scope or explicitly certify additional coefficients. A pointwise improvement at today's best coefficient does not spend down the worst-case allowance. Never discard promised coefficients, erase B, or relabel the reference and call it repair.
- **Make choice valuable.** Hide the eventual B preference until after both learners have made useful updates. Report late utility regret against exact feasible selection, certified set size/geometry at a fixed design domain, useful solo progress, blocked writes and missed deliveries, worst-prefix A/C retention, and all proof bytes, queries, inter-branch messages and verifier time. Compare early fixed coefficients, frozen branches, coefficient-robust shaping, late search plus full rechecking, and an equally informed adaptive-contract + verifier + repair stack. Match states, B effort and old-task access where the comparison calls for it; include a no-conflict instance where simple merging should win.

### Two paper witnesses, not results

1. **An exact frontier in coefficient space.** For a quantized two-branch ReLU toy, let the old output be `ReLU(-1/2 + (5/8)u + (1/2)v)` with cap `1/8` and independent `u,v ∈ [0,1]`. Each axis is safe; the exact joint feasible region satisfies `(5/8)u + (1/2)v ≤ 5/8`. The kink at `1/2` in preactivation increment is not a failure; the cap boundary is included and any positive excess fails. Even the safe points `(1,0)` and `(0,1)` do not justify their bounding box. Enumerate rational branch states and suffix prefixes, then intersect their exact coefficient regions; branch-state quantization does not quantize the requested coefficients. Add a second old slice and a later write that invalidates part of the original frontier, as well as a B-only readout that rewards different points under two hidden preferences.
2. **Same solo scores, different interaction.** For old squared error on a two-coordinate residual with zero base residual, take equal-length solo changes `p=(1/5,0)` and `q=(1/5,0)`; replace q with `q'=(0,1/5)`. For all weights, the weighted solo losses are still `u²/25` and `v²/25`; the mixed term drops from `2uv/25` to zero. At `u=v=1` the loss moves from `4/25` to `2/25` under a cap of `3/25`. This is score equivalence, not equality of the residual vectors. Make B depend on a separate preserved useful coordinate and score C independently; then plant a directional old reader and a suffix that amplifies the rotated component. The repair must be rejected if either is in scope and fails. If orthogonal initialization already achieves the same frontier and progress on every stream, the witness shows only that geometry matters.

## Idea cards

**P** denotes a candidate primitive, not a priority claim. **I** denotes an improvement, control, or audit. All first tests below are CPU-sized proposals, not runs.

### Keep late choice certified

#### 1. Carry a coefficient region across independent writes (P)
- **Mechanism:** Give each branch a local test against a joint product envelope that preserves the same S at every eligible merge time. The deployment chooser receives S, not the training traces.
- **Novelty vs nearest prior art:** Proximity-regularized merging flattens old-task sensitivity; Pacti can express the guarantee. The candidate operation is spending local training freedom without canceling an issued continuum of deployment choices.
- **Cheapest first test:** Use the exact quantized ReLU frontier with two independently proposed B updates per branch; compare fixed coefficients, proximity shaping, the adaptive-contract stack and exact rechecking. Reveal two distinct B preferences after updates; count both delivery and B progress.
- **Old-task retention check:** Confirm A/C on all visible local prefixes, the full promised region at each eligible merge, and a shared B suffix; count a dropped coefficient as a failed promise.

#### 2. Keep a slanted promise rather than buy a box (I)
- **Mechanism:** Publish certified coupled inequalities so one coefficient can rise only if another falls. Treat interval bounds on individual coefficients as projections, not as independent rights.
- **Novelty vs nearest prior art:** Polyhedral abstract interpretation already keeps correlations; applying it here prices the cost of treating coefficients independently.
- **Cheapest first test:** Match receipt bytes for a box cover, a slanted polytope and exact half-space intersection on the ReLU witness; give B opposite preferences for the two axes.
- **Old-task retention check:** Audit joint corners, boundary equalities and just-outside points on A/C after another write; reject any cover that fills unsafe corners.

#### 3. Issue a choice with a hole (I)
- **Mechanism:** Represent a union of disjoint safe coefficient cells and allow late jumps between them only if no intermediate configuration is deployed, or certify a safe path separately.
- **Novelty vs nearest prior art:** Mode connectivity and branch-and-bound already distinguish low-loss paths from detached feasible sets; this audits the deployment semantics of a certified choice.
- **Cheapest first test:** Build a triangular interior loss bump with three ReLUs along a scalar interpolation; compare endpoints, a sound connected subinterval and a two-cell cover at matched proof size.
- **Old-task retention check:** Score A/C at each inner boundary, on the gap and after later B updates; explicitly test any deployed interpolation between cells.

#### 4. Protect the full feasible set under stale partner receipts (P)
- **Mechanism:** Let either learner progress using a partner receipt valid for a fenced version window. Bind the fence to the partner's entire admitted drift envelope; require a new receipt outside the fence.
- **Novelty vs nearest prior art:** Assume-guarantee contracts and bounded-staleness systems cover the pieces. The candidate is the asynchronously reusable right to choose weights across more than one independently advancing checkpoint.
- **Cheapest first test:** Enumerate delayed and out-of-order handoffs for two short ReLU streams; compare lockstep verification, a static worst-case envelope and time-indexed contract refinement at equal message budget.
- **Old-task retention check:** Include the pair of individually legal writes that jointly open an old gate under a stale point certificate; check A/C on every admitted asynchronous prefix and after deployment.

#### 5. Certify the choice through a shared optimizer suffix (I)
- **Mechanism:** Include the post-merge optimizer initialization rule and propagate a coefficient-dependent tube through shared training, rather than applying a snapshot certificate to the suffix.
- **Novelty vs nearest prior art:** Certified CL and robust reachability already handle protected retraining; the change is to verify the whole coefficient set as initial conditions.
- **Cheapest first test:** Enumerate three steps of a two-slot quantized recurrence where momentum moves the worst coefficient from an endpoint to an interior gate; compare exact product search, unrolled bounds and a snapshot-plus-norm control.
- **Old-task retention check:** Check A/C on both sides of the gate at every suffix step, including a transient failure that disappears by the endpoint.

#### 6. Reveal a utility preference after the training decisions (I)
- **Mechanism:** Predeclare the distribution or finite menu of deployment preferences, then evaluate policies without letting either branch train on the revealed choice.
- **Novelty vs nearest prior art:** Task arithmetic already tunes coefficients; decision theory already values deferral. This measures the value of a proved late choice rather than claiming one from interval width.
- **Cheapest first test:** Use two equally likely B objectives whose exact maximizing weights lie far apart; compare a fixed weight optimized over the same menu, late certified selection and late exact search.
- **Old-task retention check:** Require A/C at both selected extremes and all certified interior coefficients after the same B budgets and suffix; include arbitrary legal selection independent of B.

#### 7. Trade information for coefficient coverage before deployment (P)
- **Mechanism:** Ask a partner for a separating state predicate only when it can unlock a useful region that the shared envelope cannot distinguish; reprove coverage after receiving it.
- **Novelty vs nearest prior art:** [CEGIS](https://people.csail.mit.edu/asolar/papers/thesis.pdf) and decision-relevant queries ([PR #174](https://github.com/manojbajaj95/cl/pull/174)) already guide evidence acquisition. The candidate is acquiring a defeasible region-specific promise instead of another unconditional compatibility score.
- **Cheapest first test:** Plant two partner states identical under solo statistics but opposite on an interior ReLU cell; compare blind robust coverage, exhaustive disclosure and active predicate requests at equal bits and queries.
- **Old-task retention check:** Try both hidden states, including an ambiguous reply; no new cell should be accepted unless A/C and their suffix bounds follow for all surviving states.

#### 8. Transfer the range across a change of base only with a coefficient map (P)
- **Mechanism:** On rebasing, verify a map from each promised coefficient to its new implementation, preserving useful choices and the relevant merge/suffix outputs; refuse if the new representation aliases distinct useful choices.
- **Novelty vs nearest prior art:** Task arithmetic fixes a base, Git Re-Basin aligns representations, and Pacti handles refinement. The candidate transfer preserves a family of exercisable late choices, not just one checkpoint.
- **Cheapest first test:** Reparameterize a two-branch linear host with a signed basis change, then use a rank-deficient projection as the negative arm. Compare explicit remapping against full recertification from the new base.
- **Old-task retention check:** Verify A/C before and after rebasing for every promised coefficient, with an old slice reading the lost direction and another checked after shared training.

#### 9. Price a genuinely higher-order coalition (I)
- **Mechanism:** For three branches, use exact pair constraints only where a verified remainder covers triple interactions; otherwise split the coefficient region around a coalition-only gate.
- **Novelty vs nearest prior art:** Factor graphs and higher-order verification already describe such couplings; this is an audit against the ledger's rejected sparse pairwise surrogate.
- **Cheapest first test:** Put a ReLU threshold above any sum of two branches but below the sum of three. Compare pair-only, a checked triple remainder and direct joint enumeration at matched verification queries.
- **Old-task retention check:** Ensure A/C survive every approved face and interior coalition coefficient through the suffix; show the pair-only certificate fails on a planted interior point.

#### 10. Give each merge rule its own legal coefficient cells (I)
- **Mechanism:** If the merger lets coefficients affect trim, sign-election or clipping decisions, split cells at the relevant boundaries and verify the actual rule on each, including deterministic tie handling.
- **Novelty vs nearest prior art:** TIES already specifies trimming and sign resolution, and piecewise verification already handles switching; additive residuals do not transfer automatically.
- **Cheapest first test:** Use two small signed vectors with a tie that flips an elected sign; compare a sign-stable-cell proof, exact enumeration of cases and a smooth surrogate.
- **Old-task retention check:** Score A/C on both sides and exactly at each boundary, and after a suffix conditioned on the elected sign.

#### 11. Find when any positive-width promise is impossible (I)
- **Mechanism:** Use indistinguishable local states whose possible joint continuations leave disjoint feasible coefficient regions; isolate the information or coordination needed for a nonempty common promise.
- **Novelty vs nearest prior art:** Standard indistinguishability arguments and robust feasibility already supply the proof method; a sharp example would locate the failure of solo-only merge receipts.
- **Cheapest first test:** Give two states identical complete solo-score curves but opposite signed couplings, plus two-sided retained margins so neither conservative extreme suffices. Compute the exact set for each state before proposing a receipt.
- **Old-task retention check:** Check A/C on both worlds at every candidate coefficient and test a one-bit separating predicate; count refusing all useful merges as loss of coverage, not sound success.

### Repair only the interaction

#### 12. Search a verified score-equivalent fiber (P)
- **Mechanism:** Compute a repair in the intersection of both branches' declared solo-score levels and the B equivalence region. Reissue only with a strictly smaller worst harmful J on the same scope, or a jointly proved strict expansion of S.
- **Novelty vs nearest prior art:** Tangent-space disentanglement and Git Re-Basin already reduce merge interference. The candidate is recovery of a previously excluded future choice with unchanged solo behavior after useful learning.
- **Cheapest first test:** Use the equal-norm rotation witness; compare upfront orthogonal choice, projection alone, orthogonal training, post-merge correction and exact joint recertification at matched B utility and old scores. Give a later partner an orientation not known at training time.
- **Old-task retention check:** Match both weighted solo-score curves exactly; check A/C for visible repair steps, all new and previous choices, and a shared suffix. A planted directional reader must invalidate the fiber.

#### 13. Separate real interaction credit from cancellation (I)
- **Mechanism:** Attribute restored coverage to improvements in the per-slice harmful interaction bound; report actual deployment safety separately from changes in baseline, solo charges and bound looseness.
- **Novelty vs nearest prior art:** Mixed differences and variance decompositions already separate effects; this prevents better solo scores or a new verifier from masquerading as interaction repair.
- **Cheapest first test:** Plant three matched endpoint gains: lowered solo error, true J reduction and a tighter proof of an unchanged state. Verify all three against exact branch and joint readouts on the same cells.
- **Old-task retention check:** Check A/C slice by slice and their suffix bounds; only the true J reduction with preserved solos qualifies for repair credit.

#### 14. Keep interaction relief robust to the partner's next write (P)
- **Mechanism:** Choose a repair by its worst interaction against the full admissible partner continuation envelope, not the current partner direction.
- **Novelty vs nearest prior art:** Robust optimization already handles uncertainty and orthogonal training controls present overlap. The proposed reissue changes which inherited coefficient choices are safe without changing solo behavior.
- **Cheapest first test:** Give a partner two possible quantized rotations after the repair. Compare current-gradient projection, upfront orthogonality to all directions and robust repair with exact lookahead; include a case with no legal repair.
- **Old-task retention check:** Hold weighted solos and B fixed, and evaluate A/C for each allowed next branch direction, including one that reverses the apparent present-day benefit.

#### 15. Repair disconnected equivalent states without claiming a safe path (I)
- **Mechanism:** Distinguish an atomic publication of a verified new representation from a visible sequence of in-place moves. Prove the latter through the entire equivalence region or refuse it.
- **Novelty vs nearest prior art:** Git Re-Basin and transactional publication already distinguish function-preserving swaps from continuous interpolation; this audits which type of repair earns credit.
- **Cheapest first test:** Use a hidden-unit permutation with identical endpoints but a failed interpolation. Compare atomic swap, interpolation and an exact finite transition search given the same scratch budget.
- **Old-task retention check:** Check A/C on all exposed states and merged suffixes; if the swap changes optimizer slots, require them to move with the units or prove equivalence under the stated optimizer.

#### 16. Move both branches when neither can repair alone (P)
- **Mechanism:** Prove a joint endpoint and either a safe serial route or an atomic paired commit; let neither branch unilaterally claim the resulting coverage.
- **Novelty vs nearest prior art:** Joint re-basin alignment and two-phase commit already coordinate changes. The candidate operation frees range-specific headroom trapped behind individually unproductive equivalent moves.
- **Cheapest first test:** Enumerate finite task-equivalent orientations with a planted all-single-moves barrier and a safe joint move; compare independent projection, coordinate descent, exact joint recertification and paired publication.
- **Old-task retention check:** Match each solo's A/C and B; try publishing one half early and score A/C over the old and new regions after each allowed step and the shared suffix.

#### 17. Track which coefficients gained and which lost after repair (I)
- **Mechanism:** Require old S to remain included when claiming an expansion. If a move shrinks A/C liability at one edge and raises it at another, issue it only as a separately negotiated replacement, not recovered right.
- **Novelty vs nearest prior art:** Pareto dominance and set-based contract refinement already distinguish inclusion from a trade; area alone is not a safety metric.
- **Cheapest first test:** Use two old slices with opposite directional couplings so a rotation shifts the frontier without dominating it; compare area, set inclusion and exact late utility regret under two preferences.
- **Old-task retention check:** Check A/C at the original extreme where the moved frontier fails, including a preference that still selects it late and the post-merge continuation.

#### 18. Separate an equivalent scoring region from a blind witness (I)
- **Mechanism:** Construct the equivalence predicate from explicit read dependencies or finite exact semantics, then use independent adversarial old examples to audit the declared task scope.
- **Novelty vs nearest prior art:** Certified CL and formal equivalence already separate guarantees from sampling. Unlike the ledger's killed read-pinning ABI, this audit does not pin all intermediate activations to manufacture an equivalence.
- **Cheapest first test:** Make two representations agree on a publisher panel but disagree on a reachable old input. Compare score matching, exact finite equivalence and a matched-budget refreshed canary.
- **Old-task retention check:** Require A/C on the declared finite scope and report withheld old-reader performance separately, including any failure that only appears at an intermediate coefficient.

#### 19. Preserve the right through a repair that changes optimizer geometry (I)
- **Mechanism:** Treat optimizer state as part of equivalence for a suffix: transport compatible slots or prove the resulting paired training tube instead of assuming predictions imply equivalent learning.
- **Novelty vs nearest prior art:** Parameter symmetries and the parent's optimizer-state contracts already motivate transport. This checks whether an interaction repair survives a future useful write.
- **Cheapest first test:** Apply a hidden-unit permutation and compare transported versus untouched diagonal second moments in a two-step update; include a non-orthogonal reparameterization where simple slot permutation is inapplicable.
- **Old-task retention check:** Match immediate solo scores exactly and test A/C at every later local or merged prefix; an immediate J drop with a worse suffix earns no reissue.

#### 20. Require a repair that survives an independent readout (I)
- **Mechanism:** After proving repair on declared A, test whether it simply steers damage into old behaviors outside A. Audit against an independent C reader; when C is part of the promise, incorporate it before issuing credit.
- **Novelty vs nearest prior art:** Multi-objective verification and old-task holdouts are known; this specifically tests whether a large score-equivalent fiber came from an underspecified old task.
- **Cheapest first test:** Use two equal-norm rotations with the same A interaction but one worsening C; compare projection on A alone, multi-reader repair and exact feasible intersection.
- **Old-task retention check:** Keep solo A/C and B fixed and report worst C after merge as well as A; distinguish a counterexample to a declared proof from a scope/generalization failure.

### Test whether the combination matters

#### 21. Let two later preferences compete for one repaired promise (P)
- **Mechanism:** Without retraining, let a verifier-backed chooser use a repaired range under two alternative deployment preferences. They are counterfactual choices from one receipt, not two consumptions of shared slack.
- **Novelty vs nearest prior art:** Model soups and proximity shaping can yield multiple good mixtures, while verified repair can improve one point. The candidate is lifting a repair to a reusable future choice that remains valid through local learning.
- **Cheapest first test:** Cross fixed weight versus retained range with no repair versus proved equivalent repair. Add exact joint recertification and the conventional adaptive-contract stack. Seek gains beyond single-point repair, not just gains over an unsafe merge.
- **Old-task retention check:** Compare all arms at matched A/C floors, weighted solo and B progress; exhaust the exact feasible region and future prefixes, not just the two selected endpoints.

#### 22. Find the break-even scale for keeping the option (I)
- **Mechanism:** Price issuance, local updates, joint repairs and final checking together; buy a range only when avoiding repeated joint checks or improving late utility repays those costs.
- **Novelty vs nearest prior art:** Amortized verification and direct search already supply the baseline. This makes the novelty claim falsifiable at equal information, as required by the ledger.
- **Cheapest first test:** Count proof obligations, queries, bytes and decision regret as permitted prefixes and late preference counts increase in exact finite hosts with matched conflict levels. Include cases with no future merges and a single late merge.
- **Old-task retention check:** Demand equal A/C scope and worst-prefix floors, including held-out performance, and equal useful B progress or an explicit utility trade-off; never charge unrelated learners for a joint promise.

## Ranked deeper questions

1. **Can two independently advancing learners keep the same meaningful coefficient set open until the B preference arrives?** Start with exact feasible intervals and coupled regions for two quantized ReLU branches (cards 1–6, 11). Compare useful writes and late utility to fixed coefficients, proximity shaping and equally informed adaptive contracts, with exact rechecking as the oracle. A shrinking or vacuous set, frozen learners, or missed deployment does not answer yes.
2. **Can an unanticipated partner force a repair that really changes only the interaction?** Test the exact equivalence witness and the directional-reader falsifier (cards 12–16, 18–20). Match both solo-score curves and B utility; require an actual reduction in certified harmful interaction or an inclusion-preserving range expansion, then exercise a shared suffix. If upfront orthogonality, projection alone, orthogonal training or post-merge correction ties at the relevant costs and timing, the new operation has not earned its claim.
3. **What is the minimum shared evidence needed to certify late choice after more learning?** Use indistinguishable states, stale receipts, coalition-only failures and changed merge semantics (cards 4, 7–11, 14). Look for the first additional bit or version restriction that restores useful coverage, and test whether the same information lets conventional contract refinement tie.
4. **Does combining the two rights buy more than either one alone?** Cross persistent range and proved repair at matched solo behavior, B progress, retention scope and total evidence (cards 17, 21–22). Seek a stream where repair reopens useful alternatives after training and a late preference actually exercises one. Report where recertifying at deployment is cheaper.

**Verdict:** Keep both score-3 directions as conditional primitive candidates. Start with exact CPU-sized oracles, not a neural sweep: require a nontrivial range to survive useful independent training and a verified equivalent repair to expand or strengthen it without changing solo scores or losing normal old-task performance. A tie with same-information adaptive contracts, certified merging and proved repair leaves an engineering result, not a novelty claim.
