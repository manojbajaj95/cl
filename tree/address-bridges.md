# Multi-partner address bridges

**Status:** Ideas only. One exact paper witness; no pilot, implementation or GPU. **Parent:** [Description-built partners](description-partners.md), [PR #218](https://github.com/manojbajaj95/cl/pull/218), card 09. **Review seed:** [the score-3 idea for #218 in flood triage, line 331](https://github.com/manojbajaj95/cl/blob/dd1e24bbe087dd28e3c271c07c6147f5db135261/reviews/flood-triage.md#L331): compile a fresh address's public reader/slot description into a signed correction set on at most `k` of its own spare units. Publish once, before the requested partner is known. Later join **any one** of several already-shaped partners, with no per-partner reshaping or stored edge list.

**Can one neutral local write buy choices that would otherwise require several separate writes?** Having several addresses with the *same* residual does not suffice: the parent already covers that case. The interesting target is a single registered state that can serve partners with *different* obligations, via a common release rule. A chooser may read the arriving partner's public interface (not its ID as a lookup key); it may select which registered units to retire, but it may not refit them, rewrite the old partner, or update a table. If the contract forbids even this choice of what to retire and admits only one fixed removal mask, the additive version has no such multi-residual bridge.

## Contract and controls

- **W1, edit locality:** registration changes only the fresh address. A release may retire units in its declared release set, but only the declared global survivors may receive compensating writes. For the witness below, eligible local spares can be retired, not rewritten, at release. Declare these permissions before shaping; do not grant broader permissions to the bridge than to the controls. Also run the open-editor control, where direct spare donation can accomplish the same transfer. Price each occupied spare at its best alternative use, and do not call a slot free while it still carries an obligation.
- **W2, information accounting:** charge map weights, descriptor bits, selectors, certificates, storage for retained spares and any side information at its actual precision. An arbitrary labeled bipartite menu with `F` fresh addresses, `M` old ones and `d` choices per fresh address has `binom(M,d)^F` possibilities before imposing column constraints. This is a worst-case information bound for representing arbitrary menus, not a per-instance bound or evidence that all menus are physically realizable. Test a structured family against a twin that permutes descriptor-to-physical-interface assignments within matched strata while keeping the physical feasible graph and its degree marginals intact. An informed table still has the true edges; a frozen description-only map should lose its *excess* coverage over the blind prior. Report exact online recovery separately, at its real query/compute cost. Hold out whole address banks and prevent IDs, ordering, and cached solver traces from serving as edge labels.
- **One registration, one consumption:** freeze the whole published state before revealing the request. Fork that same state for every candidate in a small test; after a real join do not count its counterfactual alternatives as still available. Measure first-request reuse, number of distinct residual signatures served, usable writes to the two vacated slots, and registration/join/refusal cost. Match capacity, metadata bytes, write permissions, deadlines and new-task utility. Count failed attempts and proof cost.
- **Strongest stack:** compare [#208 card 02 single-partner registration](cancelling-counterweights.md) (including the best single choice), separate single registrations at equal aggregate spare budget, an informed byte-matched edge table **plus** exact lawful repair, re-register-on-request and per-pair reshaping as paid relaxations, exact repair without a map, [#198 card 05 shared openings](joint-releases.md), and open-editor donation. Give each baseline the same public interfaces and allowed retirement choices. If an exact solver plus amortization or a compact table matches full cost, report that tie rather than claiming a primitive.
- **A/C retention:** `A` is legacy service; `C` is the accepted newer service and all live downstream readers, including the fresh address's original readers. Compare outputs at deployed precision before and after registration, after each forked release or refusal, and after actually filling both vacated slots with useful new writes. An ambiguous descriptor must be refused unless the proposed join can be certified independently; include matching-description/hidden-reader decoys. A safe refusal is not service.
- **Ledger exclusions:** the [idea ledger](https://github.com/manojbajaj95/cl/blob/78c09a6263dafb1cad2c8afd9c6f53cca97c819c/reviews/idea-ledger.md) kills sparse merge-interference surrogates at matched audit budget, structural-rank-only safety certificates and guarantees obtained by save/restore. Sparsity here is a budget on *physical correction units*, not a claim that damage is sparse. Certified algebra is a feasibility check, not an empirical gain. A hypernetwork outputting adapters is prior art; so is saving an edit and applying it later.

### W3: a fixed payload cannot bridge distinct residuals, but selective retirement can

Consider the additive protected head on `[0,1]^5` with basis functions `x₁,…,x₅`. Let the global survivor's allowed updates be `S = span(x₁,x₂)` within bounds that permit `x₁+x₂`. Compare removed contributions modulo `S`: an old slot contributes `p+r` and a fresh slot initially contributes `q`, with `p=x₁`, `q=x₂`. For a fixed registered contribution and a fixed footprint removed at the fresh address, write its removed contribution modulo `S` as `−v`. The release equation is then `[r]=[v]`. No fixed footprint can support two distinct residual classes, regardless of how many spares were used during registration.

Now give the fresh address two dormant spares that implement `u=x₃` and `v=x₄`, and let its releasable slot implement `q−u−v`. Assume these are legal local coefficients, with spare coefficients bounded by one in magnitude. One local write installs `(q−u−v,+u,+v)` in place of `(q,0,0)`. The sum stays `q` on the entire domain. At join time always retire the fresh main slot and the requested old slot; keep exactly those spares whose registered terms sum to the requested residual, and retire the other spares. Write only `p+q` into the global survivor:

| Requested old residual | Fresh spares left in place | Fresh contribution removed | Total removed |
| --- | --- | --- | --- |
| `u` | `+u` | `q−u` | `p+q` |
| `v` | `+v` | `q−v` | `p+q` |
| `u+v` | both | `q−u−v` | `p+q` |

Both main slots become writable; any spared unit left in place stays occupied. No already-shaped slot is refit, and no coefficient at the fresh address is changed at the join apart from unit retirement. The rule is subset sum on the signed terms and the arriving residual, not three stored edge labels. If all spares must also disappear, only the zero-residual case can work. If no spare can retire, only `u+v` works here. A fourth request with residual `x₅` fails: the three independent quotient directions need at least three one-term spares under this rule. With `k` binary-retirement spares there are at most `2^k−1` distinct nonzero signatures, not necessarily that many legal joins. Multiple addresses can share a signature. Direct donation in the open editor writes the required `u` and/or `v` on demand and absorbs `p` globally without first registering; it need not vacate the fresh main slot to do so. Compare it at equal *useful new-write* demand, including any local cleanup needed to free that slot. W3 proves feasibility and a failure case, not learnability, reduced cost, or real task retention after new writes.

## Idea cards

### Compile choices without enumerating partners

#### 01. Description-to-subset bridge
- **Mechanism:** Learn a single map from public fresh-interface features to at most `k` physical signed terms. Train on feasible neutral corrections, not on edge IDs. The frozen release rule matches a requested quotient residual to an admissible subset of those terms.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Text-to-LoRA](https://arxiv.org/abs/2506.06105) emits parameter updates from text. The proposed operation exposes a family of legal, mutually exclusive *retirements* from one neutral physical edit, not different generated adapters on demand.
- **Cheapest first test:** Lift W3 to tiny integer banks with permuted feature names, then withhold complete banks and partner combinations. Compare one use of the registered bridge to the full control stack, including the shuffled assignments.
- **Old-task retention check:** Exhaust A/C on the integer domain before and after registration and on every join/refusal fork, then fill both freed main slots with new tasks at the same success threshold as the controls.

#### 02. Teach the quotient, not the raw correction
- **Mechanism:** Predict signed terms in equivalence classes modulo legal survivor updates, then choose representatives that fit the fresh slot and each spare's coefficient range. Use one common realizability check at registration, rather than solving for a new representative at each request.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) adds task vectors; parent #208 card 06 already matches a *pair* modulo survivors. The additional operation is to install one physical representative set that realizes several classes and their combinations.
- **Cheapest first test:** Add large survivor-only offsets to otherwise identical W3 families; compare raw-vector prediction and exact quotient repair with and without joint representative selection. Include a class with no legal local representative.
- **Old-task retention check:** For each accepted branch, verify the compensating survivor stays in range and preserve old outputs in both changed and untouched coordinates.

#### 03. Learn reusable sums, not popular edges
- **Mechanism:** Train the map to maximize the number of held-out residual *combinations* covered by each signed term set. Hold out complete compositions even if their component directions occur in supervision.
- **Novelty vs nearest prior art — IMPROVEMENT:** [End-to-end sparse dictionary learning](https://arxiv.org/abs/2405.12241) optimizes dictionaries for network behavior. Here the objective is coverage by jointly realizable retirements, not reconstruction error; an ordinary dictionary followed by a lawful placement solver is the control.
- **Cheapest first test:** Supervise on singletons and some pairs in a small signed-integer dictionary. Hold out all triples and a dependent but unrepresentable combination; compare with standard dictionary fit and exact maximum coverage at `k=3`.
- **Old-task retention check:** Exercise each held-out release, including ones with identical support but different signs, and confirm all rejected requests preserve A/C.

#### 04. Compile a decoder from the geometry
- **Mechanism:** Prefer realizable signed sets with a cheap shared decoder, e.g. triangular exposed coordinates that determine which spares survive without enumerating subsets. Fall back to paid exact search or refuse when ambiguous.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Learned indexes](https://arxiv.org/abs/1712.01208) accelerate lookup by learning its structure. The decoder here recovers a lawful retirement mask from coordinates without storing records for individual partners.
- **Cheapest first test:** Compare triangular signed sets against same-coverage sets requiring enumeration. Charge the structured set's fit losses and decoder bytes; time exact decoding with and without the learned compiler.
- **Old-task retention check:** Check every decoded mask against the full residual and all protected outputs; use a residual that agrees on pivots but fails a nonpivot coordinate.

#### 05. Spend a spare on a shared sign contrast
- **Mechanism:** When two requested residuals share a common term but flip another sign, compare installing both signs as separate bounded units with installing a common base plus one signed difference. Later choose subsets; do not allow a unit to change sign at release.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Task Arithmetic](https://arxiv.org/abs/2212.04089) makes signed differences explicit. Here sign factoring has to survive per-unit amplitude bounds, neutral installation and an immutable retire/keep selector.
- **Cheapest first test:** Compare `r+s` and `r−s` in small integer banks; try `{r+s,−2s}`, then tighten the spare bound until the difference becomes illegal. Compare to direct signed installation and a full bounded solve.
- **Old-task retention check:** Evaluate both branches at sign and magnitude boundaries, including the case that refuses because representing the contrast would saturate a spare.

#### 06. Support matters more than span
- **Mechanism:** Give the map two loss terms: coverage of requested quotient directions and exact realizability as allowed subsets. Penalize predictions that have adequate rank but whose subsets collide or leave holes.
- **Novelty vs nearest prior art — AUDIT:** [LoRA](https://arxiv.org/abs/2106.09685) and ordinary factor models operate in a low-rank update space. Rank is only a lower bound on required independent units here, not a safety certificate; the ledger already kills such proxies.
- **Cheapest first test:** Compare dictionaries `{u,v}` and `{u,u+v}` for the menu `{u,v,u+v}`. They have the same span and sparsity but different coverage. Check against exhaustive lawful masks.
- **Old-task retention check:** A span-only false positive (request `v` from the second set) must be refused without disturbing any live task.

### Make the permission model carry its weight

#### 07. Release footprints with two real writes
- **Mechanism:** Require a bridge to free enough *usable* capacity in both main slots at every advertised join; schedule new writes against the capacity actually left by retained spares, not nominal addresses.
- **Novelty vs nearest prior art — AUDIT:** [Net2Net](https://arxiv.org/abs/1511.05641) preserves a function while changing a network. This check distinguishes genuine reuse of freed slots from relabeling an occupied fixed-width state.
- **Cheapest first test:** Couple the W3 spare bank to a tiny allocation problem where freeing the main slot alone may not suffice for its requested new write. Compare bound-aware planning to counting two vacancies.
- **Old-task retention check:** Evaluate A/C after each new write, including the old reader that still needs a retained spare. Do not credit a branch where either new write fails.

#### 08. Same signatures, different permissions
- **Mechanism:** Compile one signed set against a public description of legal keep/retire masks, e.g. two spares tied to a single deallocation block. Put jointly needed terms in independently retireable blocks only when that is truly available.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [Sparsely gated MoE](https://arxiv.org/abs/1701.06538) routes inference to experts. These masks govern irreversible changes of ownership at a release, not inference routing; the test is whether registration can create usable alternatives across those block boundaries.
- **Cheapest first test:** Use identical W3 features with independent versus co-retiring spares. Compare a permissions-aware compiler with an exact block-aware solver and an unconstrained mask oracle.
- **Old-task retention check:** Try the singleton branch in the co-retiring version. It must be refused (or proved legal by a different installed set) without removing the other spare's live contribution.

#### 09. One bridge across several survivor pools
- **Mechanism:** Give an address a small number of predeclared global survivor domains whose legal update spaces differ. Compile a common signed set for all of them; the request names a lawful domain, and only that domain may absorb the removed payload. Retirements cannot change domain ownership.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [ZipIt!](https://arxiv.org/abs/2305.03053) aligns and merges redundant features. The proposed object is one neutral preparation whose distinct, permission-checked retirements work across different survivor spaces, rather than one merged model.
- **Cheapest first test:** Exhaust tiny two-domain integer heads with intersecting but unequal survivor spaces. Compare one common registration with independent per-domain bridges at equal spares and exact domain-aware repair.
- **Old-task retention check:** On each accepted branch verify every domain, including one where a numerically available survivor is not authorized to receive the payload.

#### 10. Prefix-safe retirement without assuming atomicity
- **Mechanism:** For a nonatomic editor, compile correction sets whose advertised branches have at least one safe micro-order; search only over authorized retirements and declared survivor writes. An unmasked intermediate head is part of the contract, not ignored as an implementation detail.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Net2Net](https://arxiv.org/abs/1511.05641) concerns equivalent endpoints; this adds a scheduling constraint to the bridge. The parent #208's prefix bounds and a paid atomic publish are controls, not new mechanisms.
- **Cheapest first test:** Enumerate all micro-orders of a small join, with and without a fixed-width shadow bank priced as storage. Include a W3 endpoint whose first visible retirement necessarily alters the protected head without atomicity.
- **Old-task retention check:** Read A/C after every visible microstep or refusal. Endpoint equality is not a pass for a failing prefix.

#### 11. Pack for a partly occupied spare bank
- **Mechanism:** A descriptor names which local units are actually idle and which spare units are pinned by new readers. Compile using only the idle units; favor a set that still offers several choices if a pinned block cannot retire.
- **Novelty vs nearest prior art — IMPROVEMENT:** [PackNet](https://arxiv.org/abs/1711.05769) allocates parameters by iterative pruning. This is a stricter allocation test for neutral preparation under real occupancy, not a claim to invent pruning or free hidden width.
- **Cheapest first test:** Feed the same stream to an empty-bank compiler, an occupancy-aware compiler and exact local repair; give them the same width and inject arrivals for immediate use of scarce spares.
- **Old-task retention check:** Preserve tasks already using pinned units and verify any missed new write is recorded as a capacity trade-off, not silently dropped from C once accepted.

### Learn only what the public description can support

#### 12. Train on neutral solves, with partner labels hidden
- **Mechanism:** Generate target signed sets by solving generic interface obligations on disjoint training banks. Distill classes of equivalent sets, rather than one solver's arbitrary ordering, and let a deployed compiler see only the fresh descriptor.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Amortized optimization](https://arxiv.org/abs/2202.00665) learns to replace repeated solves. This is an amortization test; any edge from solver labels or cached traces counts against it.
- **Cheapest first test:** Compare exact solver time, cold compiler plus verifier, and warmed exact solver at equal total budgets over a short stream. Include a cheap exact-solve regime where compiling should lose.
- **Old-task retention check:** Keep training and deployment banks disjoint, then check every old reader on both an accepted unseen signature and a solver-dependent failure.

#### 13. Certify the branch, not the descriptor confidence
- **Mechanism:** When one description could hide multiple readers, retain only branches proved valid for every allowed reader, or buy a public probe before registration. Refuse if the ambiguity affects the neutral registration itself.
- **Novelty vs nearest prior art — IMPROVEMENT:** [APRNN](https://arxiv.org/abs/2304.03496) provides verification-backed neural repair. This uses a verification budget for selective service from a common prepared state, not a new repair algorithm.
- **Cheapest first test:** Construct two indistinguishable readers for which one signature is safe in both and another is not. Compare branch-wise certification, always-refuse and query-then-exact-repair at equal probe costs.
- **Old-task retention check:** Use the hidden reader that defeats the ambiguous branch as a protected C task; verify the shared branch in both worlds and test the refused branch leaves state unchanged.

#### 14. Make the shuffle a matched physical twin
- **Mechanism:** Permute public descriptors across physical banks with the same dimension, spare count and degree profile while stripping IDs. Preserve the legal graph for the informed controls. Also run a pure relabel that transports both reader and description together, which should not harm a genuine compiler.
- **Novelty vs nearest prior art — AUDIT:** [Learned indexes](https://arxiv.org/abs/1712.01208) rely on exploitable structure. This separates loss of descriptor information from loss of physical joinability, unlike a shuffle that asks a table to perform impossible edits.
- **Cheapest first test:** Generate matched pairs of fresh banks with W3-type vocabularies and run aligned, transported and scrambled assignments. Hold repair effort fixed before evaluating optional paid recovery.
- **Old-task retention check:** Measure false publications on both twins; all invalid predicted masks must be rejected without changing A/C.

#### 15. Prove a family once, audit its instances cheaply
- **Mechanism:** Factor certification into a global rule for a descriptor grammar and instance checks on unit bounds, residual equality and current permissions. Derive branch checks from the grammar; do not persist a separate proof per edge.
- **Novelty vs nearest prior art — IMPROVEMENT:** [APRNN](https://arxiv.org/abs/2304.03496) gives a verified repair baseline. Reusing a proof is ordinary specialization; the concrete claim is that the family proof amortizes legality across *unseen* branches without recovering the menu as stored proof bytes.
- **Cheapest first test:** Build a finite grammar for small blockwise integer heads and compare proof sizes and checking work against exact repair plus proof caching. Test an out-of-grammar address.
- **Old-task retention check:** Exhaust all protected inputs in the tiny grammar, including the boundary where a proof premise fails but sampled outputs would pass.

#### 16. Publish against exact finite-precision semantics
- **Mechanism:** Compile signed terms on the deployed integer grid, constrain reduction and saturation, and certify the exact executed registration and retired sums. Use the same accumulator budget as the uncompiled controls.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Integer-only quantization](https://arxiv.org/abs/1712.05877) supplies the arithmetic. Here the feasible object is a family of exactly neutral retirements under that arithmetic, not quantization itself.
- **Cheapest first test:** Sweep an 8-bit W3 head around saturation edges. Compare integer compilation, rounded real compilation and exact integer repair. Include two masks with the same real sum but different executed saturation behavior.
- **Old-task retention check:** Compare bit-exact A/C outputs at boundary inputs under registration, every allowed retirement mask and the filled-slot state.

### Seek a benefit that survives actual use

#### 17. Price late choice against a shared opening
- **Mechanism:** Keep the address registered while an independent new payload arrives; commit one retirement only after learning which old address the payload really needs. Use a short deadline to price a precompiled choice against a new install.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [#198 card 05](joint-releases.md) prepares an opening that has several finishes; [Text-to-LoRA](https://arxiv.org/abs/2506.06105) maps a description to weights. Their stack ties unless one unseen-description installation, without naming branches, makes an otherwise unavailable lawful finish on time.
- **Cheapest first test:** Cross fresh address seen/unseen with partner demand known/delayed. Compare to a paid preopened menu and exact online repair; score useful service within a fixed deadline, not number of installed options.
- **Old-task retention check:** Keep the payload producer's existing service and A/C live while waiting, on refusal and after consuming either branch.

#### 18. Train for the second request without promising two joins
- **Mechanism:** Select among equally lawful masks for the first request by minimizing obligations left in retained spares that block the *next* write. This does not leave the original bridge live or permit a second join from its pre-consumption state.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Continual LoRA](https://arxiv.org/abs/2502.17920) reuses limited adaptation capacity. Here the specific scheduling advantage would come from interchangeable masks with different post-consumption occupancy, not from adapter reuse itself.
- **Cheapest first test:** Use two equal-sum masks on spares of unequal downstream value. Compare request-oblivious tie-breaking, shortest mask, and exact two-request lookahead over the same feasible set.
- **Old-task retention check:** Verify every accepted task after both requests, especially C tasks served by spare units kept after the first release.

#### 19. Move the proof across a new live reader
- **Mechanism:** When a newly accepted task adds an observation, keep the installed weights frozen. Revalidate only those retirement choices that could change the observation; stop advertising others. Derive that scope from public feature support, not saved partner IDs.
- **Novelty vs nearest prior art — IMPROVEMENT:** Parent #218 card 16 invalidates stale registrations. [APRNN](https://arxiv.org/abs/2304.03496) provides a recertification baseline. The narrower bet is that one branch can remain certified even when another branch of the same address becomes unsafe.
- **Cheapest first test:** Add a reader that observes the `u` spare directly but not the `v` spare in W3. Compare incremental checks to whole-address invalidation and full re-verification.
- **Old-task retention check:** Exercise the new reader and original A/C on every surviving branch; a branch that removes the observed spare must be refused if its obligation cannot be discharged.

#### 20. Reserve robust choices for jointly stressed banks
- **Mechanism:** Optimize the signed set against a small public family of survivor load levels. Two masks can cancel the same quotient residual while leaving different survivor updates: e.g. keep `u+x₁` or `u−x₁`, so the survivor needs `p+q−x₁` or `p+q+x₁`. Compile for choices that fit the actual headroom without a local rewrite.
- **Novelty vs nearest prior art — IMPROVEMENT:** [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147) accommodates different representation budgets. This is a budget-conditioned service check for fixed physical coefficients, not an assertion that a prefix representation ensures retention.
- **Cheapest first test:** Reduce global survivor headroom after registration, giving each baseline the same legitimate intervening writes. Compare robust and nominal compilers against exact bounded repair at equal new-task success.
- **Old-task retention check:** Test tasks that caused the load change along with the original ones; when insufficient global range remains, a failed join must leave both task sets intact.

#### 21. Account for the whole menu in bytes and probes
- **Mechanism:** Compare a zero-edge compiler to an informed compressed table plus exact repair on the full cost frontier. Block access to IDs during compilation; count descriptor probes, missed requests, all persistent metadata, and transient decode work separately.
- **Novelty vs nearest prior art — AUDIT:** [Learned indexes](https://arxiv.org/abs/1712.01208) already trade description structure for lookup cost. A win here must buy a lawful new write that table lookup plus repair cannot match at the same budget; compression alone is not the result.
- **Cheapest first test:** Sweep from structured to permuted descriptors and vary menu width at fixed degree per old address where possible. Compare exact release rates versus bytes at fixed probe/time budgets; include the cheap-table regime.
- **Old-task retention check:** Check A/C on equal-budget table and compiler runs, including a table entry that names a real edge but cannot legally release under the current capacity.

#### 22. Make nonlinear branch choice genuinely necessary
- **Mechanism:** Learn signed terms represented by small piecewise-linear units and require one mask to cancel a requested residual on *every* protected cell. A branch may exploit a cell-spanning functional identity, but cannot select a different mask for each probe or alter the runtime inference graph.
- **Novelty vs nearest prior art — PRIMITIVE CANDIDATE:** [APRNN](https://arxiv.org/abs/2304.03496) repairs networks under piecewise-linear specifications. The proposed operation amortizes a single neutral preparation over several fixed interference patterns; a separate cell repair per request is the tying control.
- **Cheapest first test:** Enumerate cells of a scalar ReLU head with two independent hinges and one decoy narrow hinge. Compare shared nonlinear preparation to exact joint cell repair and a linear-quotient compiler at equal width and proof cost.
- **Old-task retention check:** Verify every cell, boundaries and the hidden hinge after registration and after both useful slot reuses. Interpolation on sampled old inputs is not enough.

## Ranked deeper questions

1. **Does a frozen registration buy distinct, usable choices under actual edit locality?** Start with W3 and cards 01, 07, 08 and 17. Demand two distinct residual classes from the same registered state, one actual join per fork, real writes to both released slots, and better cost/service than the stacked local controls. If selective retirement is unavailable, stop at the fixed-footprint impossibility. If open donation ties under the relevant permissions, do not claim a primitive there.
2. **How much of the option menu comes from the description rather than hidden side information or exact repair?** Use cards 12–15 and 21 on wholly unseen address banks. Require a gap over the blind prior that disappears in the matched shuffle, inspect the decoy refusal curve, and include the informed byte-matched table. Report the point at which probing or residual entropy makes the compiler lose.
3. **What sets the useful frontier: spares, mask restrictions, or verification?** Use cards 02, 04–06, 10 and 16. Separate independent rank, actual bounded subset coverage, intermediate-state legality, decoder cost and certifier cost. Compare to exact tiny-world optima and a partner family requiring strictly more than `k` independent spares.
4. **Does flexibility survive ongoing service rather than a hand-picked join?** Use cards 09, 11 and 18–20, then card 22 if linear worlds survive. Add real readers and competing writes between registration and request. Score new-task service, refusals and spare opportunity cost without giving back any old capability.

**Verdict:** The narrow primitive candidate is a description-compiled, neutral edit with several selectable release footprints, not a hypernetwork plus a list of partners. W3 rules out distinct additive signatures under a fixed footprint. Under elective retirement it shows what to test, not that the learned compiler wins. Keep the claim only if lawful, held-out service beats the single-partner/shared-opening/table-plus-repair stack at equal full cost, with A/C intact and the W2 shuffle breaking the compiler advantage.
