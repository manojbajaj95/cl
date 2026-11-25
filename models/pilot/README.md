# CPU pilot: old behavior retention during on-policy adaptation

Run from the repository root with Python 3.10+:

```sh
python -m venv .venv
.venv/bin/python -m pip install --index-url https://download.pytorch.org/whl/cpu 'torch==2.6.0' 'numpy<3'
.venv/bin/python -B -m unittest discover -s models/pilot -v
.venv/bin/python -B models/pilot/run.py
.venv/bin/python -B models/pilot/audit.py
```

The training run uses one CPU thread and takes about 72 seconds on the test machine; there are no downloads besides dependencies, no checkpoints on disk, and no dataset artifacts. Use `--seeds`, `--steps`, or `--target` for follow-up experiments.

## What is measured

A small GRU language model learns an old rule for two prompt groups. Each prompt permits two distinct seven-token completions. The pretrained checkpoint also knows an alternate rule behind a privileged task marker, including from partially corrupted answer prefixes. It initially applies the old rule to unhinted new prompts. In the adaptation stage, the learner generates trajectories on unhinted new prompts; its frozen pretrained copy supplies next-token targets under the hidden marker on those same trajectories.

Every method uses the same new-task objective. On old prompts, methods differ only in their additional objective: none; token KL on fresh student trajectories; supervised replay of both valid paths; KL on the relative distribution between paths conditional on success (a simplified CoKL control); mean old success-drop penalty; or worst-group success-drop penalty. Success is the sum of the two exact autoregressive trajectory probabilities under free generation; no best-of-N or forced decoding at evaluation. Methods get the same adaptation step limit. Each guarded method has the same four penalty weights; the unguarded method has no weight to sweep. Checkpoint selection maximizes development worst-group BWT among candidates with new success at least 0.75. Final scores use separate nuisance prompt values, held out from adaptation but seen at pretraining. This tests retention, not transfer to never-seen task templates.

The audit first simulates fixed-sample decisions with known accepted, rejected, and unresolved mass. It then samples actual autoregressive outputs from the learned policy on one old prompt: certify the first valid path and reject all invalid paths outside the second style, then draw from the second style prefix only. This tests the interval arithmetic and residual sampler, not certificate discovery.

## Results

Five seeds, PyTorch 2.6.0+cpu, 100 adaptation steps per trial. The initial mean old success across the five seeds was 0.978. Means below are **conditional on development qualification**; different seed counts mean the table is not a paired ranking. BWT is the change in old success from the initial reference, in percentage points (higher is better).

| Method | Qualified | New success | Mean BWT | Worst-group BWT |
|---|---:|---:|---:|---:|
| Unguarded OPSD | 2/5 | 75.5% | −96.31 pp | −97.16 pp |
| Token KL | 4/5 | 93.7% | −0.99 pp | −1.31 pp |
| Canonical replay | 3/5 | 97.6% | −0.16 pp | −0.47 pp |
| Conditional KL | 2/5 | 87.2% | −36.87 pp | −57.44 pp |
| Mean event mass | 4/5 | 92.2% | −0.83 pp | −1.09 pp |
| Worst-group event mass | 4/5 | 94.3% | −0.63 pp | −0.69 pp |

On the four paired token-KL seeds, worst-group event mass improved worst-group BWT by 0.62 pp and new success by 0.64 pp, but this small difference is not strong evidence. On the three seeds qualifying for both canonical replay and worst-group event mass, replay was ahead on both worst-group BWT (−0.47 vs. −0.62 pp) and new success (97.59% vs. 96.05%). On the two seeds qualifying for unguarded OPSD, the event guard retained 96.57 pp more on worst-group BWT while achieving higher new success. One seed failed qualification under every method; the highest development new success on that seed was 0.7008. A first 60-step run with a weaker hint teacher had only two qualified seeds for the event guards; the second run strengthened teacher recovery on off-target prefixes and increased the step budget rather than lowering the 0.75 gate. These runs demonstrate recoverable forgetting, not a superior training objective or a strict acquisition match.

The simulated audit ran 2,000 independent replicates per cell for true success 0.58 (should reject) and 0.62 (should accept), using a 0.60 threshold and 95% fixed-sample Hoeffding intervals. With 50% unresolved mass, 2,048 verifier calls yielded 81.3% correct rejections and 82.6% correct accepts. Plain rollouts needed 8,192 calls for similar rates (81.8% and 81.6%). With 15% unresolved mass, 512 calls yielded 99.9% correct rejections and 100% correct accepts. There were no wrong decisions at the three reported budget settings; remaining replicates were inconclusive. On the learned policy's one prompt (true success 0.9603, unresolved mass 0.5006), residual sampling reduced RMSE from 0.0167 to 0.0044 at 128 draws and from 0.0095 to 0.0026 at 512 draws, each over 16 replicates. The certificate in that test follows from the rules of the toy. Call counts do **not** include prefix construction, decoding, or an adaptive sequence of tests. The next experiment should measure the cost of constructing trustworthy prefixes against the residual mass they eliminate before claiming a practical advantage.

## Scaling

Keep the pilot as the exact small-domain control. For the first GPU experiment, replace the GRU with a 0.5B/1.5B instruct model, use batched student generation and an independently scored old-prompt stream, and begin with verifiers that admit cheap short-prefix certificates (e.g. bounded structured output). Compare plain and residual sampling at fixed false-decision rates, charging all prefix compute and verifier calls. Advance to a larger model or general reasoning only if the speedup survives that accounting and tuned replay remains a competitive control. The [proposal](../proposal.md) lists the staged hardware, controls, and kill criteria.
