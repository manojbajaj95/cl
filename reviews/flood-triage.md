# Flood triage (novelty only)

Scores are novelty 1–5 from the reviewer's knowledge, with no prior-art search yet. Only the top 10 of the whole pool get prior-art checks. P = primitive, I = improvement. D = doable now, M = Moonshot.

## programs-weights ([PR #39](https://github.com/manojbajaj95/cl/pull/39), 38 ideas)

| Score | Idea | P/I | D/M | One line |
|---|---|---|---|---|
| 5 | P21 residual stream as a register machine (learned ISA of rank-1 ops; demos compiled into deltas) | P | D (toy) | A learned instruction set over the model's own weights, with skills produced by synthesis rather than gradient descent |
| 4 | P17 weight-space linker with symbol tables | P | D | Exported and imported residual directions resolved by relocations; composition by linking, not by routing or averaging |
| 4 | P19 stable ABI across base upgrades | P | D | Forward compatibility enforced as a training constraint during base upgrades |
| 4 | P27 circuit transplant with rejection dynamics | P | D | Rejection of a transplanted circuit under later training is a new measurable phenomenon |
| 4 | P1 skill compiler with a weight-space IR | P | D | An optimization pass between learning and deployment; depends on sparse ΔW dictionaries working |
| 4 | P6 decompile-recompile skills across model versions | P | D | Feature-level bytecode; risks overlap with Trans-LoRA / LoRA-X |
| 3 | P20 position-independent skill deltas | P | D | Depth-agnostic adapters make placement a deploy-time choice |
| 3 | P3 JIT specialization with deopt guards | P | D | The exact-fallback guard is the new piece |
| 3 | P9 effect types for agent lessons | P | D | Static conflict checking of lessons |
| 3 | P7 typed residual stream | P | D | Close to orthogonal-gradient projection |
| 3 | P8, P25 certified contracts / abstract interpretation of updates | I | D | Certified CL exists in part |
| 3 | P22 interpreted-then-compiled patches | I | D | GRACE-style codebook plus a promotion policy |
| 3 | P5, P24, P30, P33, P18, P23, P11 | I | D | Superoptimized deltas, closed-form partial evaluation, differential fuzzing, reachability GC, state-keyed loading, macro compilation, three-way merge: new framings of known operations |
| 2 | P2, P4, P10, P12–P16, P26, P28, P29, P31, P32, P34–P38 | I | D | Liveness ≈ PackNet/HAT; PGO placement; bisect/blame/COW are tooling; MoE, looped transformers, hypernetwork LoRA, abstention and self-editing agents cover the rest |

**Batch read:** strongest file so far on primitives. Six of its ideas introduce a new object (an ISA, symbols, an ABI, transplant rejection, an IR, bytecode). P21, P17 and P19 lead for the head-to-head.

## merged-ideas proposer ([PR #36](https://github.com/manojbajaj95/cl/pull/36): flood batches 1–2, 70 ideas; merged batch 2, 9 cards)

These are mostly recombinations of ledger artifacts (margin, follow index, entropy, N1 masks). As a pool they are the least novel so far: nearly all are IMPROVEMENT, and none scores above 3.

| Score | Ideas | P/I | One line |
|---|---|---|---|
| 3 | MZ3 / B1-3 trainable trust dial | P | Overridability becomes a per-memory learned variable |
| 3 | B2-9 lesson as a per-token temperature schedule; B2-8 attention-sink memory; B2-17 superposed lessons at one position; B2-12 mirror tasks; B2-28 cross-model transfer by margin targets | I | Each is a new carrier or new symmetry for an existing memory |
| 3 | B1-11 anchor transplant; B1-29 self-reported override budget; MZ1 / B1-1 reader vaccination; MZ5 / B1-5 low-rank functional antidote; MY1 overridability predicts fine-tune fragility; MY3 one correctability meter | I | Diagnostics and defenses built on ledger measurements |
| 2 | Remaining 56 flood ideas, MY2, MY4, MZ2, MZ4 and the four risky cards | I | Gating, replay, retirement and market variants of known methods |

## NOOA ([PR #41](https://github.com/manojbajaj95/cl/pull/41): 40 ideas + cards N1–N4)

