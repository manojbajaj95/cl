# Self-closing witnesses: certify the states your replacement creates

**Status:** Ideas only; no experiments, probe code, or GPU work. **Parent:** [Witness examples](witness-examples.md) ([PR #163](https://github.com/manojbajaj95/cl/pull/163)), cards 2 and 20. **Review seed:** [Flood triage row 261](https://github.com/manojbajaj95/cl/blob/ca1b7ced397ff87da9a10d6d67234f4273c4780d/reviews/flood-triage.md#L261), two score-3 directions: fit a buffer against disagreements on both source- and replacement-reachable states, then freeze it; buy today's examples where they eliminate the most expensive future corrections.

## Is a memory that certifies its own coverage region a new primitive?

**Not yet.** Learning a compact surrogate, searching its own rollouts for mistakes, and proving forward invariance are known operations. The candidate primitive is a **frozen memory plus an independently checkable training-substitution contract for a region induced by that very memory**. It must establish both that the declared continuations stay inside the checked region and that the buffer agrees with the source there within a predeclared tolerance. “Self” means this buffer induces the dynamics to be checked; it does not mean the buffer gets to grade itself. It becomes a primitive if the contract enables useful operations such as composing or transporting certified replacements, or trading teaching data for certified bytes, that the best stack of condensation, counterexample search, verification and exact retirement cannot match at equal cost. If the stack finds the same useful releases, the buffer is an improvement in how those tools are used, not a new primitive.

### What freezes, and what the certificate means

Fix the comparison start, permitted batch orders, horizon, update code, numeric semantics, randomness and tolerances before fitting. State includes weights, trainable and frozen model state, optimizer slots, clocks, and sampler state where they affect the future. For every candidate buffer, search legal source **and** replacement rollouts for a state where applying both updates on that same state and legal next batch disagrees (direction is a good search heuristic; verify full next-state error). Search also for a successor the proposed region omits. Add the failure, refit, and repeat. Search the *new* replacement after every fit: the old replacement's paths are not its reachability set. Freeze the exact buffer, sampling rule and contract only after an exhaustive or sound check; “no counterexample found” in a budgeted search gives an empirical result, not a certificate. If validation is inconclusive, keep the source. Bind the result to the frozen artifacts and versions; no post-cut repair using the old source.

For a finite horizon a certificate can be a sequence of sets `R₀,…,R_H`, indexed by legal batch-prefix state when needed. `R₀` contains the initial states. At each step both transitions must send `R_t` to the appropriate `R_{t+1}`, and their same-state discrepancy on `R_t` must be at most `ε_t`. Under the same admitted external input sequence, if the source map is `L_t`-Lipschitz on the compared pairs, the coupled rollout error obeys `d_{t+1} ≤ L_t d_t + ε_t` by the triangle inequality. An alternative is to check an inductive *paired* relation directly, without a global Lipschitz assumption. For adaptive batch choice or sampling, the contract must model the joint state and allowed input coupling; identical seeds alone do not guarantee identical batches. Exact match from the same start gives identical trajectories by induction. Approximate agreement need not preserve labels near a boundary, and faithful replication need not preserve old tasks if the source itself forgets.

**First construction, on paper:** Use a two-unit ReLU learner with a normal B update near one gate and a legal continuation that approaches it twice. Arrange a slightly biased witness correction so the source stays on one side but the witness steps across, changing the next gradient. Select the example and required post-cut retention floor independently of that failure branch; first establish the live source actually protects A there. Enumerate the resulting finite tree as ground truth for the toy. Use a linear restricted-Fisher case as a negative novelty control: exact quadratic factorization should suffice there. Do not extrapolate an exhaustive result for a finite toy to a continuous neighborhood or longer horizon.

**What to price:** For a fixed truthful subset `D` of today's examples, define `m(D)` as the minimum total persisted bytes of a verified replacement in the common grammar, or infinity if none is verified. Every legal branch needs either a checked replacement or a separately justified read-free refresh; learning more on easy branches does not excuse losing a hard one. Optimize over `D` under the same example quota and over replacements under the same peak allocation cap. A candidate interaction is a truthfully taught branch that removes a costly witness obligation, or changes the remaining branches' reachable sets enough that a *shared* buffer becomes cheaper. Measure the marginal cost with and without the paired data decision. A planted cap can check the accounting, but evidence requires the byte change to come from learned nonlinear trajectories, not a surcharge hard-coded on one branch.

### Closest prior art and common controls

- **Small data with training effects:** [Gradient matching](https://arxiv.org/abs/2006.05929), [MTT](https://arxiv.org/abs/2203.11932), [GCR gradient coresets](https://arxiv.org/abs/2111.11210) and [trajectory-error minimization](https://arxiv.org/abs/2211.11004) already match gradients or training paths, including attention to error accumulation. [HAL](https://arxiv.org/abs/2002.08165) learns anchors against simulated interference; [FRCL](https://arxiv.org/abs/1901.11356) and [FROMP](https://proceedings.neurips.cc/paper_files/paper/2020/file/2f3bbb9730639e9ea48f309d9a79ff01-Paper.pdf) constrain old functions. Compare branch-matched MTT with the **same** both-arm search, verifier, source queries and retirement planner, and equal-byte HAL/FROMP, raw replay and low-rank Fisher. Include a non-example surrogate where useful. Do not compare a verified proposal to an unverified baseline.
- **Self-induced states, fixed points, and certificates:** [DAgger](https://arxiv.org/abs/1011.0686) already asks the expert to label learner-induced states. [Counterexample-guided neural repair](https://arxiv.org/abs/2301.11342) already couples verification to refitting; [forward invariance of neural dynamics](https://arxiv.org/abs/2210.04763) and [interval bound propagation](https://arxiv.org/abs/1810.12715) supply ingredients for checking sets. [Certified CL for regression](https://arxiv.org/abs/2407.06697) and [certified behavioral retention with held-out anchors](https://arxiv.org/abs/2610.40740) are stronger novelty neighbors than unverified replay. None of these distinctions alone clears novelty: the claim is about a checked substitution for a resource that can actually be removed, with a region dependent on the substitute. The literature screen is provisional.
- **Buying future changes now:** Compare [MIR](https://arxiv.org/abs/1908.04742), HAL-style look-ahead, direct bilevel selection, and the [data-only edit cost](data-only-edit-cost.md) and [future-edit cost](future-edit-cost.md) nodes. In the data-only arm select only from today's truthful labeled pool; match examples, acquisition effort, initial per-item margins and B progress or report no feasible match. The future optimizer, batches and schedule are fixed; a branch declared read-free runs with neither teacher nor buffer. Establish that the teacher rescues the default selector under that schedule. When combining teaching with witnesses, beat both solo arms, their strongest independently tuned stack, and compare to exhaustive joint search over the same grammar as a ceiling, not a weaker baseline.
- **Ledger and accounting:** The [idea ledger](https://github.com/manojbajaj95/cl/blob/ca1b7ced397ff87da9a10d6d67234f4273c4780d/reviews/idea-ledger.md) rules out credit for the identity of the example generator, warns against assuming sparse damage, and requires stacked ideas to beat stacked parts. Start with exhaustive finite CPU toys, then a tiny nonlinear CPU learner. Put ordinary old tasks A/C on independent data never used for fitting or calibration, score separately against acquisition and pre-cut references at all visible prefixes and after reuse, and report rare slices and refusals. Any certificate tied to a finite family has that family defined before fitting; hold out whole sequence families/orders for independent behavioral tests, not adjacent checkpoints. A finite enumeration may inspect all declared branches for the proof; report that cost rather than claiming those branches were blind. Keep the evaluation oracle physically separate. After draining old reads, block all aliases and overwrite the source with useful B state. Count persistent and peak bytes, including region/proof, sampler, routing, overlap, validation and any retained source summary; count build/source-query and runtime compute separately. Charge refusals and report B progress under the same scope. **P** = conditional primitive candidate; **I** = improvement or audit.

## Idea cards

### Make closure depend on the buffer

#### 1. Follow the replacement across a gate (I)
- **Mechanism:** On each refit, recompute successor prefixes from both arms and fit on the earliest new counterexample, including source queries from replacement-only states.
- **Novelty vs nearest prior art:** DAgger plus counterexample-guided repair already does the essential aggregation. This is the necessary baseline, not an invention.
- **Cheapest first test:** Exhaust short batch orders in the two-unit ReLU construction. Compare source-only MTT, branch-matched MTT with the same search, HAL and FROMP at equal bytes. Detect whether the first crossing disappears or just moves a step later.
- **Old-task retention check:** Measure normal A/C immediately before and after crossing and at the final refresh on independently chosen orders, after source overwrite.

#### 2. Stop refits from resurrecting retired paths (I)
- **Mechanism:** Retain counterexamples by legal prefix, not just by weight snapshot. Try preserving old constraints while re-solving the new reachable tree; compare archiving versus dropping demonstrably irrelevant prefixes.
- **Novelty vs nearest prior art:** A counterexample archive is standard CEGIS. The specific question is whether proof invalidation or indefinite archive growth is the practical bottleneck for compiling examples.
- **Cheapest first test:** Use a two-gate learner where fixing one crossing can reopen the other. Enumerate a quantized buffer grammar; record actual fit cycles and certificate size versus replay of only the latest failure and exact search.
- **Old-task retention check:** After the final freeze, rerun ordinary A/C on prefixes that previously reopened as well as untouched orders; being absent in the last failed buffer is not evidence of safety.

#### 3. Search for damage, not for the largest gradient angle (I)
- **Mechanism:** Order reachable counterexamples by a downstream retention proxy times error size; still prove all in-scope error and successor obligations after fitting. Use independent proxy anchors, not evaluation A/C.
- **Novelty vs nearest prior art:** MIR ranks interference, and trajectory-error methods already weight accumulation. This is a search-efficiency change, not a new certificate.
- **Cheapest first test:** Construct two legal divergences, a large benign one and a small gate-crossing one. At equal queries compare angular, next-state norm and downstream-prioritized search against exhaustive ordering.
- **Old-task retention check:** On ordinary A/C, compare first harmful prefix and worst prefix after reuse; discordant proxy rankings must not be scored as coverage wins.

#### 4. Certify pairs instead of a cloud of weights (P)
- **Mechanism:** Store a relation between source and witness states for each legal progress stage, preserving shared coordinates symbolically and bounding the ones that drift. Discharge the source side before retirement; no paired source rollout runs afterward.
- **Novelty vs nearest prior art:** Relational verification and simulation relations already do the mathematics. The candidate object is a reusable replacement contract when a single-state tube overapproximates impossible combinations enough to block release.
- **Cheapest first test:** Enumerate a two-layer learner with a shared B clock and crossed activation regions. Compare a paired polytope to equal-cost separate tubes, both with the same CEGIS/MTT fit and a finite exact checker.
- **Old-task retention check:** After reuse, score A/C on ordinary orders that approach both gates; the paired proof must admit the actual B schedule rather than erase difficult states.

#### 5. Keep the grammar fixed when correction really cannot fit (I)
- **Mechanism:** For a fixed quantized example grammar, collect legal obligations whose feasible sets have empty intersection. Emit an infeasibility result for that grammar rather than silently switching to a routed buffer.
- **Novelty vs nearest prior art:** Unsatisfiable cores and the parent's expressiveness check are known; this separates inability to fit from inability to find a good candidate.
- **Cheapest first test:** Build two legal gate branches needing conflicting labels at the only allowed witness location. Exhaust one-slot versus two-slot candidates, and compare with a priced state-conditional lookup.
- **Old-task retention check:** Check A/C on both branches with live source, each failed release and a feasible control. Report grammar infeasibility separately from any harmless update mismatch.

#### 6. Verify a distribution without throwing out rare rollouts (P)
- **Mechanism:** Issue a stochastic contract with a declared coupling, a finite-horizon upper bound on bad-prefix probability, and an explicit rare branch that must pass deterministically. Price the sampler state and witness weights.
- **Novelty vs nearest prior art:** Probabilistic model checking and stochastic trajectory matching supply the tools. The possible new operation is retirement under a stated risk budget without pretending expected gradients imply safety.
- **Cheapest first test:** Enumerate every draw of a small replay sampler with equal mean updates but different tail transitions; compare exact probabilistic checking plus ordinary MTT, mean matching and deterministic worst-case closure.
- **Old-task retention check:** Measure ordinary A/C on each rare class plus the probability of any floor breach, not just final mean accuracy.

### Turn the region into something another learner can use

#### 7. Fence off an unsafe loop without shrinking the advertised job (P)
- **Mechanism:** Compile a proof indexed by batch-order automaton state; admit a prefix based on what's already consumed, not a single box that treats every next batch as always legal.
- **Novelty vs nearest prior art:** Trace partitioning and [finite safe regions (PR #152)](https://github.com/manojbajaj95/cl/pull/152) already support scoped verification. The candidate gain is a smaller frozen substitute for the very same sequence language, not fewer admitted B jobs.
- **Cheapest first test:** Use one toggle batch followed by one correction batch, with a third legal interleaving. Compare mode-indexed regions with interval bounds and per-order certificates, charging the automaton.
- **Old-task retention check:** Verify ordinary A/C on every legal order and test a recognizably illegal loop separately as refusal, never as a retention success.

#### 8. Publish the drift budget per prefix (P)
- **Mechanism:** Pair the witness with a frontier of remaining error budgets. Sum additive errors on contracting segments and enforce tighter local bounds immediately before expansive segments; reserve downstream slack rather than treating every step equally.
- **Novelty vs nearest prior art:** Accumulated-error distillation and Lyapunov analysis already weight propagation. The candidate operation is sharing a checkable residual budget with a later consumer that did not fit the buffer.
- **Cheapest first test:** Alternate contracting and expanding updates in a tiny nonlinear system. Give a separately fixed second job the remaining budget; compare uniform error bounds and the best stacked trajectory fitter plus exact paired verifier.
- **Old-task retention check:** Report worst-prefix and final A/C for both orderings, including equal total local error placed on opposite sides of the expansive step.

#### 9. Prove the execution precision, not the fit precision (I)
- **Mechanism:** Fit in float if helpful, but freeze quantized examples and certify under the actual rounding and sampling rules; account for cells where ties can change gate decisions.
- **Novelty vs nearest prior art:** Quantized-network verification is established. This audit stops unpriced precision from becoming hidden witness memory.
- **Cheapest first test:** Put a two-unit model near a rounding boundary and exhaust tiny legal continuations at two precisions. Compare verify-after-quantizing, quantization-aware fitting and a same-byte quantized anchor.
- **Old-task retention check:** Run ordinary A/C after reuse at deployed precision; flag any float-only pass separately.

#### 10. Carry a certificate across optimizer clocks (P)
- **Mechanism:** Prove a mapping between allowed slot/clock states that preserves the relevant paired transition relation; transport the frozen buffer only when this map checks, without source queries after the cut.
- **Novelty vs nearest prior art:** Optimizer-state transfer and MTT already model slots. The conditional operation is offline transport of checked coverage, not matching a first normalized step.
- **Cheapest first test:** Use a tiny Adam learner with equal weights at two clocks, one candidate mapping under equivalent bias correction and one invalid reset. Compare recertifying each clock pre-cut and joint trajectory fitting with the same verifier.
- **Old-task retention check:** Check A/C after the second and later steps where moment errors appear, plus the original clock regime; reject the reset if it is not covered.

#### 11. Compose contracts through the mixed region (P)
- **Mechanism:** Use a relational compatibility check on the *joint* trajectories of two frozen buffers; discover whether one buffer exposes a gate region never visited under either substitution alone.
- **Novelty vs nearest prior art:** Assume-guarantee interfaces such as [Pacti](https://arxiv.org/abs/2303.17751) and joint condensation are the nearest combination. Value requires reuse of local checked artifacts to make joint release cheaper than checking and refitting from scratch.
- **Cheapest first test:** Enumerate two substitutions individually below a gate threshold but jointly above it. Compare naively composing receipts, exact joint verification, and joint MTT with the same verifier.
- **Old-task retention check:** Score normal A/C with neither, either, and both replacements after reuse; require the refuser to identify the first unsafe mixed prefix without grading it as success.

#### 12. Keep an independently checkable source summary (I)
- **Mechanism:** Before erasure, convert the relevant source bounds to a small proof transcript tied to the source version, and retain just what an independent checker needs to audit a historical certificate. Disallow using the transcript as a corrective lookup.
- **Novelty vs nearest prior art:** Proof-carrying code and functional summaries already separate proving from checking. The question is whether the audited proof is genuinely smaller than a useful substitute for the source.
- **Cheapest first test:** Serialize facts for a finite quantized ReLU tree and compare a checker transcript, a complete teacher-response table, and a pinned verifier's signed result; disclose the different trust assumptions.
- **Old-task retention check:** Run ordinary A/C with only authorized runtime bytes after overwrite; use a deliberately wrong transcript to test checker rejection, not to score retention.

### Spend today's examples where they buy tomorrow's bytes

#### 13. Remove the priciest branch, not the most frequent one (P)
- **Mechanism:** Choose from today's truthful examples to remove a branch's teacher correction requirement, then compile only the remaining obligations. Estimate the price by how much smaller the **joint** buffer becomes when that branch goes read-free.
- **Novelty vs nearest prior art:** HAL-style anticipation plus MTT already provides the parts. A win requires an allocation breakpoint one purchase crosses only because the other changes cost, not a sum of two small gains.
- **Cheapest first test:** Exhaust equal-size subsets and buffer grammars in a two-branch nonlinear toy with a hard overlap cap. Compare both solo arms, independently tuned look-ahead plus verified MTT, and the same-grammar joint optimum; also test a cap just above the claimed breakpoint.
- **Old-task retention check:** Demonstrate teacher necessity for the default subset; after overwrite, score A/C separately on data-only and buffer-backed branches while both deliver matched B progress.

#### 14. Buy a common return corridor (P)
- **Mechanism:** Choose examples that make two distinct B branches later reenter a shared region where one tiny buffer suffices. Do not erase earlier correction needs; certify the approach and the return.
- **Novelty vs nearest prior art:** [MER](https://arxiv.org/abs/1810.11910) and look-ahead selection improve joint trajectories; MTT can train one shared buffer. The proposed interaction is shrinking certified bytes by changing the geometry shared across branches, as opposed to reducing either isolated loss.
- **Cheapest first test:** Use two legal orders with a shared bottleneck after a separating labeled example. Measure shared versus separate buffer sizes and compare exact return-aware search with direct post-refresh bilevel selection stacked with joint MTT.
- **Old-task retention check:** Score A/C on each branch before the merge point as well as after it; a temporary old-task failure cannot be hidden by return to the common region.

#### 15. Spend one example on the proof, not on the correction (P)
- **Mechanism:** Select a current example that pushes competing starts away from an uncertain gate, leaving approximately the same witness update and empirical retention but reducing the size of its proof.
- **Novelty vs nearest prior art:** Certified training with interval bounds already optimizes provability. The claim is a trade of current data for future proof bytes at otherwise matched witness size and job scope.
- **Cheapest first test:** Pick equal-count subsets for a two-gate model where only one simplifies the activation partition. Control for margins, proof grammar and verifier; compare ordinary certified look-ahead selection followed by MTT.
- **Old-task retention check:** Compare ordinary A/C after reuse on both near- and far-gate legal orders. Treat equality in accuracy without actual reclaimed B capacity as no win.

#### 16. Price branch liabilities that overlap (I)
- **Mechanism:** Measure residual buffer size after eliminating each subset of reads; use these marginal costs rather than assigning a disjoint byte price to every branch.
- **Novelty vs nearest prior art:** Set-cover accounting and the parent's last-reader question already explain why individual prices mislead. This bounds the benefit of a proposed selector, not a new learning rule.
- **Cheapest first test:** Enumerate three branches where two share a witness example and only removing both frees its bytes. Compare singleton ranking, pairwise pricing and the exact allocation frontier at the same teaching quota.
- **Old-task retention check:** Check normal A/C on each remaining and read-free branch, holding B exposure fixed even if a subset makes a branch cheap.

#### 17. Teach away the worst authorized surprise (P)
- **Mechanism:** Precommit a family of possible B objectives independently of today's selector; spend examples to lower the worst certified residual buffer cost across that family rather than expected teacher-free loss.
- **Novelty vs nearest prior art:** Robust bilevel selection and [Premonition](https://arxiv.org/abs/2403.07356) anticipate shifts; the additional claim is a lower maximum *checked memory liability* without vetoing a legal surprise.
- **Cheapest first test:** Let a blind evaluator choose between two predeclared nuisance reversals after commitment. Compare expected and worst-case look-ahead stacked with verified MTT and a live teacher. Use equal worst-case as well as average query budgets.
- **Old-task retention check:** Check ordinary A/C after both reversals, including the rarely chosen one; require matched progress on the surprise objective itself.

#### 18. Spend fewer bytes now, only if they arrive in time (I)
- **Mechanism:** Compare option curves for immediate and later swaps; a data purchase that reduces persistent witness bytes but requires source/buffer overlap beyond the cap is infeasible.
- **Novelty vs nearest prior art:** Exact retirement planning and the parent's break-even audit already handle lifetimes. This catches a joint selector that wins only in steady-state accounting.
- **Cheapest first test:** Enumerate two acquisition windows and three usable allocation sizes. Compare steady-state ranking with exact peak-aware scheduling, and count whether B can place its first real write on time.
- **Old-task retention check:** Score A/C before drain, during any intermediate refresh and after B reuse; postponing a promised refresh is a refusal.

### Try to break the proposed primitive

#### 19. Distinguish universal coverage from a favorable random seed (I)
- **Mechanism:** Pair a small exhaustive distribution with blind empirical rollouts to measure how many replacement-only paths a budgeted search misses; label convergence without a proof empirical.
- **Novelty vs nearest prior art:** Falsification versus verification is a standard distinction. The audit prevents a DAgger-style stopping rule from being advertised as a certificate.
- **Cheapest first test:** Plant a legal three-batch sequence that is rare under the fit sampler but easy to enumerate. Compare random, coverage-guided and exact checking with equal rollout budgets where possible.
- **Old-task retention check:** Report normal A/C for the planted sequence and independent ordinary orders after overwrite, separating empirical misses from actual in-scope proof errors.

#### 20. Extend the horizon without resurrecting the teacher (P)
- **Mechanism:** Seal a finite tube with a proved entry into an invariant paired tail relation that itself enforces the rollout error bound. Local discrepancies alone could accumulate without limit. Admit longer runs only while the tail assumptions remain valid.
- **Novelty vs nearest prior art:** Inductive invariance and bounded model checking already separate finite prefixes from unbounded tails. A candidate operation is cheap extension of a certified replacement, without renewing its source access.
- **Cheapest first test:** Engineer a stable small basin after a nonlinear transient and a sibling toy with slow drift back out. Compare a tail-invariant proof to unrolling and repeated finite MTT certification with the same checker and fit access.
- **Old-task retention check:** Check ordinary A/C well beyond the original horizon in both toys; the drifting toy must not be counted as admitted merely because first-horizon retention passed.

#### 21. Let the source fail independently (I)
- **Mechanism:** Separate three outcomes: source and witness both retain, both forget, or disagree. Require an independent retention gate in addition to transition fidelity; a candidate that improves on the source but fails equivalence is a different claim.
- **Novelty vs nearest prior art:** Certified CL and functional replay already distinguish old behavior from parameter fidelity. The audit prevents “same update” from being substituted for preserving skill.
- **Cheapest first test:** Use a stale EWC anchor that does not protect a rare old slice next to a competent teacher. Compare exact substitution, no-source refresh and an independently validated retention method.
- **Old-task retention check:** Measure old A and C individually, with rare-slice results, against acquisition and pre-cut scores; don't infer retention from teacher agreement.

#### 22. Compile away the novel interface (I)
- **Mechanism:** Give a conventional solver the identical buffer grammar, legal starts, branch search, proof language, joint teaching options and exact release scheduler. Ask whether ordinary fitting and checking can reconstruct every claimed benefit without exposing a new interface.
- **Novelty vs nearest prior art:** This is the strongest-stack control required by the ledger: MTT/gradient matching, counterexample repair, verification and exact retirement, not a weaker replay-only straw man.
- **Cheapest first test:** Exhaust the small linear, ReLU crossing and example/byte breakpoint toys. Compare admitted jobs, source queries, proof size, time and net reusable bytes; then test one frozen receipt with an independently specified consumer.
- **Old-task retention check:** Require the same ordinary A/C floors at every visible post-cut prefix and matching B progress in both arms. A tie at matched scope means no new primitive demonstrated.

## Ranked deeper questions

1. **Can a useful witness certify the nonlinear states it creates before the source is erased, at less total cost than keeping or conventionally replacing the source?** Start with the gate-crossing toy (cards 1–5), a linear null case, and real overwrite. Give branch-matched MTT the exact same counterexample search and verifier; compare HAL and equal-byte FROMP. The first win is more admitted learning with independent A/C retention at matched B progress, not merely finding a replacement-only state.
2. **When does a truthful example today remove enough joint correction or proof liability to cross a real byte cap tomorrow?** Use cards 13–18. Look for a breakpoint that independently tuned look-ahead plus verified MTT misses and the exhaustive same-grammar joint solver predicts. Check both sides of the cap, source necessity, peak overlap and both branches' post-cut retention.
3. **Which proof form is both sound and cheap enough to carry?** Compare full trajectories, single-state tubes, paired relations and invariant tails (cards 4, 7–9 and 20). Seek a smallest counterexample to each and report a regime where the proof is more expensive than the source. Distinguish “no fit exists,” “the verifier cannot establish it,” and “a legitimate continuation fails.”
4. **Can a frozen contract do useful work for a second consumer without re-querying the source?** Try transport and joint closure (cards 10–12 and 22). Require an independently fixed consumer and a mixed-region failure control. If ordinary verification and planning recover the same releases at equal cost, keep the technique and drop the primitive claim.
