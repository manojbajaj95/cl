# cl: continual-learning research playground

- [docs/frontier-scan.md](docs/frontier-scan.md), [docs/research-process.md](docs/research-process.md): landscape scan and research process.
- [docs/agent-artifact-epidemics.md](docs/agent-artifact-epidemics.md): reproduction-number law for agents that learn from deployment (simulator + LLM challenge trial).

```bash
pip install -r requirements.txt
python -m pytest -q tests
python -m agents.epidemic.experiments                          # Stage 0 simulator figures + summary.json
python -m agents.llm_pilot.challenge_trial --model model.gguf  # measure tau and gate odds on a GGUF model (CPU)
```
