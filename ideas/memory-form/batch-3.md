# Memory-form proposer batch 3: contrastive-pair memory, a parallel-reading arm for the lesson capacity law

Read before writing: ledger (PR #6), agent batches (PR #7), the batch 1-2 verdicts. Prior art checked via alphaXiv on 2026-11-24.

## C1. Contrastive-pair memory: store a lesson as a (good, bad) trajectory pair, read it as a logit difference
**Form.** No written lesson. Memory holds paired trajectory snippets from the same state, one that succeeded and one that failed. At read time the agent runs two forward passes, with the good snippet and with the bad one, and acts on ℓ_good + α(ℓ_good − ℓ_bad). Text memory must state the difference between the two in words. This form reads it as an exact difference of the model's own predictions, so features both snippets share cancel without anyone naming them.
**Claim.** The lesson-writing step is where agent memories go wrong: defective lessons (batch-11 P3), error reproduction (2610.27406), and memory-induced degradation. Contrastive-pair memory skips that step. It should beat written lessons when the distinguishing feature is hard to verbalise (a subtle argument format, an ordering), and tie them when it is easy to state.
**Closest prior art.** Contrastive decoding / context-aware decoding (CAD); PCED (2601.08670) contrasts each retrieved document's logits against the no-context prior for RAG, but never good against bad experience. Contrastive skill evolvers write text lessons from success/failure pairs (the 2610.27406 baselines, AdMem, ExpeL). Evidence-linked memory (Don't Just Trust Your Memory). I found no agent memory that is read as a logit difference between success and failure contexts.
**Strongest control.** The same pair placed in one context, labelled "worked" and "failed", with 2-sample self-consistency so the compute matches the two passes. Also a contrastive text lesson written from the same pair, and plain CAD (good snippet vs. no snippet).
**Smallest falsifying test.** Tool world with 30 failure modes: 15 easy to verbalise, 15 that are format/ordering subtleties. Collect one pair per failure mode, then run 400 test episodes. Qwen2.5-1.5B, 3 seeds, α swept on a dev split. **Kill** if C1 does not beat the labelled-pair-in-context control by ≥ 5 success points on the subtle half, or if plain CAD (no bad snippet) gets within the CI of C1. The second case means the bad snippet adds nothing.

## C2. (Arm for the lesson capacity law) Does the capacity knee come from attention crowding or from lesson conflict?
**Form.** The same lessons, read two ways: concatenated in one context, or PCED-style, with each lesson in its own pass and the logit shifts summed against the no-lesson prior. Parallel reading removes the competition between lessons for attention, but it keeps any real conflict between what the lessons say.
**Claim.** If the knee in the lesson capacity law is caused by attention crowding, it moves far right under parallel reading. If it is caused by semantic conflict, it stays put. This decides whether capacity is a property of the memory form (KV/attention) or of the lesson set. It also suggests a fix that no text-only method gives.
**Closest prior art.** PCED (2601.08670), Parallel Context Windows, REPLUG (mixture), and the surviving lesson capacity law in the ledger.
**Strongest control.** The capacity law's own setup, plus REPLUG mixture-of-probabilities at the same number of passes, which separates sum-of-logit-shifts from simple averaging.
**Smallest falsifying test.** Rerun the capacity-law sweep (N = 1 to 64 lessons) under both reading modes. **Dead** if the knee N* moves by less than a factor of 2 under parallel reading *and* the lessons do not conflict per a pairwise check, because then neither account explains the knee. If N* moves ≥ 2x, report capacity as form-limited.

## Killed at proposal (self-review)

| Idea | Why dropped |
|---|---|
| Lessons as trigger programs gating text insertion (rule + precondition) | AutoManual-style rule systems, Voyager/skill preconditions; interference-by-overlap is exact by construction |
| Closed-form (ROME/MEMIT/GRACE) edits as procedural agent memory | Lifelong editing (WISE, GRACE codebook keyed by activation) covers key-gated weight memory |
| Small model writes KV that a big model reads | Cache-to-Cache, KV-Lingo (2609.32610) |
| Text+weights double storage, disagreement flags stale memories | Reduces to the off-target KL already in E1/M3 and to the double-dosing pilot (2606.11627) |
| kNN-LM style logit memory keyed by context | kNN-LM; hidden-state retrieval already killed in the ledger |
