"""Generate the paper's vector figure from the saved seed-level sweep."""

import json
from pathlib import Path

import matplotlib
import numpy as np
from scipy.stats import t as student_t

matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = Path(__file__).resolve().parent
PALETTE = ("#0072B2", "#D55E00", "#009E73", "#CC79A7")
STYLES = ("-", "--", "-.", ":")


def main():
    data = json.loads((HERE / "../../experiments/waterbed/results.json").read_text())
    runs = data["runs"]
    omega = np.asarray(runs["omega"])
    primary = np.asarray(runs["gain"])[:, :, 0, :]
    normalized = primary / np.asarray(runs["one_step_gain"])[..., None]
    count = len(primary)
    critical = student_t.ppf(0.975, count - 1)

    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "grid.alpha": 0.25,
        "grid.linestyle": "--",
        "pdf.fonttype": 42,
    })
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.45), sharex=True)
    fig.subplots_adjust(left=0.10, right=0.995, bottom=0.2, top=0.78, wspace=0.28)
    labels = ("GD (slow)", "GD (fast)", "Replay", "EWC")
    for ax, values, ylabel in zip(
        axes, (primary, normalized), ("Old-task loss gain", "Gain / one-step gain")
    ):
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Frequency (radians / update)")
        ax.grid()
        for idx, (label, color, style) in enumerate(zip(labels, PALETTE, STYLES)):
            logs = np.log(values[:, idx])
            mean = logs.mean(axis=0)
            half = critical * logs.std(axis=0, ddof=1) / np.sqrt(count)
            ax.fill_between(omega, np.exp(mean - half), np.exp(mean + half), color=color, alpha=0.13)
            for trace in values[:, idx]:
                ax.plot(omega, trace, color=color, linewidth=0.6, alpha=0.20)
            ax.plot(omega, np.exp(mean), style, label=label, color=color, linewidth=1.7)
    handles, legend_labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, legend_labels, loc="upper center", ncol=4, frameon=False)
    fig.savefig(HERE / "spectra.pdf", metadata={"CreationDate": None, "ModDate": None})
    plt.close(fig)
    print(f"Plotted {len(labels)} arms, {count} seeds and {len(omega)} frequencies from results.json.")


if __name__ == "__main__":
    main()
