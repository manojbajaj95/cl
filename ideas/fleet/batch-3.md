# Fleet-memory proposer batch 3

I read the ledger (PR #6: Fleet Q1 killed, Q2 passed and in pilot, Q3 passed at low priority) and PR #7 batches 1–11 before each idea. Prior art was checked on alphaXiv on 2026-11-24.

## Q4. Lift that breaks under paraphrase predicts which lessons will not survive any reader change, using only the current model
**Claim.** Q2 needs the new model and Q3 needs a lineage history. A fleet that mixes readers (other families, a future model, a different harness) needs a portability score *now*, from the current model M alone. Memory portability work finds that compressed natural-language notes are model-coupled (2609.05339). Hypothesis: part of a lesson's lift on M comes from M-specific wording, such as phrasing that matches M's own token-level preferences, rather than from the content. That part does not move to another reader.

Mechanism:
- Paraphrase each lesson K = 3 times with an independent model P (a different family, meaning-preserving, checked by an NLI filter).
- Define fragility Φ(L) = ℓ̄_M(L) − mean_k ℓ̄_M(para_k(L)), using G1/Q2's log-prob lift on logged states.
- Portable lift = mean_k ℓ̄_M(para_k(L)).

Prediction: lessons with high Φ lose more of their benefit on new readers, and pooling by portable lift beats pooling by raw lift when the pool is read by a different model.
**Strongest control, and why it should fail.**
1. **Lift on another available reader, R.** Score each lesson's lift on one other existing model at the same scoring budget (the paraphrase pass costs about one extra model's worth of calls). This is the simplest same-budget baseline and the one most likely to tie. It measures transfer to R specifically. Φ claims to measure the coupling to M, which should predict transfer to *unseen* readers better than one sampled reader does.
2. Raw lift on M, ℓ̄_M.
3. An LLM judge of each lesson's generality.
4. Lesson length and specificity: token count and named-entity count.
**Smallest falsifying test.**
- Setup: the G1 router and the 40 frozen lessons from the Q2 protocol, with M = Qwen2.5-1.5B and paraphraser P = Llama-3.2-1B-Instruct. Control 1's reader is R = Qwen2-1.5B.
- Unseen readers: Qwen3-1.7B, Llama-3.2-3B and Gemma-2-2B (where the A/B/C legal tokens are single tokens).
- Truth: per-lesson retention on each unseen reader, Δ_reader(L) from 200 paired rollouts.
- **Kill** if Spearman(portable lift, mean Δ over unseen readers) is not ≥ 0.15 above control 1.
- **Kill** if Φ's Spearman with each lesson's loss of benefit (Δ_M − mean Δ_unseen) is < 0.3.
- **Kill** if the paraphrases change lift by less than the run-to-run noise of a re-tokenized identical lesson. If so, there is no wording-coupled component to measure.
**Closest prior art.**
- Memory portability (2609.05339) shows model-coupled notes but has no per-entry predictor.
- PromptBridge (2512.01420) and Rosetta Memory (2606.07711) *rewrite* prompts or memory for a known target model. Q4 predicts for unknown targets and only scores.
- RCCM (2610.19872) decomposes prompt-transfer gains and harms after transfer.
- Prompt-sensitivity work (Sclar et al.; 2509.01790; 2602.17316) measures performance variance under paraphrase. I found none that uses that variance as a portability predictor for memory entries.
- Self-preference / "models know models best" (2601.22699) is the explanation, measured for evaluation formats.

**Ledger check.** It is not Q2 or Q3, which need the new model or the lineage, and not a provenance idea. Paraphrase is used as an intervention on wording, not as data augmentation.

## Killed at proposal (self-review)

| Idea | Why dropped |
|---|---|
| Translate a fine-tuned copy's weight update into text lessons for the other copies (select lessons aligned with the update direction) | K2P 2609.38898, Prompt-Level Distillation 2602.21103, Introspection Adapters 2604.16812, interpreting weight diffs 2510.05092 |
| Forgetting-targeted text memory: after a weight update, add lessons whose lift is concentrated on states where the weights forgot | Reduces to evaluating lessons on the states that got worse (G1/Q2 lift restricted to u < 0); replay selection MSSR 2603.09892 and NADS 2610.25751 do this on the weight side |
| Pairwise lesson-interaction (synergy/interference) model to pick pooled sets | Agent Behavior Maps 2610.30014 and Oyama et al. find prompt displacements roughly compose, so the additive top-k control is likely to tie; D1 already covers capacity |
| A writer-reader match bonus: route lessons back to copies of the model that wrote them | Self-preference literature (2504.03846, 2601.22699), and Rosetta Memory's per-reader adaptation |
