---
name: paper-review-and-tighten
description: "Run a 5-pass adversarial review and tightening pass on a draft paper before compilation and publishing: claim-to-evidence audit, Vaswani-style prose compression, Reviewer-2 methodology attack, notation consistency, and visual PDF inspection."
---

# Paper Review and Tighten (5-Pass Pre-Submission Edit)

Use this skill after finishing a first draft and before publishing to alphaXiv or sharing a PDF. Landmark papers are not written crisp on pass one—the LaTeX source of *Attention Is All You Need* (`1706.03762`) contains commented-out drafts twice as long as the published text that the authors ruthlessly compressed. Run all five passes in order.

## Pass 1: Claim-to-Evidence Audit
Check every claim in the **Title, Abstract, Introduction, and Conclusion**:
- [ ] Every quantitative claim in the Abstract and Introduction matches the exact number in the main Results table and saved run logs (no stale numbers from an earlier run).
- [ ] Every qualitative claim ("faster", "lower variance", "isolates the fault", "generalizes") points to a specific `\cref{tab:...}`, `\cref{fig:...}`, or `\cref{eq:...}`.
- [ ] Unproven explanations are explicitly tagged as hypotheses (*"We suspect..."*, *"We hypothesize..."*), never stated as established theorems.
- [ ] For negative / null results: the positive control or oracle check is reported *before* the null finding so a reader knows the harness was not broken.
- [ ] Delete or narrow any claim the evidence does not fully support.

## Pass 2: Cut-the-Fluff Prose Compression
Aim to cut **20–30%** of draft word count without losing a single technical fact:
- [ ] **Abstract:** 110–200 words, one paragraph, 5–7 sentences.
- [ ] **Introduction:** 3–5 paragraphs (~250–450 words). Delete any opening sentence that starts with *"In recent years..."*, *"With the rapid rise of..."*, or *"X has attracted widespread attention..."*.
- [ ] **Zero AI-slop words:** Grep the `.tex` files for: `delve`, `tapestry`, `groundbreaking`, `revolutionary`, `game-changing`, `paradigm shift`, `seamlessly`, `comprehensive`, `leverage`, `unlock`, `empower`, `harness`, `crucial` (overused), `notably` (overused), `moreover` (overused). Replace with concrete mechanisms or delete.
- [ ] **Kill meta-signposting:** Remove *"In this section we will discuss..."*, *"As we will see in Section 5..."*, *"To summarize what we have shown so far..."* unless a forward pointer genuinely prevents confusion.
- [ ] **One idea per paragraph:** Split any paragraph longer than ~8 lines in rendered PDF; merge 1-sentence orphan paragraphs unless used intentionally for emphasis.

## Pass 3: Reviewer-2 Methodology Attack
Play the toughest fair reviewer at NeurIPS/ICLR and try to break your own paper:
- [ ] **Strongest baseline:** Is there a simpler baseline (frozen model, replay, retrieval, linear probe, matched-compute random search) that explains the gain? If it is missing, either run it or explicitly scope the claim.
- [ ] **Budget parity:** Are FLOPs, trainable parameters, persistent bytes, wall time, and auxiliary queries (probes, teacher calls, retrieval context) accounted for on the *same* footing?
- [ ] **No data/chronology leakage:** In continual/stream settings, confirm predict-before-score, no future access, no regime-ID leakage, and held-out stream seeds/entities.
- [ ] **Statistical discipline:** Are CIs computed over **independent streams/seeds** (the true replicate), not over individual steps or tokens? Are noisy intervals called inconclusive rather than wins?
- [ ] **Ablation isolation:** Does each ablation block change *one* variable relative to `base`? Does the mechanism analysis actually rule out the main alternative explanation?
- [ ] **Honest limitations:** Are failure regimes, compute assumptions, and scope boundaries stated plainly in Discussion/Conclusion?

## Pass 4: Notation, Citations & Reproducibility Check
- [ ] **Symbol consistency:** Every variable has one meaning across text, equations, figures, and tables. Every symbol is defined on or before first use.
- [ ] **Citation integrity:** Every `\cite`/`\citep`/`\citet` key resolves in `references.bib`, and **every cited paper is verified** (exact authors, title, venue/arXiv ID, year—never guessed from memory).
- [ ] **Reproducibility details:** Exact datasets/simulators, model checkpoints, commit hash or code URL, optimizer/schedule, seeds, and hardware/wall time are reported (main text or Appendix).

## Pass 5: Visual & Typesetting QA
After compiling the PDF (see `paper-latex-and-publish`):
- [ ] Zero LaTeX errors, zero undefined references (`??`), zero undefined citations.
- [ ] Zero overfull `\hbox` warnings > 5pt (no text or equations spilling into margins).
- [ ] Render **every page** to PNG (using `pdftoppm` or `pypdfium2` per `paper-latex-and-publish`) and visually inspect them with the `read` tool:
  - Check Figure 1 placement (page 1 or top of page 2).
  - Check that all figure axis labels, tick marks, and legends are legible at 100% zoom.
  - Check that no table overflows the text width or wraps awkwardly.
  - Check for orphan section headings at page bottoms or awkward half-empty pages.
