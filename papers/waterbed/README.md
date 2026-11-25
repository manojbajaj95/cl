# A Counterexample to the Forgetting Waterbed

The [paper PDF](paper.pdf) reports the falsification of raw log-area
invariance and explains the local, gain-normalized result. The
[experiment directory](../../experiments/waterbed/) contains the simulator,
estimator checks, and saved seed-level data.

From this directory, regenerate the vector figure from the saved sweep
and build the paper:

```sh
python3 plot.py
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
bibtex paper
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
pdflatex -interaction=nonstopmode -halt-on-error paper.tex
```

`plot.py` uses NumPy, SciPy, and Matplotlib. The TeX build uses the
standard LaTeX packages listed in `paper.tex`.
