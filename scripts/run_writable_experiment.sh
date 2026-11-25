#!/usr/bin/env bash
# End-to-end reproducer for the ~20M writable-from-birth pretraining vs standard LM kill test.
# Trains Model A (19.80M standard) and Model B (19.82M writable-from-birth) on the exact same
# data distribution and matched FLOPs budget, then runs the text-vs-write kill test on fresh
# fictional facts (recall, paraphrase, cue-free inverse, cue-free 2-hop, and static drift).
set -euo pipefail

MAX_FLOPS="${MAX_FLOPS:-2.0e14}"
LR="${LR:-8e-4}"
SEED="${SEED:-42}"
THREADS="${THREADS:-8}"
OUT_ROOT="${OUT_ROOT:-runs/repro_20m}"

export PYTHONPATH="."

echo "=== [1/3] Pretraining Model A (StandardLM, ~20M) for ${MAX_FLOPS} FLOPs ==="
python3 -m writable_pretrain.train \
  --mode standard --scale 20m \
  --max_flops "${MAX_FLOPS}" --lr "${LR}" --seed "${SEED}" \
  --out_dir "${OUT_ROOT}/model_a_20m" --threads "${THREADS}"

echo "=== [2/3] Pretraining Model B (WritableLM, ~20M) for ${MAX_FLOPS} FLOPs ==="
python3 -m writable_pretrain.train \
  --mode writable --scale 20m \
  --max_flops "${MAX_FLOPS}" --lr "${LR}" --seed "${SEED}" \
  --out_dir "${OUT_ROOT}/model_b_20m" --threads "${THREADS}"

echo "=== [3/3] Running Text-vs-Write Kill Test on Fresh Fictional Facts ==="
python3 -m writable_pretrain.eval_killtest \
  --ckpt_a "${OUT_ROOT}/model_a_20m/final.pt" \
  --ckpt_b "${OUT_ROOT}/model_b_20m/final.pt" \
  --chains 4 8 --episodes 5 --rag_top_k 2 \
  --out_json "${OUT_ROOT}/killtest_results.json"