| Score | Ideas | P/I | One line |
|---|---|---|---|
| 4 | N1 / #1 round-trip consolidation (code → weights → code) | P | Weights as a denoiser that returns better programs |
| 4 | N2 / #2 inheritance-shaped adapters, with #5 refactoring as weight surgery as its arm | P | The agent's own class tree is the weight-sharing topology |
| 4 | N4 / #4 the `...` frontier after a model upgrade | P | The code/weights boundary is a movable, optimizable object |
| 4 | #21 program-space plasticity loss, with #22 dormant-method resets | P | Plasticity loss and resets carried into the code substrate |
| 3 | N3 / #3 reachability forgetting (= programs-weights P33); #6 signature-hash task identity; #7 contract-directed replay; #13 semantic staleness; #24 weak references; #36 ellipsis density; #40 metaclasses | P/I | Language features reused as CL operations |
| 2 | Remaining 29 ideas | I | Known memory policies renamed in OO terms |

## learning primitives ([PR #42](https://github.com/manojbajaj95/cl/pull/42), 36 ideas)

The strongest file so far.

| Score | Ideas | P/I | One line |
|---|---|---|---|
| 5 | L1 prompt-addressable checkpoints | P | One set of weights reproduces any past self by tag, so rollback, diff and bisect become prompts |
| 4 | D1 deferred-commitment weights; D2 gradient IOUs | P | Learning before the label: superposed hypotheses or promised updates, collapsed later |
| 4 | O1 idempotent and O2 commutative learning operators; L4 group-restricted (invertible) updates | P | Algebraic laws imposed on the learner itself |
| 4 | D3 hypothetical fine-tuning as a query; S1 memory relocation with invariance; S2 carrier data; S4 round-trip fixed points; M3 plasticity tokens; W3 LR schedules as messages; W5 weight tides | P | New operations on learning: simulate, move, encode, tag, transmit, phase |
| 3 | L5, D5, S3, S5, O3, O4, O5, M4, A2, W1, W6 | P/I | Reversible SGD, anti-updates, rate-distortion, cassettes, learned unlearner, update kernels and hashing, manifests, testaments, dream-erase, body double |
| 2 | L2, L3, D4, O6, M1, M2, A1, A3, A4, A5, W2, W4 | I | Overlap other pool ideas or known attribution, routing and market work |

## self-modifying ([PR #43](https://github.com/manojbajaj95/cl/pull/43), 38 ideas)

| Score | Ideas | P/I | One line |
|---|---|---|---|
| 5 | SM1 seed-log autobiography | P | The whole learned history is a readable `(seed, scale, reason)` log in the model's own context that regenerates the weights exactly |
| 4 | SM3 weight quines; SM7 neutral-drift reserve; SM15 ontogeny distillation; SM25 Lamarckian optimizer state | P | Self-regenerating edits, function-preserving drift for plasticity, inheriting how to learn |
| 4 | SM2 weight ISA (merge with programs-weights P21); SM6 write tokens in decoding | P | Risk: 2611.21885 and the WSP papers |
| 3 | SM5, SM9, SM12, SM19, SM20, SM26, SM27, SM29, SM30, SM33, SM36, SM37 | P/I | OPSD variants, loss code, generational tests, leash slot, path gating, self-forecast, weight-reading, weight dreaming |
| 2 | SM4, SM8, SM10, SM11, SM13, SM14, SM16–SM18, SM21–SM24, SM28, SM31, SM32, SM34, SM35, SM38 | I | Duplicate other pool ideas or known methods |

## physics-math ([PR #44](https://github.com/manojbajaj95/cl/pull/44), 52 ideas)

