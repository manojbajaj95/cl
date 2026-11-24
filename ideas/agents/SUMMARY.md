# Agent proposer: summary of batches 1–10

Angle: agents that keep learning after deployment. Verdicts are from the reviewer ledger (PR #6).

| Batch | Idea | Verdict | Reason / strongest control |
|---|---|---|---|
| 1 | A1 memory inoculation | KILLED | Inoculation prompting exists; a skeptic instruction plus exemplars ties |
| 1 | A2 Baldwin vs Lamarck | KILLED | Cross-episode meta-RL for LLM agents exists |
| 1 | A3 time-travel snapshots | KILLED | Flat reacquisition holds by construction |
| 2 | B2 vocabulary-grown skills | KILLED | Prompt-pool CL (L2P/CODA) and ToolkenGPT |
| 2 | B3 lesson-only interference (implicit ΔW alignment) | PASSED | Function-vector cosine (2605.16591), length-matched dilution |
| 3 | C1 inverse tool models | KILLED | Hindsight relabelling of agent trajectories exists (AgentHER) |
| 3 | C2 memory-loop Lyapunov exponent | PASSED → FALSIFIED in pilot (PR #11) | 20-step two-order divergence predicts at ρ 0.91 |
| 4 | D1 lesson capacity law | PASSED (gated on B3) | Length-matched dilution pool |
| 4 | D2 write-time poison energy | KILLED | Trigger-only poisons miss off-domain probes by construction |
| 5 | E1 consolidation-survival predictor | Pending | Effect size, first-step distillation loss |
| 5 | E2 edge-of-chaos tuning | KILLED (with C2) | Depends on C2 |
| 6 | F1 context interference → weight forgetting | Pending (gated on B3) | Distillation-gradient cosine |
| 7 | G1 exact-likelihood OPE of memory edits | PASSED, piloting | Unweighted log-likelihood gain; ESS ≥ ~50 per lesson |
| 8 | H1 surprisingly-popular fleet memory | PASSED, piloting | Keep every lesson and retrieve by regime |
| 10 | H1b SP from log-probs (memory-free prior) | Proposed as an H1 arm | Mean P_i without prior subtraction |

Killed at proposal (self-review): group-testing credit, genre-framed memory, revision-preference learning, label-free attention pruning, bucket-brigade credit, counterfactual-world vetting, policy-drift obsolescence, hidden-state retrieval, fleet synchronization, closed-form implicit-update writing, minimal-edit corrections, Matthew-effect skill libraries, Einstellung, e-value gating, coded fragments, cycle-consistency scoring, WSP repair, batch 9's six, MDL lesson scoring, silent-tool-drift prediction error.

Lesson for this angle: the ideas that survived use exact quantities only an LLM exposes (log-probs, activations) or aggregation signals that consensus discards. Analogy-driven mechanisms were almost all already published. From batch 11, ideas come from unexplained phenomena in the pilots' raw results.
