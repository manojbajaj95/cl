# A3: Paired action-swap test

Do the words of a lesson change which tool the model selects, or just
how confidently it selects the tool it already preferred? This
follow-up to [A3](../a3-lessons-temperature/README.md) compares two
otherwise identical lesson prompts prescribing different legal actions.
See the [protocol](protocol.md) for the frozen design and decision
rules. No verifier-success outcomes are used to score following.

## Verdict: keep for 0.5B; the matched-margin comparison is inconclusive

The 0.5B follow index was **17.50 pp [5.69, 32.15]**, so neither kill line
fired. Changing only the prescribed action changed which action won;
temperature scaling alone cannot do that. The valid directive selected
its named action **11.11 pp [4.93, 18.61]** more often than same-length
filler and **11.18 pp [5.07, 18.47]** more often than the D twin.
Among targets that were not the baseline top action, the model flipped
to the named tool **17.09% [7.22%, 29.83%]** of the time with a valid
directive, **0.00% [0.00%, 0.00%]** with filler, and **6.73% [1.44%, 14.32%]**
with the non-menu twin. The D twin also perturbed some winners, so a
top-action flip on its own is not a measure of content following.

| Shared baseline-margin bins | 0.5B follow [95% CI] | 1.5B follow [95% CI] | 1.5B − 0.5B [95% CI] |
|---|---:|---:|---:|
| All shared bins, including zero | 19.09 pp [7.16, 33.28] | 0.00 pp [0.00, 0.00] | −19.09 pp [−33.28, −7.48] |
| Shared positive-margin bins only | 0.39 pp [0.00, 1.57] | 0.00 pp [0.00, 0.00] | −0.39 pp [−1.50, 0.00] |

**The test did not show that 1.5B follows at matched margins.** Most
0.5B flips to the named tool (155/160) were in small positive gaps below
1 logit unit, where 1.5B supplied no observations. Over the shared
positive gaps (1.75–2.75, excluding the unmatched 2.25–2.50 bin),
neither model showed clear following. This is consistent with a margin
effect, but without both readers in the low positive bins the test
cannot distinguish margin from scale as the reason for 1.5B's earlier
zero flips.

The all-bin difference is driven by the zero bin, where the targets
already lead at baseline (B on 0.5B; A on 1.5B). At shared positive
margins, the targets are C on 0.5B and B on 1.5B. Matching gap size
does not match the token identity or the rest of the model's ranking.
The smallest shared positive bin contains only one 1.5B observation
replicated across lessons; pooled matched 1.5B and model-difference
intervals use the 2,258/4,000 bootstrap draws that retain every
shared bin. The primary CI uses all 4,000 draws.
[Full results](results.json) include bin-by-bin counts, label mix
and conditional intervals.

## Reproduce

From this directory, with Python 3.10+:

```sh
python -m pip install -r ../a3-lessons-temperature/requirements.txt
export OPENBLAS_NUM_THREADS=1
python -m unittest discover
python analysis_swap.py --data-dir data --output /tmp/a3-swap-results.json
diff -u results.json /tmp/a3-swap-results.json
```

To recollect, build llama.cpp b6800 and download the same GGUFs
following the [A3 setup](../a3-lessons-temperature/README.md#reproduce),
then point to that work directory and create a new output directory:

```sh
WORK="$HOME/a3-pilot-work"
SWAP_WORK="$HOME/a3-swap-work"
mkdir -p "$SWAP_WORK"
PYTHONPATH=../a3-lessons-temperature python -u collect_swap.py \
  --server "$WORK/llama.cpp/build/bin/llama-server" \
  --old-model "$WORK/old.gguf" --new-model "$WORK/new.gguf" --work-dir "$SWAP_WORK"
python analysis_swap.py --data-dir "$SWAP_WORK" --output "$SWAP_WORK/results.json"
```

The [frozen data](data) contain the lesson templates, exact filler
texts, prompt token counts and all constrained legal-action scores.
