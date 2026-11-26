# When Should a Self-Written Skill Branch?

[Preprint PDF](paper.pdf) • [Experiment and results](../../experiments/self_branching_skills)

From the repository root, regenerate the plot and tables from the saved run with Matplotlib:

```sh
python3 papers/self-branching-skills/plot.py
```

Then, from this directory, build the manuscript:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex
```
