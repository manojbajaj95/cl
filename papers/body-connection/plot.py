"""Figure and tables for the body-connection paper from saved run artifacts."""

import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
EXP = HERE.parent.parent / "experiments" / "body_connection"
R = json.loads((EXP / "mechanism_results.json").read_text())["results"]
FAMS = ["curved", "contact", "mixed"]
NS = [300, 1200, 4800, 19200]

mpl.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
    "grid.alpha": 0.25, "grid.linestyle": "--", "lines.linewidth": 1.6, "pdf.fonttype": 42, "ps.fonttype": 42,
})
STYLE = {
    "Gamma_oracle": ("Oracle connection", "#000000", "--"),
    "EB12_oracle": ("Oracle affine map", "#56B4E9", "--"),
    "EB12": ("Learned affine (EB12)", "#0072B2", "-"),
    "Gamma_RFF": ("Learned $\\Gamma$", "#D55E00", "-"),
    "Gamma_gated": ("Gated $\\Gamma$", "#CC79A7", ":"),
    "GAT_MLP": ("GAT-MLP", "#009E73", "-"),
}


def cell(cfg, fam, arm, key="s5_heldout_return"):
    return R[cfg][fam][key][arm]


fig, axes = plt.subplots(1, 3, figsize=(6.5, 2.3), sharey=False)
for ax, fam in zip(axes, FAMS):
    for arm, (lab, col, ls) in STYLE.items():
        m = [cell(f"N{n}_noise0.01", fam, arm)["mean"] for n in NS]
        se = [cell(f"N{n}_noise0.01", fam, arm)["se"] for n in NS]
        ax.plot(NS, m, color=col, ls=ls, marker="o", ms=3, label=lab)
        ax.fill_between(NS, [a - 1.96 * b for a, b in zip(m, se)], [a + 1.96 * b for a, b in zip(m, se)], color=col, alpha=0.12, lw=0)
    ax.set_xscale("log")
    ax.set_xticks(NS)
    ax.set_xticklabels(["300", "1.2k", "4.8k", "19.2k"])
    ax.set_title(fam, fontsize=9)
    ax.set_xlabel("ritual samples per body $N$")
axes[0].set_ylabel("held-out S5 return")
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.13))
fig.tight_layout()
fig.savefig(HERE / "budget.pdf", bbox_inches="tight")


def fmt(d, bold=False):
    s = f"{d['mean']:.3f} $\\pm$ {1.96 * d['se']:.3f}"
    return f"\\textbf{{{s}}}" if bold else s


# Main table: N=1200 (the PR #418 budget) and N=19200, 1% noise.
arms = ["Gamma_oracle", "EB12_oracle", "EB12", "Gamma_RFF", "Gamma_gated", "GAT_MLP", "NoTransport"]
names = {**{a: v[0] for a, v in STYLE.items()}, "NoTransport": "No transport"}
lines = []
for a in arms:
    row = [names[a]]
    for cfg in ["N1200_noise0.01", "N19200_noise0.01"]:
        for fam in FAMS:
            row.append(fmt(cell(cfg, fam, a)))
    lines.append(" & ".join(row) + r" \\")
    if a == "EB12_oracle":
        lines.append(r"\midrule")
(HERE / "table_main.tex").write_text("\n".join(lines) + "\n")

# Paired gaps table across the sweep.
pairs = [("Gamma_oracle-EB12", "Oracle $-$ EB12"), ("Gamma_RFF-EB12", "$\\Gamma$ $-$ EB12"),
         ("Gamma_gated-GAT_MLP", "Gated $\\Gamma$ $-$ GAT"), ("Gamma_RFF-Gamma_oracle", "$\\Gamma$ $-$ oracle")]
cfgs = [("N300_noise0.01", "300", "1\\%"), ("N1200_noise0.01", "1200", "1\\%"), ("N4800_noise0.01", "4800", "1\\%"),
        ("N19200_noise0.01", "19200", "1\\%"), ("N1200_noise0", "1200", "0\\%"), ("N19200_noise0", "19200", "0\\%")]
lines = []
for cfg, n, nz in cfgs:
    row = [n, nz]
    for fam in ["curved", "contact"]:
        for key, _ in pairs[:3]:
            p = R[cfg][fam]["paired"][key]
            row.append(f"{p['mean_diff']:+.3f} ({p['gap_in_se']:+.1f})")
        row.append(f"{R[cfg][fam]['retention_s1_s4_return']['Gamma_gated']['mean']:.2f}")
    lines.append(" & ".join(row) + r" \\")
    if cfg == "N19200_noise0.01":
        lines.append(r"\midrule")
(HERE / "table_sweep.tex").write_text("\n".join(lines) + "\n")
print("ok")
