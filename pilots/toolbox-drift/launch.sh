#!/bin/bash
# 12 jobs (4 arms x 3 seeds); LLM-heavy lesson arms first, 4 at a time, 2 threads each.
cd "$(dirname "$0")"
jobs=()
for arm in lesson lesson+tests tool+tests tool; do for s in 0 1 2; do jobs+=("$arm $s"); done; done
printf '%s\n' "${jobs[@]}" | xargs -P 4 -L 1 bash -c 'python3 run.py --arm $0 --seed $1 --threads 2 > runs/${0/+/_}_s$1.log 2>&1'
