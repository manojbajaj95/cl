# A3: Is 1.5B not following lessons because of its margin?

The [previous action-swap test](../a3-action-swap/README.md) found
that 0.5B followed paired directives but that 1.5B supplied no
observations in the small, positive-margin bins where most 0.5B
flips occurred. Here we put 1.5B into those bins in two ways:
a fixed source-fit A-logit offset and a natural prompt change
(renamed actions plus permuted menu). Both use the same paired
directions and a length-matched filler control. See the [protocol](protocol.md).

## Verdict: inconclusive

| 1.5B arm | Distinct eligible states | Follow index [95% CI] | Named-action lift vs filler [95% CI] |
|---|---:|---:|---:|
| Controlled A offset | 30/30 test states | **10.42 pp [0.00, 25.56]** | +5.21 pp [0.00, 12.78] |
| Natural labels and menu order | 36/36 (minimum 30) | **90.97 pp [79.17, 99.38]** | +45.49 pp [39.58, 49.69] |

Natural following passed the ≥10 pp and positive-CI gates. Controlled
following cleared the point threshold but its CI touched zero, so the
joint margin rule did not pass. The scale rule did not pass either:
1.5B plainly followed under the natural prompts. This establishes
that 1.5B **can** follow, not that the earlier zero flips were caused by
margin alone.

The source fit subtracted **2.105** logit units from A in every
controlled arm. The natural screen first tried X/Z/Y menu order
(0/36 qualifying); its next variant, **Y/X/Z**, qualified all 36
without changing their scores. Across the four small positive bins the
controlled counts were **2/9/17/2** and natural counts were **7/13/13/3**.
The canonical top-two pair was A/B in every admitted state, but the
natural prompt usually made canonical B the leader (35/36), whereas
A usually remained the leader after subtraction (29/30). Thus the
natural intervention can change more than the top-two gap: it changes
token identities, order, and the prevailing action. In the controlled
arm the directive picked the runner-up **13.33% [1.85%, 28.33%]** of the
time versus **3.33% [0.00%, 10.00%]** for filler; natural rates were
**92.01% [80.09%, 100.00%]** versus **2.78% [0.00%, 8.33%]**.
All CIs use 4,000 crossed lesson/state draws.

**Carry to [7B ALFWorld](../a3-lessons-temperature/replication-7b.md):**
on a fixed no-memory state tape after the source-stage gate, cross
menu order with action-ID renaming instead of changing both together.
Keep the underlying action semantics fixed, fit the logit offset on
source states only, and compare paired follow indices and correct-flip
rates vs filler on held-out states with overlapping top-two gaps.
Stratify by whether the intervention preserves the baseline leader
and by the action pair; report lack of overlap rather than treating
nonoverlap as evidence for scale.

## Reproduce

From this directory, with Python 3.10+:

```sh
python -m pip install -r ../a3-lessons-temperature/requirements.txt
export OPENBLAS_NUM_THREADS=1
export PYTHONPATH=../a3-action-swap:../a3-lessons-temperature
python -m unittest discover
python analysis_margin.py --swap-data ../a3-action-swap/data \
  --natural data/natural-policies.npz --output /tmp/a3-margin-results.json
diff -u results.json /tmp/a3-margin-results.json
```

Controlled scores are derived from the raw [swap policies](../a3-action-swap/data);
the logits are not rescored. To recollect the natural scores, follow
the [CPU build and model setup](../a3-lessons-temperature/README.md#reproduce)
and run:

```sh
WORK="$HOME/a3-pilot-work"
MARGIN_WORK="$HOME/a3-margin-work"
mkdir -p "$MARGIN_WORK"
python -u collect_margin.py --server "$WORK/llama.cpp/build/bin/llama-server" \
  --new-model "$WORK/new.gguf" --notes ../a3-action-swap/data/lessons.json \
  --work-dir "$MARGIN_WORK"
```

The [frozen natural data](data) include every tested no-lesson variant,
selected state IDs, canonical action scores, fillers and token counts.
