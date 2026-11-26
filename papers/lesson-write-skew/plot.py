"""Regenerate the vector figure and LaTeX result artifacts."""
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
EXPERIMENT = HERE.parents[1] / "experiments" / "write_skew"
COUNTS = np.array([0, 1, 1, 2, 1, 2, 2, 3])
ARM_STYLE = {"focal": ("#0072B2", "-", "Focal"), "control": ("#D55E00", "--", "Disjoint")}


def plot(summary):
    matplotlib.rcParams.update({
        "font.family": "serif", "font.size": 9, "axes.titlesize": 10,
        "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42,
    })
    fig, (left, right) = plt.subplots(1, 2, figsize=(6.5, 2.35), layout="constrained")
    counts = np.arange(4)
    wording = summary["by_wording"][0]
    rng = np.random.default_rng(832)
    n = summary["holdout_n"]
    bootstrap = rng.integers(0, n, size=(10000, n))
    for arm, (color, style, label) in ARM_STYLE.items():
        cube = np.asarray([store["margins"] for store in wording["stores"][arm]])
        delta = cube - cube[:, :1]
        curve = np.column_stack([delta[:, COUNTS == k].mean(axis=1) for k in counts])
        lo, hi = np.quantile(curve[bootstrap].mean(axis=1), [.025, .975], axis=0)
        left.plot(counts, curve.mean(axis=0), style, marker="o", ms=3, color=color, label=label)
        left.fill_between(counts, lo, hi, color=color, alpha=.15, linewidth=0)
    left.plot(counts, wording["count_curve"], ":", color="black", label="Separate count fit")
    left.set(xlabel="Active new rules", ylabel="Old margin change (logits)", xticks=counts,
             title="A. Margin by active count")
    left.legend(frameon=False, fontsize=8, loc="best")

    witness = wording["arms"]["focal"]["strict_seeds"][0]
    masks = r"$\varnothing$", "B", "C", "D", "BC", "BD", "CD", "BCD"
    order = [0, 1, 2, 4, 3, 5, 6, 7]
    right.axhline(0, color=".45", linewidth=.75, linestyle=":", zorder=0)
    for i, phrasing in enumerate(summary["by_wording"]):
        store = next(s for s in phrasing["stores"]["focal"] if s["seed"] == witness)
        signed = np.asarray(store["all_rival_min"])[order]
        right.plot(np.arange(8), signed, ("o-", "s--")[i], ms=3, color=("#0072B2", "#009E73")[i],
                   label=f"Query {i+1}")
    right.set(xlabel="Active subset", ylabel="Worst-rival margin (logits)",
              xticks=np.arange(8), xticklabels=masks, title="B. The only strict failure")
    right.legend(frameon=False, fontsize=8, loc="best")
    fig.savefig(HERE / "factorial.pdf", metadata={"CreationDate": None})
    plt.close(fig)


def write_tables(summary, run):
    def fmt(metric):
        x, low, high = metric
        return f"{x:.2f} [{low:.2f}, {high:.2f}]"

    n = summary["holdout_n"]
    by_wording = summary["by_wording"]
    primary = by_wording[0]["arms"]["focal"]
    secondary = by_wording[1]["arms"]["focal"]
    witness_seed = primary["strict_seeds"][0]
    witness, reversed_witness = (
        next(s for s in phrasing["stores"]["focal"] if s["seed"] == witness_seed)
        for phrasing in by_wording
    )
    audit = json.loads((EXPERIMENT / "binding_audit.json").read_text())
    store = run["holdout"][0]
    token_lengths = [row["token_count"] for row in store["old_reads"]]
    assert all([row["token_count"] for row in s["old_reads"]] == token_lengths
               for s in run["fit"] + run["holdout"])
    values = {
        "holdoutN": n,
        "fitN": summary["count_fit_n"],
        "nCalls": f'{run["scored_calls"]:,}'.replace(",", r"{,}"),
        "totalTokens": f'{run["scored_prompt_tokens"]:,}'.replace(",", r"{,}"),
        "elapsedMinutes": f'{run["wall_seconds"] / 60:.1f}',
        "noWitnessUpper": f'{100 * summary["zero_event_upper95"]:.1f}',
        "oldOn": f'{summary["calibration"]["active"]:.2f}',
        "oldOff": f'{summary["calibration"]["inactive"]:.2f}',
        "unboundCorrect": sum(np.argmax(row["removed"]) == 3 for row in audit),
        "strictPrimary": primary["strict"],
        "strictSecondary": secondary["strict"],
        "primaryFull": primary["full_correct"],
        "primaryNew": primary["new_correct"],
        "controlNew": by_wording[0]["arms"]["control"]["new_correct"],
        "newTotal": 3 * n,
        "primaryRatio": fmt(primary["third_to_pair"]),
        "primaryDelta": fmt(primary["third"]),
        "primaryAbs": fmt(primary["mean_abs_third"]),
        "primaryPairAbs": fmt(primary["pair_abs"]),
        "primaryFullChange": fmt(primary["full_change"]),
        "primaryCountThird": f'{by_wording[0]["count_third"]:.2f}',
        "primaryPredChange": f'{by_wording[0]["count_curve"][3]:+.2f}',
        "primaryResidualGap": fmt(by_wording[0]["focal_minus_disjoint_residual"]),
        "secondaryResidualGap": fmt(by_wording[1]["focal_minus_disjoint_residual"]),
        "primaryCountError": fmt(primary["count_error"]),
        "primaryPairError": fmt(primary["pair_error"]),
        "primaryCorrectedError": fmt(primary["corrected_error"]),
        "primaryTokens": token_lengths[0],
        "secondaryTokens": token_lengths[1],
        "witnessSeed": witness_seed,
        "witnessMargin": f'{witness["all_rival_min"][7]:.2f}',
        "witnessProper": f'{min(witness["all_rival_min"][:7]):.2f}',
        "witnessReworded": f'{reversed_witness["all_rival_min"][7]:+.2f}',
        "witnessPair": f'{witness["pair_min"]:+.2f}',
        "witnessCount": f'{witness["count_min"]:+.2f}',
        "witnessCorrected": f'{witness["corrected_min"]:+.2f}',
        "witnessRival": witness["full_rival"],
    }
    (HERE / "numbers.tex").write_text("".join(
        f"\\newcommand{{\\{name}}}{{{value}}}\n" for name, value in values.items()
    ))

    retention, error = [], []
    for wording, report in enumerate(by_wording, 1):
        for arm, (_, _, label) in ARM_STYLE.items():
            a = report["arms"][arm]
            retention.append(
                f'{wording} & {label} & {a["empty_correct"]}/{n} & {a["full_correct"]}/{n}'
                f' & {a["strict"]} & {a["pair_miss"]} & {a["corrected_miss"]}'
                f' & {token_lengths[wording-1]}'
            )
            error.append(f'{wording} & {label} & {fmt(a["count_error"])}'
                         f' & {fmt(a["pair_error"])} & {fmt(a["corrected_error"])}'
                         f' & {fmt(a["third_to_pair"])}')
    for name, rows in (("retention", retention), ("predictions", error)):
        (HERE / f"table_{name}.tex").write_text("".join(f"{row} " + r"\\" + "\n" for row in rows))


def main():
    summary = json.loads((EXPERIMENT / "summary.json").read_text())
    run = json.loads((EXPERIMENT / "run.json").read_text())
    plot(summary)
    write_tables(summary, run)


if __name__ == "__main__":
    main()