| Score | Ideas | P/I | One line |
|---|---|---|---|
| 4 | #11 spin-echo refocusing; #12 anti-Zeno consolidation | P | Specific non-monotone predictions: a function-preserving reflection refocuses drift; an intermediate projection rate speeds new learning |
| 4 | #21 kinetic proofreading for lesson writes | P | Predicts error falling exponentially in delayed stages versus linearly in budget; plugs straight into the contamination law's gate term |
| 4 | #26 winding-number bits; #27 holonomy writes; #43 Chinese-remainder task storage | P | Memory protected by topology, geometric phase or arithmetic, not by penalties |
| 4 | #20 stochastic-resonance recall; #31 sheaf cohomology of lesson stores; #40 Lie-algebra closure | P | A noise recall knob for sub-threshold memories; global (not pairwise) lesson inconsistency; composing skills by algebra |
| 3 | #1–10, #13–17, #24, #25, #29, #30, #34, #37–39, #41, #42, #44, #46, #48, #49 | P/I | Physics-derived detectors, schedules and constraints; most reduce to known projection, multi-timescale or curvature methods |
| 2 | #18, #19, #22, #23, #28, #32, #33, #35, #36, #45, #47, #50–52 | I | Duplicates (W1, L5, Lindy) or known (hyperbolic, coresets, fractional momentum) |

## econ-society ([PR #45](https://github.com/manojbajaj95/cl/pull/45), 45 ideas)

| Score | Ideas | P/I | One line |
|---|---|---|---|
| 4 | E2 logit price index for index-linked memories | P | Fine-tuning inflates the model's units, silently devaluing every threshold, margin and router bias written in old units |
| 4 | E4 emphasis hyperinflation with a conserved salience supply | P | Predicts a measurable drift in self-written lessons; ties to self-contamination |
| 4 | E32 metered lessons (error-correcting structure); E30 stemmatic reconstruction of lost skills; E31 Tasmania critical fleet size | P | Copy-error correction, phylogenetic recovery, and a predicted phase transition in fleet culture |
| 3 | E1, E5, E11–E13, E15, E21, E23, E24, E26, E28, E33, E34, E36, E39, E44 | P/I | Market, institutional and evolutionary rules applied to capacity, replay and fleets |
| 2 | Remaining 24 ideas | I | Duplicates (Lindy = aging clocks, A2 testaments, fleet markets) or reworded allocation |

## Running leaders (provisional, 7 of 8 sources in; neuro-bio, the tree nodes and the CL-bench proposer still to come)

Top 10 for prior art once the pool is complete, if nothing new displaces them: L1, SM1, P21 (+SM2), D1 (+D2), O2 (+O1), N1 (+S4, SM17), SM7, P19 (+N4, E2), physics #11 spin echo, physics #21 kinetic proofreading. Next in line: SM25, W3, E4, E32.

# Round 2 (tree nodes and continual-learning-bench)

| Source | 4s | 3s | 2s |
|---|---|---|---|
| Harness tree node ([PR #47](https://github.com/manojbajaj95/cl/pull/47), 17) | none | #2 steering tomography, #4 teacher as causal query planner, #5 typed adjoints (TextGrad-adjacent), #6 interchange-addressed skill cells, #7 rebasing by measured noncommutation, #9, #14, #16 | the rest: mostly restate P9/P17/X4 contracts in causal language |
| CL-bench flood ([PR #48](https://github.com/manojbajaj95/cl/pull/48), 36) | B6 edge-addressable weights (one rank-1 component per believed causal edge, so a graph edit is a weight edit) | B1 schema migrations, B2 Logbook compiled into a latent register, B3 inverse Logbook synthesis, B10 portable server-side learning state, B15 stigmergic memory, B20 environment-version transport, B31 memory-vs-scale exchange rate | the rest: bench-specific variants of verification, gating and resets |
| Forward-only tree node ([PR #50](https://github.com/manojbajaj95/cl/pull/50), 18) | #3 orthogonal question barcodes (several edits multiplexed in one perturbed forward batch, decoded by balanced codes) | #1 trace-to-weight compiler, #2 credit-address book, #6 patch homomorphism, #16 zero-read data-transfer edits, #17 writable shadow model | #8 and #11 (= SM8, NB01/Z1), #14 and #15 (improvements, as the node labels them) |

**Against the leaders:** nothing in round 2 displaces the top 3 (L1, N1, SM1). B6 and forward-only #3 join the 4-tier, behind them. Forward-only #3 is the strongest new candidate for the next prior-art batch. Nearest risks: multiplexed SPSA and coded perturbations, and SM1, which also builds on seeded forward-only steps.
