---
name: paper-latex-and-publish
description: "Compile a clean arXiv/NeurIPS-style LaTeX paper PDF, run automated LaTeX and visual QA checks, and publish to alphaXiv AI Track with accurate metadata and AI disclosure."
---

# Paper LaTeX Build, QA, and alphaXiv Publish

Use this skill to set up, compile, inspect, and publish a paper PDF to alphaXiv's AI Track from `manojbajaj95/cl`.

## 1. Starting from the Preprint Template

Copy the clean preprint template from this skill's `templates/` directory into your paper directory (e.g. `papers/<slug>/`):
- `templates/paper.tex` — clean single-column arXiv/NeurIPS-style preprint (`geometry`, `microtype`, `booktabs`, `amsmath`, `amssymb`, `hyperref`, `cleveref`, `natbib`, `algorithm`/`algpseudocode`, clean title/author header).
- `templates/references.bib` — sample BibTeX structure.

For papers longer than ~5 pages, split sections into `sections/intro.tex`, `sections/method.tex`, `sections/experiments.tex`, etc., and `\input{...}` them from `paper.tex` (matching *Attention Is All You Need*'s `ms.tex` layout).

## 2. Clean Compilation & Automated Log Audit

Compile with `latexmk` (preferred) or `pdflatex` + `bibtex`:
```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex
```
Or without `latexmk`:
```bash
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
bibtex paper
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

Immediately run a log audit — **do not ship with unresolved references or bad boxes**:
```bash
grep -E "Undefined|Multiply defined|Citation .* undefined|Reference .* undefined|Overfull \\\\hbox" paper.log || echo "CLEAN"
```
Fix every undefined citation/reference (`??`) and any `Overfull \hbox` wider than ~5pt (shorten table columns, use `\resizebox{\linewidth}{!}{...}` only as a last resort, or break long equations with `align`).

## 3. Mandatory Visual Inspection

Never publish a PDF without looking at the rendered pages. Render each page to PNG (`pdftoppm` if installed; otherwise `pypdfium2` installs cleanly without root):
```bash
mkdir -p /tmp/pdf_preview && rm -f /tmp/pdf_preview/page-*.png
if command -v pdftoppm >/dev/null 2>&1; then
  pdftoppm -png -r 150 paper.pdf /tmp/pdf_preview/page
else
  python3 -c 'import pypdfium2' 2>/dev/null || python3 -m pip install -q pypdfium2
  python3 -c '
import pypdfium2 as pdfium
doc = pdfium.PdfDocument("paper.pdf")
for i, page in enumerate(doc, 1):
    page.render(scale=2.0).to_pil().save(f"/tmp/pdf_preview/page-{i:02d}.png")
'
fi
ls -la /tmp/pdf_preview/
```
Inspect every rendered page PNG with the `read` tool:
- Verify title/author/abstract alignment on page 1.
- Verify Figure 1 appears early (page 1 or top of page 2) with crisp vector text and no overlapping labels.
- Verify tables align cleanly within margins and use `booktabs` spacing.
- Verify equations do not collide with equation numbers.
- Verify bibliography renders cleanly with no missing years, broken LaTeX escapes, or raw underscores.

## 4. Publishing to alphaXiv AI Track

Before publishing, verify you have run `paper-review-and-tighten` and that every number matches your saved experiment logs.

### Step 1: Upload the compiled PDF (max 50 MB)
```bash
curl -sS -X POST 'https://api.alphaxiv.org/papers/v3/submissions/pdf-uploads' \
  -H 'Content-Type: application/pdf' \
  --data-binary @paper.pdf
```
Capture the returned `{"pdfId": "<uuid>"}`.

### Step 2: Call `publish_paper` on MCP `alphaxiv-992d`
Call `mcp_call_tool(server="alphaxiv-992d", tool_name="publish_paper", tool_args=...)` with:
- `pdf_id`: the UUID returned in Step 1.
- `title`, `abstract`, `authors`: omit to read from PDF, or pass exact strings matching the PDF (`authors: []` if no human authors; include human co-authors only when truthful).
- `url_slug`: short kebab-case slug derived from the title (e.g. `probe-before-write-shift-isolation`).
- `ai_disclosure`: **always truthful, never fabricated**:
  - `stages`: `{idea, literature, experiments, analysis, writing}` — each one of `"ai"`, `"mixed"`, or `"human"`.
  - `tools`: list of `{model, harness, contribution}` objects accurately naming the model(s) and harness (e.g. `"Devin"`) used and what each did.
- For a revision of an existing alphaXiv paper, pass `new_version_of` with the existing alphaXiv URL or ID.

### Step 3: Record the Result
- If `publish_paper` returns a published URL, record the URL, PDF commit SHA, and experiment artifact paths in the PR description / session summary.
- If `publish_paper` returns a rejection with a reason, fix the stated issue, recompile, visually re-inspect, and resubmit.
- Never fabricate citations, experiment numbers, authors, or AI disclosure fields.
