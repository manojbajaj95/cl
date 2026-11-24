# Memory-form proposer batch 4: choosing a lesson's form from its learned-salience trajectory

Read before writing: ledger (PR #6), agent batches (PR #7), the batch 1-3 verdicts. Prior art checked via alphaXiv on 2026-11-24. This batch is small on purpose: most of the remaining form-specific ground I checked is covered (see the table below).

## R1. (Arm for the M2/N1 pilot) Route a lesson to weights or text by how its learned bias b_i moves over time
**Form.** Hybrid text ⇄ weights. M2 learns a per-lesson attention-logit bias b_i from dense log-prob gradients over time. So every lesson carries a salience trajectory b_i(t), a quantity that exists only once lessons are read through a learned attention handle.
**Claim.** A lesson whose b_i rises and then stays flat holds a stationary truth, and is safe to consolidate into weights. A lesson whose b_i swings (raised in one regime, suppressed in the next) is regime-conditional. Consolidating it hard-codes one regime, so it should stay in text, where M2 can keep turning it up and down. Prediction: routing by the variance of b_i over a trailing window beats consolidating everything, consolidating nothing, and routing by usage, on recurring-regime streams.
**Closest prior art.** Use and Disuse (intent-structured, usage-based consolidation), Auto-Dreamer (learned offline consolidation), Instant Weight-Space Consolidation, ENGRAM (verified consolidation), Useful Memories Become Faulty When Continuously Updated. These decide consolidation from usage, verification or a learned policy, never from the stability of an outcome-trained read weight. E1 predicts consolidation loss from the lesson's ΔW share, not from regime stability.
**Strongest control.** ACE-style helpful/harmful counter variance, and usage-frequency routing, both at equal compute. Also E1's score with the same consolidation budget.
**Smallest falsifying test.** Reuse the M2 pilot's recurring-regime tool world (A, B, A, C, B ...). After 300 episodes, consolidate the top-k lessons by each routing rule into a LoRA and keep the rest in text. Then measure success on the next 300 episodes, including returns to earlier regimes. 3 seeds. **Kill** if b-variance routing does not beat counter-variance routing by ≥ 3 success points on regime returns, or if its Spearman with per-lesson consolidation regret adds < 0.1 over E1's score.

## Killed at proposal (self-review)

| Idea | Why dropped |
|---|---|
| Token-selective context distillation (distil only where context shifts logits) | Token-utility OPD, SCOPE (2610.38391), Speculative Self-Distillation, selective contrastive OPD |
| Consolidation timing from accumulated usage | Use and Disuse, Auto-Dreamer, Instant Weight-Space Consolidation |
| Minimal-diff lesson revisions keep off-target behaviour | ACE's incremental delta updates already target context collapse |
| Lesson self-report after consolidation (does the model know what it learned?) | Behavioural self-awareness after fine-tuning (2501.11120) |
| Activation-patch lesson memory gated by query match | Steering-vector memory (2610.14958) plus hidden-state retrieval, both killed |
| DSL program memory with LLM fallback, crossover study | A study, not a mechanism |
