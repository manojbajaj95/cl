# Dirty-Paper Writes Make Old Weights Free but Do Not Beat Projection

The [paper PDF](paper.pdf) reports the CPU test of dirty-paper writes (top-10
idea #6): a clean negative against GPM/OWM projection at equal update norm.
The [experiment directory](../../experiments/dirty_paper/) has the simulator,
self-tests and saved seed-level data.

From this directory, regenerate the figures, tables and numbers from the saved
sweep, then build the paper:

```sh
python3 plot.py
latexmk -pdf paper.tex
```
