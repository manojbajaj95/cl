# Sequential model edit capacity pilot

See the [locked protocol](../docs/edit-capacity-protocol.md) for the endpoint, forecasts, and keep criterion, and the [results](../docs/edit-capacity-results.md) for the verdict.

## Reproduce

Python 3.10 with CPU PyTorch:

```sh
python -m venv .venv
. .venv/bin/activate
pip install 'torch==2.7.1+cpu' 'transformers==4.53.3' 'numpy==2.2.6' \
  --extra-index-url https://download.pytorch.org/whl/cpu
python -m unittest discover -s pilots -v
```

Set `DATA` to a directory containing `counterfact.json` from
[ROME](https://rome.baulab.info/data/dsets/counterfact.json)
(SHA-256 `d017056125178a13728594e66a801357a8db9ed7973a7425554bb4271de9fc6f`)
and `gpt2/{config.json,tokenizer.json,model.safetensors}` from
[openai-community/gpt2 @ 607a30d](https://huggingface.co/openai-community/gpt2/tree/607a30d783dfa663caf39e06633721c8d4cfcd7e)
(weights SHA-256 `248dfc3911869ec493c76e65bf2fcf7f615828b0254c12b473182f0f81d3a707`).
Set `OUT` to a fresh output directory.

```sh
python pilots/edit_capacity.py --data "$DATA" --out "$OUT" --phase calibrate
python pilots/edit_capacity.py --data "$DATA" --out "$OUT" --phase evaluate
python pilots/edit_capacity.py --out "$OUT" --phase summary
```

The first step generates calibration traces. The second writes the capacity
forecast before the first edit of each held-out run and the norm forecast when
the 10% prefix ends, then measures the endpoint. With `--seed`, either run
phase can be split across processes by stream (the recorded run used two
threads per process). Finished runs are not repeated.

Reproduce the comparison without editing or downloading weights:

```sh
python pilots/edit_capacity.py --out pilots/results/edit-capacity --phase summary
```
