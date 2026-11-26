# Self-branching skills: CPU pilot

A writer revises scalar steering skills from noisy matched-item comparisons. It can split one shared coefficient into two cue-routed children, rejoin, and split again. The toy follows the cue-and-common-probe criterion proposed in the [root](https://github.com/manojbajaj95/cl/pull/344), [branching](https://github.com/manojbajaj95/cl/pull/346), and [rejoining](https://github.com/manojbajaj95/cl/pull/348) research notes. It does not implement LoRA, natural-language skill writing, or dormant amendment reserves.

From the repository root with Python 3, NumPy, and SciPy:

```sh
python3 -m pytest -q experiments/self_branching_skills
OPENBLAS_NUM_THREADS=1 python3 experiments/self_branching_skills/run.py
```

The run writes the seed-level phase metrics (`seed_metrics.csv`) and summaries and configuration (`results.json`). A `--seeds` list selects replicates; `--out` accepts an existing output directory. `null` in JSON or an empty CSV field marks an event not observed or a cohort absent in that phase. The paper, vector plot, and LaTeX source are under [`papers/self-branching-skills`](../../papers/self-branching-skills).
