# Three-way write skew between in-context lessons

[Paper and figures](../../papers/lesson-write-skew/) · [Frozen protocol](PROTOCOL.md)

Each held-out store gives two eight-cell cubes from a shared inactive baseline,
with a fixed old rule and disjoint sets of random candidate keys. The separate
fit stores provide the count curve. A signed cubic factorial contrast tests
departure from a store's own lower-order effects; the count and disjoint arms
check whether that departure needs a specific combination. Accuracy is forced
choice among six queues, not unconstrained generation.

## Reproduce

Use Python 3.10+, NumPy, and the CPU `llama-server` build at llama.cpp
`0ce7f213b0749fa4dee4e87d8ae7bf63e621c1ad`. Download the
[pinned official FP16 GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-fp16.gguf).
Keep model weights outside git. From the repository root:

```sh
GGUF=/path/to/qwen2.5-0.5b-instruct-fp16.gguf
llama-server -m "$GGUF" --host 127.0.0.1 --port 8089 -t 8 -tb 8 -np 1 -c 512 -ngl 0 --no-warmup --no-webui
```

In another shell, with `GGUF` pointing to the same file:

```sh
python3 experiments/write_skew/run.py --model "$GGUF" --llama-commit 0ce7f213b0749fa4dee4e87d8ae7bf63e621c1ad
python3 experiments/write_skew/analyze.py --self-test
python3 experiments/write_skew/analyze.py
```

`run.json` records keys, slots, queue labels, verified positions, six
conditional log probabilities per read, the token budget, and elapsed wall
time. Subset index is a three-bit mask in candidate slot order; 0 is shared
and 7 is fully active. `summary.json` records paired store effects and
store-bootstrap intervals. The figure and paper tables can be regenerated
without model inference. Minor floating-point differences across CPU builds
are possible.
