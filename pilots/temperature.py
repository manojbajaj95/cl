import numpy as np


def temper(logp, temperature):
    logits = np.asarray(logp, dtype=np.float64) / temperature
    logits -= logits.max(axis=-1, keepdims=True)
    return logits - np.log(np.exp(logits).sum(axis=-1, keepdims=True))


def entropy(logp):
    return -(np.exp(logp) * logp).sum(axis=-1)


def fit_temperature(blank, full):
    target = float(entropy(full).mean())
    lower, upper = 1e-3, 1e3
    for _ in range(45):
        mid = np.sqrt(lower * upper)
        if entropy(temper(blank, mid)).mean() < target:
            lower = mid
        else:
            upper = mid
    temperature = float(np.sqrt(lower * upper))
    return {"temperature": temperature, "source_queries": len(blank),
            "source_full_entropy": target, "source_blank_entropy": float(entropy(blank).mean()),
            "source_tempered_entropy": float(entropy(temper(blank, temperature)).mean())}
