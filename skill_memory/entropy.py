"""Exact entropy under the configured finite next-token sampler."""

from math import isclose, log
from statistics import mean
from typing import Callable

TOP_K = 20
ACTION_TEMPERATURE = 0.7
SOURCE_SEEDS = (101, 103)


def token_entropy(logprobs: dict) -> float:
    entropies = []
    for token in logprobs["content"]:
        probs = [candidate["prob"] for candidate in token["top_probs"]]
        if not probs or not isclose(sum(probs), 1.0, abs_tol=1e-5):
            raise ValueError("Expected complete post-sampling token probabilities from llama-server")
        entropies.append(-sum(p * log(p) for p in probs if p > 0))
    # Empty outputs can occur if the first sampled token is EOS and the server
    # omits that token from the reported trace.
    return mean(entropies) if entropies else 0.0


def fit_temperature(target: float, measure: Callable[[float], float]) -> tuple[float, dict]:
    profiles = {temp: measure(temp) for temp in (0.15, 0.35, 0.5, ACTION_TEMPERATURE, 0.9, 1.15, 1.5)}
    for _ in range(2):
        ordered = sorted(profiles)
        best = min(ordered, key=lambda temp: abs(profiles[temp] - target))
        pos = ordered.index(best)
        for neighbor in ordered[max(0, pos - 1):pos] + ordered[pos + 1:pos + 2]:
            temp = round((best + neighbor) / 2, 4)
            if temp not in profiles:
                profiles[temp] = measure(temp)
    fitted = min(profiles, key=lambda temp: (abs(profiles[temp] - target), temp))
    return fitted, dict(sorted(profiles.items()))
