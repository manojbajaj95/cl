"""Generate the paper's figures and tables from the saved seed-level sweep."""

import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "../../experiments/dirty_paper/results.json").read_text())
ARMS = ("GPM", "OWM", "GPM-GD", "VP", "VP-joint")
LABELS = {"GPM": "GPM", "OWM": "OWM", "GPM-GD": "GPM + modular GD", "VP": "Dirty-paper (A-null)", "VP-joint": "Dirty-paper (joint)"}
COLORS = {"GPM": "#7f7f7f", "OWM": "#CC79A7", "GPM-GD": "#0072B2", "VP": "#D55E00", "VP-joint": "#009E73"}
STYLES = {"GPM": ":", "OWM": "-.", "GPM-GD": "--", "VP": "-", "VP-joint": "-"}


def style():
    plt.rcParams.update({
        "font.family": "serif", "font.size": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
        "legend.fontsize": 8, "axes.spines.top": False, "axes.spines.right": False,
        "grid.alpha": 0.25, "grid.linestyle": "--", "pdf.fonttype": 42,
    })


def budget_figure():
    S = DATA["summary"]["theta30_S0"]
    b = np.asarray(DATA["parameters"]["budgets"])
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.5), sharex=True)
    fig.subplots_adjust(left=0.09, right=0.995, bottom=0.19, top=0.80, wspace=0.25)
    for ax, key, ylabel in zip(axes, ("acc_b", "acc_a"), ("New-task (B) accuracy", "Old-task (A) accuracy")):
        ax.set_xscale("log")
        ax.grid()
        ax.set_xlabel("Update norm / GPM exact-write norm")
        ax.set_ylabel(ylabel)
        ax.axhline(1 / DATA["parameters"]["M"], color="k", linewidth=0.6, alpha=0.4)
        for a in ARMS:
            v = np.asarray(S[key][a])
            ax.fill_between(b, v[:, 1], v[:, 2], color=COLORS[a], alpha=0.13, linewidth=0)
            ax.plot(b, v[:, 0], STYLES[a], color=COLORS[a], linewidth=1.6, label=LABELS[a])
        ax.set_ylim(0, 1.03)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=5, frameon=False, columnspacing=1.0, handlelength=2.2)
    fig.savefig(HERE / "budget.pdf")


def decay_figure():
    S = DATA["seeds"]["theta30_S0"]
    f = np.asarray(DATA["parameters"]["decay"])
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 2.3), sharex=True, sharey=True)
    fig.subplots_adjust(left=0.09, right=0.995, bottom=0.21, top=0.80, wspace=0.12)
    for ax, key, title in zip(axes, ("decay_b", "decay_a"), ("New task B", "Old task A")):
        ax.set_xscale("log")
        ax.grid()
        ax.set_title(title, fontsize=9)
        ax.set_xlabel(r"Weight shrink after the write, $\gamma$")
        ax.set_xlim(1e-2, 0.3)
        for a in ("GPM", "GPM-GD", "VP", "VP-joint"):
            v = np.asarray([r[key][a] for r in S])
            m = v.mean(0)
            h = 2.131 * v.std(0, ddof=1) / np.sqrt(len(v))
            ax.fill_between(f, m - h, m + h, color=COLORS[a], alpha=0.13, linewidth=0)
            ax.plot(f, m, STYLES[a], color=COLORS[a], linewidth=1.6, label=LABELS[a])
    axes[0].set_ylabel("Accuracy")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=4, frameon=False)
    fig.savefig(HERE / "decay.pdf")


def fmt(v, d=2):
    return f"{v[0]:.{d}f} [{v[1]:.{d}f}, {v[2]:.{d}f}]"


