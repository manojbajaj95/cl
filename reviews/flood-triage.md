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
| Guided-edits tree node ([PR #49](https://github.com/manojbajaj95/cl/pull/49), 22) | #8 self-describing weights (an auxiliary head trained from birth writes a manifest for each block, so editing becomes a lookup) | #1 weight debugger, #2 weight-edit world model, #4 edits with falsifiable predictions, #7 learning edit idioms from SGD diffs, #11 cross-model edit transport (near Heirloom 2611.00650 and rebasin), #12 portability score, #21 | #3 gauge fixing (known canonicalization), #5 and #6 (metrics: improvements), #13 and #20 (= P30, P22/GRACE), the rest |

**After PR #49:** still no change to the top 3. Self-describing weights joins the 4-tier and feeds SM1 and L1 directly as a readable substrate. The node's CPU probe finds almost no headroom in choosing *where* to edit, which agrees with the W-ISA kill: edit location is not the frontier.
| RL-on-OOD tree node ([PR #51](https://github.com/manojbajaj95/cl/pull/51), 18) | none | #3 verifier twins that invert one accidental cue, #9 reversal-based credit depth (a measured dependency horizon), #1 executable fork tapes, #2 teacher as experimental designer, #5 action transport maps, #10 branch flow conservation (TD-like), #15 mutant verifiers | #11 (= forward-only #3), #13 (= O2/Y2), #12 (= guided-edits #18), #16 and #17 (improvements), the rest. The core verified-fork update is VinePPO-style branching with a teacher nominating alternatives |

**After PR #51:** the top 3 are unchanged. This node's strongest theme is identifiability: experiments that separate the transferable rule from the shortcut before writing. That is a good evaluation axis for the top 3 tests, but the node offers no new object at the 4-tier.
| Discrete-backprop tree node ([PR #52](https://github.com/manojbajaj95/cl/pull/52), 18) | none | #1 repair variables as wires, #3 rejection algebra (feasible/refuted/unknown messages), #9 obligations as minimum-displacement projections, #14 library of certified failed inverses, #17 reserve of future repairs (cf. SM7) | the rest: weakest precondition, CEGIS and refinement-type machinery applied to harness ports (the node names these baselines itself) |

**After PR #52:** the top 3 are unchanged. The node is well grounded but mostly formal-methods restatement. Its one new object is #14, storing proofs that a write language *cannot* fix a failure.
| Self-describing-weights tree node ([PR #53](https://github.com/manojbajaj95/cl/pull/53), 20) | #8 gauge-orbit metadata (checksummed symbols stored in exact function-preserving permutations or signs); #1 executable weight header (a calibrated, live-checked sketch of each layer's write effects) | #3 ABI-stable training (= P19), #4 units that write their own names, #6 edit algebra (= O2/X3), #11 the model reads itself, #12 write-through-language, #16 differential versioning (cf. SM1), #18 cross-model Rosetta, #19 address abstention | #15 holographic layers (HRR, known), #13 nested dropout (known), #2, #9, #14, #17 and the rest |

**After PR #53:** the top 3 are unchanged, but #8 is the strongest tree-node idea so far. Gradient training is equivariant under exact discrete symmetries, so a permutation- or sign-coded label should survive any amount of training until two units collide. That gives a zero-function-cost channel for provenance or version tags, which L1 and SM1 could use. Nearest prior art to check: permutation-based weight watermarking. Its rescaling variant fails under weight decay.
| Info-coding flood ([PR #56](https://github.com/manojbajaj95/cl/pull/56), 64) | #58 write-once-memory codes for plastic weights (rewrite a weight region several times without erasing what it encodes); #38 dirty-paper coding for new tasks (precode the new task against the known old weights instead of avoiding them); #61 weights as a steganographic channel for their own history (same as PR #53 #8) | #1 parity layers, #2 fountain-coded adapters, #17 arithmetic-coded memory in the model's own probabilities, #22 Wyner-Ziv consolidation, #44 CRC on behaviours, #46 bits-back consolidation, #57 stuck-at-defect writing, #59 zero-error capacity, #62 version-to-version channel (= P19), #63 turbo weights↔memory | the rest: replication, sketches, Bloom filters, LR schedules, or known IB / rate-distortion framings |

**After PR #56:** with L1 falsified, the top 3 are N1 and SM1 (both paused) plus a vacancy. The candidates for the vacancy are gauge-orbit metadata (PR #53 #8, merged with #61 here), WOM codes (#58) and dirty-paper coding (#38). That gets settled in the prior-art screen once the pool is complete.
| Discriminating-experiments tree node ([PR #57](https://github.com/manojbajaj95/cl/pull/57), 21) | none | #1 shadow-rival head (a lazy twin as an explicit shortcut hypothesis; cf. LfF's biased model), #2 witness sets as memory, #3 witness-to-constraint compiler, #11 identifiability-debt ledger, #12 `do()` action tokens, #15 internal experiments before external ones, #21 rival resurrection test | the rest: EIIL, SOAR, minimal pairs, differentiable design (known) |
| Systems-db flood ([PR #58](https://github.com/manojbajaj95/cl/pull/58), 62) | SD3 write-skew between lessons (each update preserves an invariant alone, the pair breaks it; a higher-order interference that pairwise cosine misses) | SD2 MVCC mixed-version cuts, SD8 sagas with compensations registered at write time, SD11 ARIES undo-middle/redo-later (cf. SM1), SD12 LSM memtable→adapters, SD20 rerere for interference, SD46 bitemporal knowledge, SD53 MESI coherence between context and weights | the rest (about 54): database and git vocabulary over known gating, merging, routing and unlearning; SD47 `AS OF` = L1, falsified |

**After PRs #57 and #58:** no change. SD3 is the one new measurable object: count write-skew triples among real updates. If they are common, pairwise interference metrics undercount forgetting.
| Logic-proofs flood ([PR #59](https://github.com/manojbajaj95/cl/pull/59), 64) | LP39 re-derivability memory (store a lesson only if a verifier shows the current model *cannot* re-derive it, and drop it once it can; with LP40) | LP1 cut-elimination consolidation, LP4 harmony loss (introduce/eliminate round trip, cf. N1), LP7 conservative-extension learning, LP22 bounded-equivalence capacity release, LP29 anti-unification consolidation, LP53 automata extract–reinsert, LP58 Löb-consistent self-model, LP59 "will I still believe X after learning Y" (cf. 2610.12397), LP62 random-SAT forgetting phase (cf. Gardner capacity) | the rest: verification, certified training, TMS/AGM and Lean tooling over known CL methods |
| Cogsci flood ([PR #61](https://github.com/manojbajaj95/cl/pull/61), 64) | none | C12 retrieval-induced forgetting as pruning, C19 source monitoring head, C23 mutual exclusivity as write collision, C34 modeling one's own past self (cf. L1, falsified), C40 infantile amnesia as format migration, C47/C48 concept differentiation and coalescence, C54 learnability bottleneck, C58 devaluation probes | the rest: well-known developmental and memory effects mapped onto known curricula, replay, gating and sleep |
| Trace-compile tree node ([PR #60](https://github.com/manojbajaj95/cl/pull/60), 38) | none | #3 collision-triggered feature split, #11 counterexample-driven address allocator, #13 write demultiplexer, #19 ∀-patching over generated families, #26 near-silent units as a write ISA (cf. W-ISA), #31 trace programs instead of values, #35 spectral domain growth | the rest: ROME/MEMIT-style locate-and-edit with linker, type and commutator vocabulary already scored under P17, O2 and X1 |

**After PRs #59–#61:** no change. Since round 1 the 4-tier has gained gauge-orbit metadata, the executable weight header, WOM codes, dirty-paper coding, write-skew (SD3), re-derivability memory (LP39), edge-addressable weights (B6) and question barcodes. These are the candidates for the top-10 screen.
| Edit-simulator tree node ([PR #63](https://github.com/manojbajaj95/cl/pull/63), 24) | none | #1 edit-response tensor, #7 shadow twin edited first, #8 retention shadow prices, #10 simulator trained on the model's own past SGD steps, #18 self-simulation of post-edit outputs, #19 edits with a domain of validity, #21 edit-effect hash, #24 temporal simulator | the rest: TuneAhead-style predictors, influence functions, TabPFN and RL-with-baseline variants |
| Harness-falsifying-probes tree node ([PR #62](https://github.com/manojbajaj95/cl/pull/62), 24) | none | #3 interaction sets as the hypothesis object, #9 retention-only refuter, #15 adversarial function-preserving reparametrization, #20 refuting over futures, #21 negative addresses, #24 harness-to-weights handoff by refuted claims | the rest: locator/refuter games and bandits over known attribution |
| Chemistry flood ([PR #64](https://github.com/manojbajaj95/cl/pull/64), 64) | none | 02 autocatalytic skills, 09 vitrimer rewiring under a conservation law, 11 sacrificial parameters that fail first, 12 valence-limited handles, 24 two-way shape memory, 42 sorption-hysteresis operating ranges, 49/51 tracer and pulse–chase provenance, 53 split-and-pool attribution, 60 delayed recovery without replay | the rest: catalysis, compartment and assembly metaphors for known gating, routing and adapter methods |
| Self-testing-skills tree node ([PR #65](https://github.com/manojbajaj95/cl/pull/65), 24; its 8 cited papers read in full from arXiv) | none | #1 skill = claim + crucial experiment (only the help-vs-hurt discriminating half is open: Beyond Gain [2610.32322](https://arxiv.org/abs/2610.32322) already stores a synthesized task per skill), #3 experiments indexed by the reader's margin (cf. MX1), #6 transfer the experiment and re-fit the conclusion, #9 anti-skill siblings, #23 skill-to-skill cross-examination | #2 internalized-vs-uncovered litmus is done by Beyond Gain (withhold the skill, trust a high unaided score only if another model gains); #5 skill-generated twin tasks is close to SkillSandbox [2610.10088](https://arxiv.org/abs/2610.10088) (synthesized scenario, with/without verifier); the rest: gain prediction, calibration and VoI gating (SkillApt, 2609.32274, 2610.39358) |
| Hardware flood ([PR #66](https://github.com/manojbajaj95/cl/pull/66), 65) | none | H02 device drift as a timestamp, H15 acknowledge-before-forgetting synapses, H29 retention leases, H39 handing off write debt instead of logs, H54 fragment-tolerant holographic writes, H59 reservoir contracts that survive a hardware swap | the rest: analog-memory, spiking and memory-hierarchy mechanisms mapped onto known gating and replay |
| Negotiated-constraints tree node ([PR #67](https://github.com/manojbajaj95/cl/pull/67), 26) | none (folds into existing 4s) | #1 counteroffer probes generated from weights alone, #9 edit escrow, #12 gauge negotiation (old behaviours relocate along function-preserving symmetries, cf. gauge-orbit metadata), #13 behaviours that pay with released capacity, #24 forgetting insurance | the rest: null-space projection, KL budgets and ES variants |
| PL-compilers flood ([PR #68](https://github.com/manojbajaj95/cl/pull/68), 64) | none | 14 negative-dependency invalidation, 23 deoptimization with write restitution, 52 product programs for forgetting localization, 58 ephemerons (a memory lives only while its key does), 59 lazy migrate-on-write with old-reader projections | the rest: type-system and compiler vocabulary over known routing, provenance and merging |
| Weights-self-header tree node ([PR #69](https://github.com/manojbajaj95/cl/pull/69), 25) | folds into the executable weight header: #1 header-consistency loss and #10 header in the gauge (with gauge-orbit metadata) are its concrete forms; #21 a header that predicts its own staleness | #3 secant headers, #4 optimizer-equivariant transport, #6 scope-carrying header, #16 no-op certificates, #19 adversarial header audit | the rest: NTK, influence and conformal machinery |
| RL-forward-operations tree node ([PR #70](https://github.com/manojbajaj95/cl/pull/70), 26) | none | #1 shared-seed task × perturbation matrix, #19 antithetic sums as a free protection map, #22 negation as an operation test, #24 context–weight exchange rate, #26 seed provenance (= SM1) | the rest: ES, ICA and variance-reduction variants |
| Multiagent flood ([PR #71](https://github.com/manojbajaj95/cl/pull/71), 64) | none | M2 selling the cross term (pricing interaction, cf. SD3), M16 reveal when you learned it, M33 call options on a learning direction, M49 transmit the question, not the answer, M52 consensus commits a distinction | the rest: auctions, VCG, PSRO and insurance over known allocation and replay |
| Inversions flood ([PR #72](https://github.com/manojbajaj95/cl/pull/72), 64) | 03 relearning as the read head (memory written so it is only readable through relearning speed, i.e. savings as a deliberate channel) | 01 memory by missing answers, 06 unlearning as a concept-ancestry assay, 21 writing interactions without marginals (cf. SD3), 25 KV collision as a join, 56 a skill stores the question it can't answer (cf. LP39), 63 a canary that must go extinct | the rest: inversions of known gating, interference and drift results |
| Obligation-identifiability tree node ([PR #73](https://github.com/manojbajaj95/cl/pull/73), 25) | none | #2 the keep bit as the only external query, #6 non-identifiability witnesses as outputs, #8 ±Δ interferometry, #24 keep-bit budget scaling law | the rest: active learning and disagreement-region search |
| Control-dynamics flood ([PR #74](https://github.com/manojbajaj95/cl/pull/74), 66) | CD2 a waterbed law for forgetting (a Bode sensitivity integral: reducing forgetting at some timescales must raise it at others) | CD3 Floquet forgetting under cyclic curricula, CD7 non-minimum-phase skills, CD37 prompt-reachability retention (cf. 2610.08718), CD49 points of no return, CD63 fundamental-lemma replay | the rest: CBF, MPC, Kalman and Lyapunov tools over known regularizers |
| Immuno-dev flood ([PR #75](https://github.com/manojbajaj95/cl/pull/75), 64) | none | ID05 missing-self invariants, ID18 transferring the tolerance boundary, ID33 inheriting tests, not weights, ID50 injury transfer, ID62 a map of tolerable mutations | the rest: immune and developmental metaphors for gating, provenance and growth |
