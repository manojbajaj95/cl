#!/bin/bash
# No-memory floor: 3 seeds at the entropy-matched T from temperature_fit.json (waits for the fit).
cd "$(dirname "$0")"
while [ ! -f temperature_fit.json ]; do sleep 30; done
T=$(python3 -c "import json; print(json.load(open('temperature_fit.json'))['fitted_T'])")
for s in 0 1 2; do echo "none $s"; done |
  xargs -P 3 -L 1 bash -c "python3 run.py --arm \$0 --seed \$1 --threads 2 --temperature $T > runs/\$0_s\$1.log 2>&1"
