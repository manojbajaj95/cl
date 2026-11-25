# Landmark Paper Style Reference

Observed structural and stylistic patterns from the actual LaTeX sources of five landmark ML papers. Consult this reference when choosing a paper structure, drafting a tricky section, or calibrating prose density.

## 1. *Attention Is All You Need* (Vaswani et al., 2017 — arXiv:1706.03762)
**Archetype:** Clean architecture + systems + empirical paper (10 pages main text).

- **Section layout:** Abstract (162 words) → 1. Introduction (4 paragraphs, ~290 words) → 2. Background (4 short paragraphs) → 3. Model Architecture (top-down: Stacks, Attention, FFN, Embeddings, Positional Encoding) → 4. Why Self-Attention (Table 1 complexity axes) → 5. Training (Data/Batching, Hardware/Schedule, Optimizer, Regularization) → 6. Results (Main Table 2, Ablation Table 3, Generalization Table 4) → 7. Conclusion (3 short paragraphs) → Appendix visualizations.
- **Signature craft moves:**
  - **Ruthless intro tightening:** Commented-out drafts in `introduction.tex` and `background.tex` show long, discursive paragraphs cut down to 4 crisp paragraphs: (1) SOTA RNNs, (2) sequential bottleneck, (3) attention already exists alongside RNNs, (4) pure-attention Transformer + 12h on 8 P100s.
  - **One-table architectural argument (Table 1):** Compares Self-Attention, Recurrent, Convolutional, and Restricted Self-Attention on 3 quantitative axes (*Complexity per Layer*, *Sequential Operations*, *Maximum Path Length*).
  - **Cost alongside quality (Table 2):** Every translation BLEU score sits next to estimated Training Cost (FLOPs), making the efficiency claim indisputable.
  - **Blank-means-base ablation table (Table 3):** Base row on top, then lettered groups `(A)`–`(E)` where unchanged hyperparameters are left blank. Each group tests one hypothesis and gets 2–3 sentences of interpretation.
  - **Honest speculation tagging:** Uses *"We suspect..."* (for $\frac{1}{\sqrt{d_k}}$ scaling, backed by a crisp variance footnote) and *"We hypothesize..."* (for sinusoidal relative-position linearity) instead of asserting unproven theory as fact.

## 2. *Deep Residual Learning for Image Recognition* (He et al., 2015 — arXiv:1512.03385)
**Archetype:** Anomaly-driven empirical discovery + simplest-possible mechanism.

- **Section layout:** Abstract (203 words; opens with a 7-word sentence: *"Deeper neural networks are more difficult to train."*) → 1. Introduction (teaser anomaly Figure 1 on page 1) → 2. Related Work → 3. Deep Residual Learning (formulation + identity shortcuts + architectures) → 4. Experiments (ImageNet plain-vs-ResNet controlled pairs, CIFAR-10 100/1000-layer analysis, COCO detection transfer).
- **Signature craft moves:**
  - **Teaser anomaly on Page 1 (Fig. 1):** Shows 56-layer plain net having *higher training error* than 20-layer plain net — immediately ruling out overfitting and motivating the paper in one glance.
  - **Constructive existence argument:** Before any math, argues that a deeper model *could* copy the shallower model and add identity layers, proving the failure is an optimization difficulty, not expressivity.
  - **Matched-pair experiments:** Always compares `plain-18/34` vs `ResNet-18/34` with identical FLOPs and parameter count so the shortcut connection is the sole variable.

## 3. *LoRA: Low-Rank Adaptation of Large Language Models* (Hu et al., 2021 — arXiv:2106.09685)
**Archetype:** Practical adaptation primitive + deep mechanism analysis (directly relevant to continual learning & adapter research).

- **Section layout:** Abstract (196 words) → 1. Introduction (compact wrapfigure Fig. 1 on page 1) → 2. Problem Statement → 3. *Aren't Existing Solutions Good Enough?* → 4. Our Method (low-rank update + Transformer application + practical benefits) → 5. Empirical Experiments → 6. Related Works → 7. *Understanding the Low-Rank Updates* → 8. Conclusion.
- **Signature craft moves:**
  - **Explicit failure-mode section (Sec. 3):** Names the exact operational defects of prior methods (adapters add inference latency; prefix-tuning eats sequence length) with numbers.
  - **Question-driven science section (Sec. 7):** Organizes post-hoc mechanism analysis into three numbered research questions (*Which weight matrices? What optimal rank $r$? How does $\Delta W$ compare to $W$?*) held at a **fixed parameter budget** (18M params), turning an engineering paper into scientific insight.

## 4. *Denoising Diffusion Probabilistic Models* (Ho et al., 2020 — arXiv:2006.11239)
**Archetype:** Theory-to-simplified-algorithm paper.

- **Section layout:** Abstract (107 words — ultra-crisp!) → 1. Introduction → 2. Background (clean variational bound) → 3. Diffusion Models and Denoising Autoencoders (choice of parameterization + simplified objective) → 4. Experiments (sample quality, parameterization ablation Table 2, progressive coding, interpolation) → 5. Related Work → 6. Conclusion → Appendices (extended derivations, experimental details).
- **Signature craft moves:**
  - **Side-by-side Algorithm 1 (Training) & Algorithm 2 (Sampling):** Each is 6 lines of pseudocode. A reader can implement the entire method from those two boxes alone.
  - **Derivations in Appendix, intuition in Main Text:** Main text shows only the key identities that motivate the simplified $\epsilon$-prediction objective; full algebra lives in Appendix A.

## 5. *Training Compute-Optimal Large Language Models* (Hoffmann et al., 2022 — arXiv:2203.15556)
**Archetype:** Empirical scaling / scientific correction paper.

- **Section layout:** Abstract (194 words) → 1. Introduction (explicit contrast with Kaplan et al. + summary Table 1) → 2. Related Work → 3. Three Independent Approaches (Approach 1: fixed model sizes; Approach 2: IsoFLOP profiles; Approach 3: parametric loss fit) → 4. Chinchilla (matched-compute validation against Gopher) → 5. Discussion & Conclusion.
- **Signature craft moves:**
  - **Triangulation:** Uses three distinct statistical analyses on the same sweep and shows all three converge on the same scaling exponent ($a \approx b \approx 0.5$) — high-confidence empirical science.
  - **Respectful, quantitative correction:** Directly states what prior work (Kaplan et al.) got right, where the conclusion diverges ($5.5\times / 1.8\times$ vs equal scaling), and *why* (learning-rate schedule & embedding parameters in Appendix).
