---
name: paper-architecture-and-prose
description: "Draft research papers in the crisp, evidence-first style of landmark ML papers (Attention Is All You Need, ResNet, LoRA, DDPM, Chinchilla), covering structure, narrative arc, math notation, and both positive and clean negative results."
---

# Paper Architecture and Prose (Landmark ML Style)

Use this skill when outlining or drafting a research paper for `manojbajaj95/cl` (or any ML paper targeting arXiv / alphaXiv / NeurIPS / ICLR). Grounded in the LaTeX sources of *Attention Is All You Need* (`1706.03762`), *Deep Residual Learning* (`1512.03385`), *LoRA* (`2106.09685`), *DDPM* (`2006.11239`), and *Chinchilla* (`2203.15556`). For annotated structural breakdowns and excerpts from those five papers, read `references/landmark-patterns.md`.

## Core Principle

A landmark ML paper makes **one sharp claim**, states the **exact structural bottleneck or anomaly** that motivates it, introduces the **simplest mechanism or experimental test** that resolves it, and proves the claim with **controlled, budget-matched evidence**. Every paragraph earns its space; nothing reads like a survey, blog post, or sales pitch.

## Section-by-Section Blueprint

Target **6–10 pages** of main text (plus references and appendix). Put extended derivations, full hyperparameter tables, and extra traces in the appendix.

### 1. Title
- Short, concrete, memorable (3–10 words). Name the mechanism or the core finding, not a vague slogan.
- Good shapes:
  - Thesis statement: *Attention Is All You Need*
  - Mechanism + domain: *Deep Residual Learning for Image Recognition*; *LoRA: Low-Rank Adaptation of Large Language Models*
  - Empirical finding: *Training Compute-Optimal Large Language Models*

### 2. Abstract (110–200 words, 1 paragraph, 5–7 sentences)
Follow the 5-beat cadence shared by Vaswani et al., He et al., Hu et al., and Hoffmann et al.:
1. **Context (1 sentence):** Name the dominant paradigm in plain terms.
2. **Bottleneck / Gap (1 sentence):** State the specific failure, cost, or open question.
3. **Contribution (1–2 sentences):** State the exact mechanism, reformulation, or empirical investigation.
4. **Quantitative Result + Cost (1–2 sentences):** Give 2–3 concrete numbers *with* the budget/scale and strongest baseline comparison (never bare percentages without context).
5. **Generalization / Scope or Code (0–1 sentence):** One second-task transfer check, boundary condition, or code link.

### 3. Introduction (3–5 tight paragraphs, ~250–450 words)
Never write a sprawling multi-page introduction. *Attention Is All You Need* uses **4 paragraphs (~290 words)**. Pick the opening pattern that fits the paper:
- **Bottleneck-to-Escape-Hatch (Architecture/Method papers, e.g. Transformer, LoRA):**
  1. Dominant paradigm and its strength (2 sentences).
  2. Fundamental structural constraint that prior patches did not remove ("The fundamental constraint of sequential computation, however, remains.").
  3. Existing ingredient or insight that suggests a cleaner alternative.
  4. "In this work we propose X..." + one concrete headline result and cost.
- **Anomaly-First (Empirical / Diagnostic / Negative-Result papers, e.g. ResNet, Chinchilla):**
  1. Accepted wisdom or scaling assumption.
  2. A concrete counterintuitive observation shown immediately in **Figure 1 on page 1** (e.g. ResNet's 56-layer vs 20-layer training error; Chinchilla's IsoFLOP curves).
  3. Rule out the trivial explanation (e.g. "Unexpectedly, such degradation is not caused by overfitting").
  4. State the mechanism or empirical law and the key quantitative takeaway.
- Put **Figure 1** (architecture diagram, teaser anomaly plot, or main scaling curve) on page 1 or top of page 2.

### 4. Background / Problem Statement (Short, 0.5–1 page)
- Define the formal task, stream/evaluation contract, and notation cleanly before proposing anything.
- Contrast with the 2–3 closest prior approaches on **explicit, quantitative axes** — not vague adjectives.
- If the paper replaces or improves a primitive, include a compact **axes comparison table** (like Transformer Table 1: Complexity per Layer, Sequential Operations, Maximum Path Length) or a concise "Why Existing Solutions Fall Short" section (like LoRA Sec. 3).

### 5. Method / Mechanism (1.5–2.5 pages)
Write **top-down**: overall architecture/loop first (referencing Figure 1), then each component in logical execution order.
- **Compact equations + exact shapes:** Give the core equation, then immediately define every symbol and its dimension (e.g. $W^Q_i \in \mathbb{R}^{d_{\text{model}} \times d_k}$).
- **Separate intuition from fact:** When explaining *why* a design choice works without a proof, say so explicitly ("We suspect that...", "We hypothesize that...", as in Vaswani et al. Sec. 3.2.1 & 3.5).
- **Include a "Why X?" / Design Rationale subsection** (Transformer Sec. 4) or **side-by-side Algorithm boxes** (DDPM Alg. 1–2) when the contribution is algorithmic.
- **State exact resource accounting:** Parameter count, FLOPs, memory bytes, and inference/update latency compared to the baseline.