def tables():
    P = DATA["parameters"]
    rows = []
    for sp in P["spreads"]:
        for th in P["thetas"]:
            S = DATA["summary"][f"theta{th}_S{sp}"]
            g = S["required_over_gpmgd"]
            rows.append(f"{th}$^\\circ$ & {sp} & {fmt(g['GPM'])} & {fmt(g['VP'])} & {fmt(g['VP-joint'])} & "
                        f"{fmt(S['vp_over_clean_vp'])} & {fmt(S['dpc_minus_gpm_pp'], 1)} & {fmt(S['switch_minus_gpmgd_pp'], 1)} \\\\")
        rows.append("\\addlinespace")
    (HERE / "table_main.tex").write_text("\n".join(rows[:-1]) + "\n")

    S = DATA["summary"]["theta30_S0"]
    lines = []
    for a in ("FT", "GPM", "OWM", "GPM-GD", "THP", "VP", "VP-joint"):
        name = {"FT": "Unprojected (FT)", "THP": "Dirty-paper (THP)"}.get(a, LABELS.get(a, a))
        jj = int(np.argmin(np.abs(np.asarray(P["budgets"]) - 0.445)))
        lines.append(f"{name} & {fmt(S['required_over_gpm'][a])} & {fmt(S['acc_b'][a][jj])} & {fmt(S['acc_a'][a][jj])} & "
                     f"{fmt(S['decay_half_life_a'][a], 3)} & {fmt(S['decay_half_life_b'][a], 3)} \\\\")
    (HERE / "table_arms.tex").write_text("\n".join(lines) + "\n")

    mac = []
    def m(name, v):
        mac.append(f"\\newcommand{{\\{name}}}{{{v}}}")
    allv = [DATA["summary"][k] for k in DATA["summary"]]
    vpg = [s["required_over_gpmgd"]["VP"][0] for s in allv]
    vjg = [s["required_over_gpmgd"]["VP-joint"][0] for s in allv]
    cl = [s["vp_over_clean_vp"][0] for s in allv]
    gc = [s["gpm_over_clean_gpm"][0] for s in allv]
    m("vpgdmin", f"{min(vpg):.2f}"); m("vpgdmax", f"{max(vpg):.2f}")
    m("vjgdmin", f"{min(vjg):.2f}"); m("vjgdmax", f"{max(vjg):.2f}")
    m("cleanmin", f"{min(cl):.2f}"); m("cleanmax", f"{max(cl):.2f}")
    m("gpmcleanmax", f"{max(gc):.1f}")
    gd4 = [DATA["summary"][f"theta{t}_S4"]["required_over_gpm"]["GPM-GD"][0] for t in P["thetas"]]
    m("gdgpmSfourmin", f"{min(gd4):.2f}"); m("gdgpmSfourmax", f"{max(gd4):.2f}")
    d = S["dpc_minus_gpm_pp"]; m("mainDelta", f"{d[0]:.2f}"); m("mainDeltaLo", f"{d[1]:.2f}"); m("mainDeltaHi", f"{d[2]:.2f}")
    d = S["vp_minus_gpmgd_pp"]; m("mainVPGD", f"{d[0]:.2f}"); m("mainVPGDLo", f"{d[1]:.2f}"); m("mainVPGDHi", f"{d[2]:.2f}")
    deltas = [DATA["summary"][k]["dpc_minus_gpm_pp"] for k in DATA["summary"]]
    m("maxDeltaHi", f"{max(x[2] for x in deltas):.2f}")
    m("bestDelta", f"{max(x[0] for x in deltas):.2f}")
    m("nkilled", str(sum(DATA["summary"][k]["killed"] for k in DATA["summary"])))
    m("nconfigs", str(len(DATA["summary"])))
    m("nseeds", str(len(P["seeds"])))
    m("runtime", f"{DATA['runtime_s'] / 60:.0f}")
    jmin = min(DATA["summary"]["theta30_S0"]["acc_a"]["VP-joint"], key=lambda v: v[0])
    m("jointAmin", f"{100 * jmin[0]:.0f}")
    hl = S["decay_half_life_a"]
    m("hlAgpm", f"{hl['GPM'][0]:.3f}"); m("hlAjoint", f"{hl['VP-joint'][0]:.3f}")
    hb = [DATA["summary"][f"theta{t}_S4"]["decay_half_life_b"]["VP"][0] for t in P["thetas"]]
    m("hlBvpSfourmax", f"{max(hb):.3f}")
    m("cvpexact", f"{min(min(s['cvp_exact']) for s in allv):.2f}")
    sw = [s["switch_minus_gpmgd_pp"] for s in allv]
    m("swmin", f"{min(x[0] for x in sw):.2f}"); m("swmax", f"{max(x[0] for x in sw):.2f}")
    m("swlomin", f"{min(x[1] for x in sw):.2f}")
    sww = [s["switch_minus_gpmgd_window_pp"][0] for s in allv]
    m("swwmin", f"{min(sww):.1f}"); m("swwmax", f"{max(sww):.1f}")
    m("swAmin", f"{min(s['switch_min_acc_a'] for s in allv):.2f}")
    hard = DATA["summary"]["theta15_S4"]["dpc_minus_gpm_pp"]
    m("hardDelta", f"{hard[0]:.2f}"); m("hardDeltaLo", f"{hard[1]:.2f}"); m("hardDeltaHi", f"{hard[2]:.2f}")
    owm = DATA["summary"]["theta30_S0"]["acc_a"]["OWM"]
    m("owmAmin", f"{100 * min(v[0] for v in owm):.0f}")
    (HERE / "numbers.tex").write_text("\n".join(mac) + "\n")


if __name__ == "__main__":
    style()
    budget_figure()
    decay_figure()
    tables()
