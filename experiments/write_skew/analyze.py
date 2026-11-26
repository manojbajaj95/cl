"""Analyze paired cubes. The unit of resampling is a held-out store."""
import argparse
import json
from pathlib import Path

import numpy as np

COUNTS = np.array([0, 1, 1, 2, 1, 2, 2, 3])
SINGLE, PAIR = [1, 2, 4], [3, 5, 6]
TARGET_INDEX = 3
RIVALS = np.array([0, 1, 2, 4, 5])
ARMS = ("focal", "control")


def pair_forecast(cube):
    return cube[PAIR].sum(axis=0) - cube[SINGLE].sum(axis=0) + cube[0]


def pair_effects(cube):
    return cube[PAIR] - cube[[1, 1, 2]] - cube[[2, 4, 4]] + cube[0]


def strict_failure(cube):
    return bool(np.min(cube[:7]) > 0 and np.min(cube[7]) <= 0)


def margins(scores):
    scores = np.asarray(scores)
    return scores[..., TARGET_INDEX, None] - scores[..., RIVALS]


def count_curve(fit, wording):
    curves, rival_curves = [], []
    for store in fit:
        cube = margins(store["old_reads"][wording]["control"])
        changes = cube - cube[0]
        by_count = np.stack([changes[COUNTS == k].mean(axis=0) for k in range(4)])
        curves.append(by_count[:, np.argmin(cube[0])])
        rival_curves.append(by_count)
    return np.mean(curves, axis=0), np.mean(rival_curves, axis=0)


def third(curve):
    return curve[3] - 3 * curve[2] + 3 * curve[1] - curve[0]


def evaluate(store, wording, arm, count, by_rival):
    old = store["old_reads"][wording]
    cube = margins(old[arm])
    ref = np.argmin(cube[0])
    fixed = cube[:, ref]
    prediction = pair_forecast(cube)
    contrast = cube[7, ref] - prediction[ref]
    corrected = prediction + third(by_rival)
    forecast = cube[0] + by_rival[3]
    strict = strict_failure(cube)
    reads = store["new_reads"][arm]
    return dict(
        seed=store["seed"],
        empty_correct=int(cube[0].min() > 0),
        full_correct=int(cube[7].min() > 0),
        strict=int(strict),
        pair_miss=int(strict and prediction.min() > 0),
        corrected_miss=int(strict and corrected.min() > 0),
        both_miss=int(strict and prediction.min() > 0 and forecast.min() > 0),
        new_correct=sum(int(np.argmax(row) + 1 == q)
                        for row, q in zip(reads, store["queues"])),
        third=contrast,
        pair_abs=float(np.mean(abs(pair_effects(fixed)))),
        count_centered_abs=abs(contrast - third(count)),
        full_change=fixed[7] - fixed[0],
        count_error=abs(fixed[7] - fixed[0] - count[3]),
        pair_error=abs(contrast),
        corrected_error=abs(contrast - third(count)),
        margins=fixed.tolist(),
        all_rival_min=cube.min(axis=1).tolist(),
        rival=int(RIVALS[ref] + 1),
        full_rival=int(RIVALS[np.argmin(cube[7])] + 1),
        pair_min=float(prediction.min()),
        count_min=float(forecast.min()),
        corrected_min=float(corrected.min()),
    )


def comparison(result, wording):
    count, by_rival = count_curve(result["fit"], wording)
    data = {arm: [evaluate(store, wording, arm, count, by_rival)
                  for store in result["holdout"]] for arm in ARMS}
    n = len(result["holdout"])
    lookup = np.random.default_rng(832 + wording).integers(0, n, size=(10000, n))
    columns = {arm: {key: np.asarray([row[key] for row in rows])
                     for key in rows[0] if key not in {"seed", "rival", "full_rival"}}
               for arm, rows in data.items()}

    def paired_ci(a):
        return [float(a.mean()), *np.quantile(a[lookup].mean(axis=1), [.025, .975]).tolist()]

    def ratio(arm):
        a, b = abs(columns[arm]["third"]), columns[arm]["pair_abs"]
        boot = a[lookup].mean(axis=1) / b[lookup].mean(axis=1)
        return [float(a.mean() / b.mean()), *np.quantile(boot, [.025, .975]).tolist()]

    def stats(arm):
        col = columns[arm]
        totals = ["empty_correct", "full_correct", "strict", "pair_miss",
                  "corrected_miss", "both_miss", "new_correct"]
        report = {key: int(col[key].sum()) for key in totals}
        report["third_to_pair"] = ratio(arm)
        report["mean_abs_third"] = paired_ci(abs(col["third"]))
        for key in ("third", "count_centered_abs", "count_error", "pair_error",
                    "corrected_error", "full_change", "pair_abs"):
            report[key] = paired_ci(col[key])
        report["strict_seeds"] = col["strict"].nonzero()[0].tolist()
        report["strict_seeds"] = [data[arm][i]["seed"] for i in report["strict_seeds"]]
        return report

    return dict(
        count_curve=count.tolist(),
        count_third=float(third(count)),
        arms={arm: stats(arm) for arm in ARMS},
        focal_minus_disjoint_residual=paired_ci(
            columns["focal"]["count_centered_abs"] - columns["control"]["count_centered_abs"]
        ),
        stores=data,
    )


def summarize(result):
    n = len(result["holdout"])
    calibration = result["calibration"]
    return dict(
        holdout_n=n, count_fit_n=len(result["fit"]),
        zero_event_upper95=1 - .05 ** (1 / n),
        calibration={key: float(margins(calibration[key]).min())
                     for key in ("active", "inactive")},
        by_wording=[comparison(result, wording) for wording in range(2)],
    )


def self_test():
    additive = 2.5 - COUNTS
    assert strict_failure(additive)
    assert additive[7] - pair_forecast(additive) == 0
    assert not pair_effects(additive).any()
    load = np.array([2.5, 2.0, 1.0, -1.0])
    cube = load[COUNTS]
    assert strict_failure(cube)
    assert cube[7] - pair_forecast(cube) == third(load) == -.5
    planted = np.full(8, 1.0)
    planted[7] = -1
    assert strict_failure(planted)
    assert pair_forecast(planted) == 1 and planted[7] - pair_forecast(planted) == -2
    assert not strict_failure(np.r_[planted[:7], 1])
    assert not strict_failure(np.r_[0, planted[1:]])
    switched = np.column_stack([planted, np.ones_like(planted)])
    assert strict_failure(switched)
    assert np.all(pair_forecast(switched) == 1)


def main():
    directory = Path(__file__).parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=directory / "run.json")
    parser.add_argument("--output", type=Path, default=directory / "summary.json")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    self_test()
    if args.self_test:
        print("Factorial analysis self-tests passed.")
        return
    summary = summarize(json.loads(args.input.read_text()))
    args.output.write_text(json.dumps(summary, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    main()
