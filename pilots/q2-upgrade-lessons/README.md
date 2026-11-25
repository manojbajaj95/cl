# Fleet Q2 pilot

Can a new model's likelihood gain on successful logged actions predict
whether a memory lesson still helps after an upgrade? See [protocol](PROTOCOL.md)
for the two gates and [results](RESULTS.md) for the keep-or-kill decision.

## Reproduce

Use Python 3.10+ and llama.cpp CPU server tag **b6800**
(`0398752dd450dfabdd1b9e289f6364c2600f6ab5`). From this directory:

```sh
python -m pip install -r requirements.txt
git clone --depth 1 --branch b6800 https://github.com/ggml-org/llama.cpp.git "$HOME/q2-llama-cpp"
cmake -S "$HOME/q2-llama-cpp" -B "$HOME/q2-llama-cpp/build" \
  -DGGML_NATIVE=ON -DLLAMA_CURL=OFF -DLLAMA_BUILD_TESTS=OFF
cmake --build "$HOME/q2-llama-cpp/build" --target llama-server -j 8
SERVER="$HOME/q2-llama-cpp/build/bin/llama-server"
OLD="$HOME/qwen2.5-0.5b-instruct-q4_k_m.gguf"
NEW="$HOME/qwen2.5-1.5b-instruct-q4_k_m.gguf"
curl -fL 'https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-q4_k_m.gguf' -o "$OLD"
curl -fL 'https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf' -o "$NEW"
export OPENBLAS_NUM_THREADS=1
python collect.py prepare --server "$SERVER" --old-model "$OLD"
python collect.py truth --server "$SERVER" --new-model "$NEW"
# Do not continue if the printed reliability gate fails.
python collect.py source --server "$SERVER" --old-model "$OLD" --new-model "$NEW"
python collect.py prune --server "$SERVER" --new-model "$NEW"
REPLICATION="$HOME/qwen2-1_5b-instruct-q4_k_m.gguf"
curl -fL 'https://huggingface.co/Qwen/Qwen2-1.5B-Instruct-GGUF/resolve/c62434db644497c0ee545c690bb66a67eba6eb3f/qwen2-1_5b-instruct-q4_k_m.gguf' -o "$REPLICATION"
python collect.py replicate --server "$SERVER" --replication-model "$REPLICATION"
python analysis.py
python -m unittest discover
```

The collector verifies the GGUF SHA-256s, validates that the legal actions
and ratings are single tokens, and checks that each server response returned
exactly those token IDs. Equal logit bias plus top-k over the boosted legal
tokens leaves their relative scores unchanged; no other truncation or
penalty is applied. The checked-in policy tensors are constrained
temperature-1 log probabilities indexed by lesson (baseline first),
checkpoint, code minus ten and action A/B/C. The text in `lessons.json` uses
zero-based source code indices and records the writer episode for authored
lessons. Regenerate `results.json` with just `python analysis.py` and the
checked-in artifacts; checkpoint downloads are not needed for analysis.
