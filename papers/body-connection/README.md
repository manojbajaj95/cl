# The Body Connection Has Headroom That a Generic Learned Model Cannot Reach

[Preprint PDF](paper.pdf) • [Experiment, preregistration and results](../../experiments/body_connection)

From the repository root, rerun the preregistered sweep (about 30 min on 8 CPU cores, needs `mujoco==3.17.0`), then regenerate the figure and tables with Matplotlib:

```sh
python3 experiments/body_connection/mechanism.py
python3 papers/body-connection/plot.py
```

Then, from this directory, build the manuscript:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex
```