### 6. Experimental Setup & Results (2–3.5 pages)
- **Setup subsection (compact, reproducible):** Dataset/stream generator, splits, held-out seeds/streams, model sizes, optimizer, schedule, hardware, and wall time (like Transformer Sec. 5). Put exhaustive hyperparameter grids in the appendix.
- **Main Results Table:** Pair quality metrics with **cost/budget columns** (FLOPs, trainable params, wall time, or persistent bytes) and include the strongest matched-budget baselines and an oracle/upper bound where applicable.
- **Controlled Ablations ("Model Variations"):** Vary **one factor at a time** from a clearly defined `base` configuration. Group rows into lettered blocks `(A)`, `(B)`, `(C)` where each block answers one scientific question, and write one crisp paragraph interpreting each block.
- **Mechanism / Diagnostic Analysis ("Understanding X"):** Follow LoRA Sec. 7 or ResNet CIFAR-10 analysis — ask 2–3 sharp follow-up questions that test *why* the method works (or where it breaks), not just *that* it wins.
- **Generalization / Transfer Check:** One secondary task, shift regime, or independent environment showing the result is not an artifact of one benchmark (e.g. Transformer's WSJ parsing; ResNet's COCO detection).

### 7. Framing Clean Negative / Falsification Results
Negative and null results are first-class scientific contributions when written with landmark discipline:
1. **State the hypothesis and why it mattered** (what widely plausible mechanism or primitive was being tested).
2. **Prove the testbed works first:** Show the positive control / oracle / symmetry check passes so the null is not a bug.
3. **Report the matched-budget comparison cleanly** with paired confidence intervals across streams/seeds.
4. **Isolate the failure mechanism:** Show *which* assumption broke (aliasing, capacity saturation, interference, variance, etc.) via a targeted diagnostic plot or ablation.
5. **State the boundary condition:** Specify what would have to change for the mechanism to work.

### 8. Related Work (0.5–1 page)
- Place after Method or after Experiments (Transformer puts short Background early; ResNet/LoRA/DDPM put Related Work as a focused thematic section).
- Group by **mechanism or assumption**, never paper-by-paper summaries ("Smith et al. did X. Jones et al. did Y."). End each thematic paragraph by stating the exact difference from your work.

### 9. Conclusion (2–3 short paragraphs, ~150–250 words)
1. One-paragraph summary of what was introduced/established and the main empirical takeaway.
2. One short paragraph on **concrete limitations and open directions** (never vague hand-waving).
3. One line pointing to reproducible code/artifacts.

## Prose & Style Rules

### Do
- Use **active voice** and plain, direct verbs (*propose, measure, compare, replace, observe, show*).
- Keep sentences short and information-dense (target 15–25 words on average; vary rhythm naturally).
- Anchor every quantitative claim to a table, figure, or exact number in the text.
- Report uncertainty honestly: paired CIs or mean $\pm$ std over independent streams/seeds; treat noisy intervals as inconclusive.
- Explain unexpected trade-offs directly (e.g. Vaswani et al.: *"This hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score."*).

### Never Do
- **No hype or AI-slop vocabulary:** Ban *groundbreaking, revolutionary, paradigm shift, game-changing, delve, tapestry, leverage (as filler), comprehensive framework, seamlessly, remarkably (without numbers), unlock, empower, harness, robust (without specifying against what)*.
- **No throat-clearing openings:** Never start with *"In recent years, deep learning has witnessed tremendous progress..."* Start directly with the specific technical paradigm or problem (compare: *"Deeper neural networks are more difficult to train."* — ResNet; *"Recurrent neural networks... have been firmly established..."* — Transformer).
- **No redundant signposting:** Cut *"In this section, we will present the results of our experiments. First, we describe..."* Just start the subsection with the finding or setup.
- **No unsupported superlatives:** Replace *"significantly faster"* with *"trains in 12 hours on 8 P100 GPUs, $4\times$ fewer FLOPs than ConvS2S"*.
- **No notation drift:** Never use $d$ in one section and $D$ in another, or $N$ for both layers and sample count.

## Math & Notation Checklist
- Define every symbol before or on first use.
- Use consistent typography: scalars italic ($n, d_k$), matrices uppercase ($Q, K, V, W_1$), operators upright ($\mathrm{softmax}, \mathrm{LayerNorm}, \mathrm{FFN}$), sets calligraphic ($\mathcal{D}, \mathcal{L}$).
- State tensor dimensions inline right below each core equation.
- Keep main-text derivations to 3–6 clean lines; move long algebraic proofs to an Appendix section and link it with `\cref{app:...}`.
