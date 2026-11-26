"""Build the paper's vector plot and TeX results from saved experiment output."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
RESULTS = HERE.parents[1] / "experiments" / "self_branching_skills" / "results.json"
LABELS = {
    "average": "Pooled ascent",
    "maxmin": "Shared MaxMin",
    "fixed_two": "Fixed two / affine",
    "adaptive": "Adaptive branch",
    "oracle": "Cohort oracle",
}
COLORS = {"adaptive": "#0072B2", "maxmin": "#D55E00", "fixed_two": "#009E73", "oracle": "#222222"}
STYLES = {"adaptive": "-", "maxmin": ":", "fixed_two": "-.", "oracle": "--"}


def plot(report):
    plt.rcParams.update({
        "font.family": "serif", "font.size": 9, "axes.spines.top": False,
        "axes.spines.right": False, "pdf.fonttype": 42, "lines.linewidth": 1.4,
    })
    fig, (utility, slots) = plt.subplots(
        2, 1, sharex=True, figsize=(6.5, 2.40), layout="constrained",
        gridspec_kw={"height_ratios": [2, 1]})
    for ax in (utility, slots):
        for phase, start, stop in report["design"]["phases"]:
            if phase in ("conflict", "reversal"):
                ax.axvspan(start, stop, color="#E7ECF1", zorder=0)
        ax.grid(axis="y", color="#D4D7DA", linewidth=.5)
        ax.set_xlim(0, 5000)
    for name, color in COLORS.items():
        points = report["curves"][name]
        x = np.array([int(step) for step in points]) + report["design"]["bin_width"] / 2
        for ax, metric in [(utility, "utility"), (slots, "slots")]:
            mean, low, high = np.array([p[metric] for p in points.values()]).T
            ax.plot(x, mean, ls=STYLES[name], color=color, label=LABELS[name])
            ax.fill_between(x, low, high, color=color, alpha=.15, linewidth=0)
    utility.set_ylabel("Mean utility")
    utility.set_yticks([.2, .6, 1])
    utility.legend(loc="lower center", bbox_to_anchor=(.5, 1.0), ncols=4,
                   fontsize=8, frameon=False, handlelength=2.2)
    slots.set_ylabel("Live skills")
    slots.set_yticks([1, 2])
    slots.set_ylim(.92, 2.08)
    slots.set_xlabel("Stream step")
    fig.savefig(HERE / "timeline.pdf")


def value(interval, places=3, bold=False):
    mean, low, high = interval
    point = f"{mean:.{places}f}"
    return (r"\mathbf{" + point + "}" if bold else point) + f"\\pm{(high-low)/2:.{places}f}"


def probability(interval):
    mean, low, high = interval
    return f"{100*mean:.0f} [{100*low:.0f}, {100*high:.0f}]"


def tables(report):
    table = report["tables"]
    first = {m: s["conflict"] for m, s in table["routable"].items()}
    lines = []
    for method, name in LABELS.items():
        if method == "oracle":
            lines.append(r"\midrule")
        cells = [value(first[method][key], bold=first[method][key][0] == max(
                  first[m][key][0] for m in LABELS if m != "oracle")) for key in ("a", "b", "worst")]
        slots = value(table["routable"][method]["all"]["slots"], places=2)
        lines.append(" & ".join([name, *[f"${x}$" for x in cells], f"${slots}$"]) + r" \\")
    (HERE / "table_main.tex").write_text("\n".join(lines) + "\n")

    lines = []
    paired = report["paired_worst"]
    for condition, name in [
        ("routable", "Routable"), ("weak_cue", "(A) Weaker cue"),
        ("hidden", "(A) Uninformative cue"), ("single_hill", "(B) One hill")]:
        estimate = table[condition]["adaptive"]["conflict"]
        first_delta = value(paired[condition]["conflict_vs_maxmin"])
        delay = estimate["split_delay"]
        cells = [
            name, f'{report["design"]["cue_accuracy"][condition]:.2f}' if condition != "single_hill" else "",
            f"${first_delta}$", probability(estimate["split_rate"]),
            f"${value(delay, places=0)}$" if delay else "---",
        ]
        lines.append(" & ".join(cells) + r" \\")
    (HERE / "table_cue.tex").write_text("\n".join(lines) + "\n")

    adaptive = table["routable"]["adaptive"]
    lines = []
    for phase, mode, name in [
        ("conflict", "split", "First fork"),
        ("rejoin", "merge", "Rejoin"),
        ("reversal", "split", "Second fork"),
    ]:
        estimate = adaptive[phase]
        cells = [name, probability(estimate[f"{mode}_rate"]),
                 f"${value(estimate[f'{mode}_delay'], places=0)}$",
                 *[f"${value(estimate[key])}$" for key in ("a", "b", "worst")]]
        lines.append(" & ".join(cells) + r" \\")
    (HERE / "table_transitions.tex").write_text("\n".join(lines) + "\n")


def main():
    report = json.loads(RESULTS.read_text())
    plot(report)
    tables(report)
    print("Generated timeline.pdf and 3 result tables")


if __name__ == "__main__":
    main()
