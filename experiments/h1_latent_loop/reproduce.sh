#!/usr/bin/env bash
set -euo pipefail

here=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
data=${H1_DATA:-"$HOME/.cache/cl-h1"}
mkdir -p "$data/model" "$data/wiki"
data=$(cd -- "$data" && pwd)
model_url=https://huggingface.co/Qwen/Qwen2.5-1.5B/resolve/8faed761d45a263340a0528343f099c05c9a4323
wiki_url=https://huggingface.co/datasets/Salesforce/wikitext/resolve/b08601e04326c79dfdd32d625aee71d232d685c3/wikitext-2-raw-v1

download() {
    local url=$1 output=$2
    if [[ ! -s "$output" ]]; then
        curl -fLsS --retry 3 "$url" -o "$output.part"
        mv "$output.part" "$output"
    fi
}

for file in config.json tokenizer.json tokenizer_config.json model.safetensors; do
    download "$model_url/$file" "$data/model/$file"
done
for split in train test; do
    download "$wiki_url/$split-00000-of-00001.parquet" "$data/wiki/$split.parquet"
done
(cd "$data" && sha256sum -c "$here/inputs.sha256")

if [[ -n "${H1_PYTHON:-}" ]]; then
    python_bin=$H1_PYTHON
else
    python_bin="$data/venv/bin/python"
    if [[ ! -f "$data/venv/.h1-ready" ]]; then
        python3 -m venv "$data/venv"
        "$python_bin" -m pip install --extra-index-url https://download.pytorch.org/whl/cpu -r "$here/requirements.txt"
        touch "$data/venv/.h1-ready"
    fi
fi

out=${H1_OUT:-"$data/results"}
"$python_bin" -u "$here/run.py" --model "$data/model" --wiki "$data/wiki" --out "$out" "$@"
"$python_bin" -u "$here/run.py" --model "$data/model" --out "$out" --add-vector-controls
"$python_bin" "$here/summarize.py" "$out/run.json"
