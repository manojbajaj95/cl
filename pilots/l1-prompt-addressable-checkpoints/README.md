# L1: prompt-addressable checkpoints

See [the protocol](protocol.md) for the reviewer’s exact gates, training setup, controls and inference limits.

## Paused

Work was paused at Manoj’s request to grow the idea pool before testing further. The five-seed CPU run (17, 29, 43, 59, 71) had already finished when the pause arrived. No GPU was used or needed for this pilot. [Raw results](results.jsonl) include tagged, matched untagged replay, random-tag, and equal-byte stored-delta arms, plus wrong-tag and frozen diagnostics.

| Reviewer check | Result (mean and paired 95% CI where applicable) |
|---|---|
| Held-out as-of KL, nats | Tagged **0.0068 [0.0033, 0.0107]**, replay **0.0102 [0.0049, 0.0160]**; paired Δ **−0.0034 [−0.0056, −0.0006]**, so the reviewer’s KL criterion passes. Probe Δ **−0.0037 [−0.0060, −0.0006]**; the effect was not probe-only. |
| Matched controls | Random tag **0.0086 [0.0041, 0.0131]**, wrong tag **0.0123 [0.0059, 0.0189]**, equal-byte stored deltas **0.0012 [0.0000, 0.0035]**. Stored deltas beat tags by **0.0056 [0.0010, 0.0102]** nats. Both deployments use 3,056,640 incremental bytes. |
| Current-tag tasks | Task 1–5 differences vs replay in pp: **−8.12 [−12.50, −3.75]**, **+5.00 [1.88, 8.12]**, **+0.62 [0.00, 1.88]**, **+9.38 [−0.62, 19.38]**, **−4.38 [−20.62, 13.75]**. Four point differences exceed the 1 pp absolute margin, including two regressions. |
| Current-tag WikiText-2 slice | PPL **67.84 [59.27, 74.32]** vs **62.64 [55.96, 67.66]**; paired relative change **+8.02% [5.13%, 10.75%]**, outside the 2% margin. |

**Pilot readout: kill this implementation, not the general hypothesis.** The held-out gain was smaller than the source card’s half-KL threshold (tagged/replay **66.7% [48.2%, 91.6%]**); the source old-accuracy floor passed relative to the checkpoints, but checkpoint accuracies for tasks 1, 3, and 5 were at or below 50% chance. The 512-token WikiText slice and head-only adapter limit the scope of the retention result. A first configuration (16 steps/stage, learning rate 0.025) was discarded for numerical/learning instability, not pooled into the final CIs; its raw trace is in [unstable-run.jsonl](unstable-run.jsonl).

No additional run is needed to apply these gates to the tested configuration. Before revisiting L1, require demonstrably learned stage checkpoints on all five tasks, then repeat the gates on independent task streams and a longer WikiText-2 split. The pilot ran in about two minutes wall time on six CPU threads; no GPU is requested. No follow-up experiment was started.

## Reproduce on CPU

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install 'torch==2.6.0+cpu' --index-url https://download.pytorch.org/whl/cpu
python -m pip install transformers==4.51.3 numpy==2.2.6 pyarrow==25.0.1
curl -fL https://huggingface.co/datasets/Salesforce/wikitext/resolve/3f68cd45302c7b4b532d933e71d9e6e54b1c7d5e/wikitext-2-raw-v1/test/0000.parquet -o wikitext-test.parquet
python pilot.py --wiki wikitext-test.parquet --seeds 17 29 43 59 71 > reproduced.jsonl
python summarize.py reproduced.jsonl
python -m unittest discover -v
```

The Qwen revision and fixed prompt splits are pinned in `pilot.py`. The WikiText-2 parquet SHA-256 is `5f1bea067869d04849c0f975a2b29c4ff47d867f484f5010ea5e861eab246d91`. The run writes only metrics, not any model weights or probe distributions.
