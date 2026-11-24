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
