# Long-run agent memory, batch 4: no new idea; saturation report

R1 was killed (KAFT, Li et al. 2022, plus 2610.02614), and its per-cycle flip-rate measurement was folded into the M3 pilot. Every candidate I tried for this batch is already covered by 2026 work, so this batch proposes nothing new. It lists what to skip so other proposers don't repeat the search.

| Candidate | Covered by |
|---|---|
| Evidence-gated counterfactual consolidation (follow a contradicting lesson only with evidence) | KAFT (relevant vs irrelevant context); selective context preference optimization ([2608.06377](https://arxiv.org/abs/2608.06377)); outdated-vs-poisoned memory robustness ([2610.41056](https://arxiv.org/abs/2610.41056)) |
| Precondition erosion: repeated lesson merges drop scope, so lessons over-apply | Scope-aware commit rules ([2610.09008](https://arxiv.org/abs/2610.09008)), authority collapse at consolidation ([2608.01679](https://arxiv.org/abs/2608.01679)), Memory Trap ([2611.07554](https://arxiv.org/abs/2611.07554)), ACE context collapse |
| Self-legibility: lessons the same model can't apply when it reads them later; check effect at write time | "Admitted is not effective" ([2611.29727](https://arxiv.org/abs/2611.29727)), falsification-gated self-evolution ([2611.14326](https://arxiv.org/abs/2611.14326)), RBC ([2610.18427](https://arxiv.org/abs/2610.18427)) |
| Delayed memory gains (a phase transition in memory value after many episodes) | Process-level evaluation of self-evolving agents ([2609.24663](https://arxiv.org/abs/2609.24663)); a study, not a mechanism |
| Memory dependence: training with memory in context makes the agent worse without it; fix with memory dropout | Standard retrieval-dropout training for RAG |
| Seed divergence of memory runs, then pick the best run | RBC already chooses among growth runs |
| Support counters inflated by episodes that used the lesson (circular evidence) | Same confound as killed M2; provenance in Memory Echo ([2610.17763](https://arxiv.org/abs/2610.17763)) |

**What this says about the angle.** Survivors and near-misses all come from interactions *between* memory mechanisms (context × weights: M3 passed; R1 was real but already fixed). Single-mechanism long-run effects (staleness, pruning, drift, compression, write gates, routing) are densely covered by late-2026 papers. The remaining value is in the M3 pilot: residual memory, consistency-regularizer control, per-cycle flip rate. Any future idea here should come from M3's raw pilot numbers rather than from new mechanisms.
