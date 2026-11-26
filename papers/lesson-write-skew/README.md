# A Wording-Sensitive Case of Three-Way Write Skew in In-Context Memory

[alphaXiv](https://www.alphaxiv.org/abs/2611.wording-sensitive-three-way-write-skew) · [Paper PDF](paper.pdf) · [Experiment and per-store data](../../experiments/write_skew/)

From this directory, regenerate the vector figure, tables, and paper from the
saved run (requires NumPy, Matplotlib, and TeX Live):

```sh
python3 plot.py
latexmk -pdf -interaction=nonstopmode -halt-on-error paper.tex
```
