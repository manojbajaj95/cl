---
name: paper-figures-and-tables
description: "Design publication-grade tables, figures, and self-contained captions in landmark ML paper style (booktabs, cost-alongside-quality comparisons, blank-means-base ablations, and reproducible vector plots from saved run artifacts)."
---

# Paper Figures and Tables (Landmark ML Style)

Use this skill whenever designing tables, plots, architecture diagrams, or captions for a research paper. Grounded in the visual and tabular conventions of *Attention Is All You Need* (`1706.03762`), *ResNet* (`1512.03385`), *LoRA* (`2106.09685`), *DDPM* (`2006.11239`), and *Chinchilla* (`2203.15556`), and aligned with the `manojbajaj95/cl` stream-contract budget reporting.

## 1. The Four Essential Table Archetypes

Always use LaTeX `booktabs` (`\toprule`, `\midrule`, `\bottomrule`). **Never use vertical rules** (`|`) or double horizontal rules (`\hline\hline`). Align text left (`l`), numbers right or decimal-aligned (`r` or `c`), with consistent decimal places per column.

### A. Design-Axes Comparison Table (e.g. Transformer Table 1)
Use early (Section 2 or 4) to compare your primitive against prior classes on 3–4 quantitative axes (complexity, memory, latency, path length, identifiability).
```latex
\begin{table}[t]
\centering
\caption{\textbf{Per-step cost and structural properties across update classes.}
$n$: stream horizon, $d$: representation dimension, $r$: adapter rank, $k$: active slots.}
\label{tab:axes}
\begin{tabular}{lccc}
\toprule
Mechanism & Update Cost & Persistent Bytes & Rollback Exact? \\
\midrule
Full fine-tuning & $O(d^2)$ & $O(d^2)$ & No \\
Replay buffer & $O(k \cdot d^2)$ & $O(k \cdot n)$ & Approximate \\
Proposed method & $O(r \cdot d)$ & $O(r \cdot d)$ & Yes \\
\bottomrule
\end{tabular}
\end{table}
```

### B. Main Results Table — Quality Alongside Cost (e.g. Transformer Table 2, LoRA Table 2)
Never report quality without its matched budget. Put the budget column (FLOPs, trainable params, wall time, or persistent bytes) in the **same table**. Separate baselines, our method, and oracles/upper bounds with `\midrule`. Bold the best **non-oracle** entry per column; include paired CIs or mean $\pm$ std over independent streams/seeds.

### C. Lettered Single-Variable Ablation Table (e.g. Transformer Table 3)
Put the `base` row at the top. Group ablations into lettered blocks `(A)`, `(B)`, `(C)`—one conceptual question per block—and **leave unchanged cells blank** so the reader's eye jumps immediately to what varied.
```latex
\begin{table}[t]
\centering
\caption{\textbf{Ablations on the base configuration.} Unlisted cells match the
\texttt{base} row. Metrics are mean $\pm$ 95\% paired CI over $S=5$ held-out streams.}
\label{tab:ablations}
\begin{tabular}{llcccc}
\toprule
& Variant & $r$ & $\lambda$ & Retention $\Delta$ ($\uparrow$) & Latency ($\downarrow$) \\
\midrule
& \texttt{base} & 8 & 0.1 & $-0.4 \pm 0.2$ & $14.2 \pm 1.1$ \\
\midrule
(A) & Rank sweep & 2 & & $-0.3 \pm 0.2$ & $21.8 \pm 2.0$ \\
    &            & 16 & & $-1.1 \pm 0.4$ & $13.9 \pm 1.0$ \\
\midrule
(B) & No probe gate & & 0.0 & $-4.6 \pm 0.8$ & $12.5 \pm 1.3$ \\
\bottomrule
\end{tabular}
\end{table}
```

### D. Mechanism / Diagnostic Table (e.g. LoRA Table 5)
Hold budget strictly fixed (state it in a spanning header, e.g. `\multicolumn{5}{c}{Budget = 18M Trainable Params}`) and vary *where* or *how* the budget is spent.

## 2. Publication-Grade Figures

### Reproducibility Rule
- Generate every data figure from a **standalone plotting script** that reads saved JSONL/CSV run artifacts—never hand-typed arrays or manual screenshots.
- Export vector **PDF** (`fig.savefig("figures/fig1.pdf", bbox_inches="tight")`) for plots and diagrams; use 300+ DPI PNG only for raster heatmaps/images.

### Visual Design Standards
- **Page-1 Teaser Figure:** Put your architecture diagram (Transformer Fig. 1, LoRA Fig. 1) or core empirical anomaly/scaling curve (ResNet Fig. 1, Chinchilla Fig. 1) on page 1 or top of page 2.
- **Typography at print scale:** Set figure width to actual LaTeX column/text width (`3.25 in` single-column, `6.5 in` full-width) so fonts render at **8–10 pt** without rescaling distortion.
- **Colorblind-safe palette (Okabe–Ito):** `#0072B2` (blue), `#D55E00` (vermilion), `#009E73` (bluish green), `#CC79A7` (reddish purple), `#E69F00` (orange), `#56B4E9` (sky blue), `#000000` (black/oracle dashed).
- **Minimal chart junk:** Remove top and right spines; use subtle light-gray gridlines (`alpha=0.25`); prefer direct curve labels or a single compact legend outside/top; never overlap text with curves.
- **Show uncertainty honestly:** Plot shaded 95% CIs (or IQR) across paired streams/seeds, and for $S \le 10$ streams show faint individual stream traces (`alpha=0.2`) behind the mean curve.
- **Reference baselines & oracles:** Draw the no-change control and oracle as thin dashed horizontal lines (`ls="--"`) labeled directly on the plot.

### Reusable Matplotlib Style Snippet
```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 9.5,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "grid.linestyle": "--",
    "lines.linewidth": 1.6,
    "pdf.fonttype": 42,   # embed TrueType fonts cleanly
    "ps.fonttype": 42,
})
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
```

## 3. Self-Contained Captions

A reader skimming only the figures and tables should grasp the entire paper's story. Every caption follows a 3-part formula:
1. **Bold declarative takeaway** (1 sentence): State *what the reader should conclude*, not just what is plotted.
   - Good: `\textbf{The Transformer achieves higher BLEU at a fraction of the training FLOPs.}`
   - Bad: `Results on WMT 2014.`
2. **Protocol & metric specifics** (1–2 sentences): Dataset/stream, number of paired streams/seeds ($S=5$), error bar meaning (95% paired bootstrap CI), direction arrows ($\uparrow$ higher is better, $\downarrow$ lower is better).
3. **Symbol / line legend** (if not obvious): Define any abbreviations or blank-cell conventions right in the caption.
