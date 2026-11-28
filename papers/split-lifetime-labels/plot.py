import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
RESULT = HERE.parents[1] / "experiments" / HERE.name / "results.json"
ARMS = {
    "split": ("Split labels", "#0072B2", "o", "-"),
    "whole": ("Whole-label refresh", "#D55E00", "s", "--"),
    "pav": ("Memoized PAV", "#009E73", "^", "-"),
    "carry": ("Carry v1", "#333333", None, ":"),
}


def make_figure(result):
    mpl.rcParams.update({
        "font.family": "serif", "font.size": 9, "axes.spines.top": False,
        "axes.spines.right": False, "grid.alpha": 0.25, "pdf.fonttype": 42,
    })
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.45), sharey=True, layout="constrained")
    for ax, (release, subtitle) in zip(axes, [("A", "+6 move"), ("B", "−5 move")], strict=True):
        rows = result["summary"][release]["by_cap"]
        caps = list(rows)
        index = np.arange(len(caps))
        ax.axvline(1, color="0.8", linewidth=1)
        for arm, (name, color, marker, style) in ARMS.items():
            y, lo, hi = np.array([rows[cap]["accuracy_pp"][arm] for cap in caps]).T
            ax.plot(index, y, label=name, color=color, marker=marker, ms=3, ls=style)
            ax.fill_between(index, lo, hi, color=color, alpha=0.10, linewidth=0)
        ax.set_title(f"Release {release}: {subtitle}")
        ax.set_xticks(index, caps)
        ax.set_xlabel("Operation cap per upgraded board")
        ax.grid(axis="y")
    axes[0].set_ylabel("Exact joint labels (%)")
    fig.legend(*axes[0].get_legend_handles_labels(), loc="outside upper center",
               ncol=len(ARMS), frameon=False)
    fig.savefig(HERE / "accuracy.pdf", metadata={"CreationDate": None})


def make_tables(result):
    rows = result["summary"]["A"]["by_cap"]["96"]
    lines = []
    for arm, (name, *_style) in ARMS.items():
        p, lo, hi = rows["accuracy_pp"][arm]
        work = rows["mean_per_upgraded_board"][arm]
        estimate = f"{p:.2f}"
        if arm == "pav":
            estimate = rf"\textbf{{{estimate}}}"
        lines.append(
            f"{name} & {estimate} [{lo:.2f}, {hi:.2f}] & {work['operations']:.2f}"
            f" & {work['guards']:.2f} & {work['validity']:.2f} & {work['continuation']:.2f}"
            + r" \\"
        )
    (HERE / "table_accuracy.tex").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    data = json.loads(RESULT.read_text())
    make_figure(data)
    make_tables(data)
