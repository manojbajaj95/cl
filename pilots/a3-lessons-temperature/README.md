# A3: Are in-context lessons mostly a temperature knob?

This pilot tests the [PR #27 anomaly](https://github.com/manojbajaj95/cl/pull/27)
using a changed router verifier and a held-out entropy-matched control.
See the [protocol](protocol.md) for the arms, balanced splits and decision
rules. Unlike the retrospective 0.95 R² in PR #27, these temperature
fits use only source-start entropy, not success outcomes.

## Result: keep on the upgraded reader

The 1.5B reader passes all three prespecified kill lines. Intervals below
are paired 95% lesson-bootstrap CIs; exact success has no rollout noise.

| Held-out metric, 40 lessons | Qwen2.5-1.5B (primary) | Qwen2.5-0.5B (diagnostic) |
|---|---:|---:|
| Pooled temperature-control R² (kill < 0.50) | **0.916 [0.872, 0.956]** | −0.123 [−0.335, 0.037] |
| Rule lessons minus temperature match (kill ≥ 5 pp with CI above 0) | **+0.94 pp [0.64, 1.30]** | +3.52 pp [0.67, 6.29] |
| Lesson main-effect share (kill > 25%) | **2.18% [0.57%, 3.74%]** | 84.17% [74.86%, 88.67%] |
| Other-lesson temperature-control R² (proposal prediction ≥ 0.80) | 0.958 [0.920, 0.985] | −0.025 [−0.311, 0.110] |
| Balanced split-half Pearson r | 0.953 [0.756, 0.985] | 0.991 [0.980, 0.997] |

On the 1.5B reader, rule lessons improve held-out success by **+3.13 pp**
[2.73, 3.45] vs no lesson. They beat same-length filler by **+0.88 pp**
[0.28, 1.48]. Other lessons add **+3.02 pp** [2.59, 3.35] vs no lesson
but **−0.10 pp** [−0.51, 0.25] vs their filler. Filler alone adds
**+2.69 pp** [2.43, 2.92] overall. The control reproduces most of the
effect pattern, but the nonzero rule residual is evidence against an
exact temperature-only account. R² measures explained variation across
lesson/start cells, not percent of average lift.

**Manipulation checks.** Each half has four high- and two low-success
starts for both readers. The 1.5B no-lesson exact success is 0.839–0.924
on nonmultiples of three and 0.088–0.117 on multiples of three; its
modal tool is A at all 36 observations. For the 0.5B reader the two
lowest starts per half are multiples of three (0.101–0.111 vs
0.208–0.266 for the rest), but its modal tool B never succeeds in this
verifier. 37/40 lessons sharpen the primary reader on source
starts; its maximum entropy mismatch is 1.3e−13 nats.

**Limits.** The unchanged prompt states the old rule, so rule lessons
must override stale instructions. The verifier remapping favors the
upgraded reader's A mode outside multiples of three, unlike the older
reader's B mode anywhere. The mechanism does not survive on the 0.5B
diagnostic and should not be treated as universal. The 40 lesson entries
include 26 unique prompts (repeated failure advice). Giving each exact
prompt one vote still passes on 1.5B: R² **0.868** [0.804, 0.935],
rule gap **+1.11 pp** [0.68, 1.61], main effect **3.28%**
[0.82%, 5.12%]. On that sensitivity check the rule-vs-filler gap is
**+0.60 pp** [−0.12, 1.29]. CIs are conditional on one router,
one inventory, and fixed starts; later observations can be reachable
from both halves. [Full results](results.json) include all contrasts
and per-start effects' underlying success values.

**Next:** [7B real-benchmark replication specification](replication-7b.md).

## Reproduce

From this directory with Python 3.10+:

```sh
python -m pip install -r requirements.txt
export OPENBLAS_NUM_THREADS=1
python -m unittest discover
python analysis.py --data-dir data --output /tmp/a3-results.json
diff -u results.json /tmp/a3-results.json
```

To collect the policies again on CPU, use llama.cpp **b6800**
(`0398752dd450dfabdd1b9e289f6364c2600f6ab5`):

```sh
WORK="$HOME/a3-pilot-work"
mkdir -p "$WORK"
git clone --depth 1 --branch b6800 https://github.com/ggml-org/llama.cpp.git "$WORK/llama.cpp"
cmake -S "$WORK/llama.cpp" -B "$WORK/llama.cpp/build" \
  -DGGML_NATIVE=ON -DLLAMA_CURL=OFF -DLLAMA_BUILD_TESTS=OFF
cmake --build "$WORK/llama.cpp/build" --target llama-server -j 8
curl -fL https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/9217f5db79a29953eb74d5343926648285ec7e67/qwen2.5-0.5b-instruct-q4_k_m.gguf -o "$WORK/old.gguf"
curl -fL https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/91cad51170dc346986eccefdc2dd33a9da36ead9/qwen2.5-1.5b-instruct-q4_k_m.gguf -o "$WORK/new.gguf"
python -u collect.py --server "$WORK/llama.cpp/build/bin/llama-server" \
  --old-model "$WORK/old.gguf" --new-model "$WORK/new.gguf" --work-dir "$WORK"
python analysis.py --data-dir "$WORK" --output "$WORK/results.json"
```

The collector verifies checkpoint hashes and legal-token IDs.
`data/` contains the frozen lesson inventory and constrained policy
tables, so the report can be recomputed without GGUFs or llama.cpp.
