import json
import os
from pathlib import Path
import re


MODEL = "BAAI/bge-small-en-v1.5"
THRESHOLD = 0.72


def tokens(text):
    return re.findall(r"[a-z0-9]+", text.casefold())


def numeric(text):
    return {word for word in tokens(text) if word.isdecimal()}


# BGE similarity alone can rank antonyms very close; preserve these explicit choices.
OPPOSITES = (
    ({"minimum", "minimize", "smallest", "lowest"}, {"maximum", "maximize", "largest", "highest"}),
    ({"sum", "summing", "add"}, {"count", "counting", "tally"}),
    ({"include", "including", "inclusive"}, {"exclude", "excluding", "exclusive"}),
    ({"higher", "greater", "above", "exceed", "exceeds"}, {"lower", "less", "below", "under"}),
)
DOMAIN_TERMS = (
    {"signed", "balance", "bin", "initial"},
    {"interval", "intervals", "meeting", "meetings", "room"},
    {"routes", "route", "edge", "edges", "path", "paths", "linked"},
)


def conflicts(left, right):
    if numeric(left) != numeric(right):
        return True
    if numeric(left) and (("%" in left) != ("%" in right)):
        return True
    a, b = set(tokens(left)), set(tokens(right))
    a_domains = {i for i, terms in enumerate(DOMAIN_TERMS) if a & terms}
    b_domains = {i for i, terms in enumerate(DOMAIN_TERMS) if b & terms}
    if a_domains and b_domains and a_domains.isdisjoint(b_domains):
        return True

    def output_only(words):
        return "only" in words and bool(words & {"output", "return", "write", "respond"})

    def explanation(words):
        return bool(words & {"explain", "show", "describe"}) and not bool(words & {"without", "not", "no"})

    if (output_only(a) and explanation(b)) or (output_only(b) and explanation(a)):
        return True
    for first, second in OPPOSITES:
        if (a & first and not a & second and b & second and not b & first
                or a & second and not a & first and b & first and not b & second):
            return True
    return False


class SemanticSimilarity:
    def __init__(self, texts):
        from fastembed import TextEmbedding

        texts = sorted(set(texts))
        cache = os.environ.get("HW1_EMBED_CACHE", str(Path.home() / ".cache" / "hw1-fastembed"))
        model = TextEmbedding(MODEL, cache_dir=cache, threads=2)
        self.vectors = dict(zip(texts, model.embed(texts)))

    def __call__(self, left, right):
        if left == right:
            return 1.0
        if conflicts(left, right):
            return 0.0
        return float(self.vectors[left] @ self.vectors[right])


def main():
    data = json.loads(Path(__file__).with_name("clustering_audit.json").read_text())
    similarity = SemanticSimilarity([row[side] for row in data for side in ("left", "right")])
    counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for row in data:
        value = similarity(row["left"], row["right"])
        counts[("t" if (value >= THRESHOLD) == row["match"] else "f") + ("p" if value >= THRESHOLD else "n")] += 1
        print(f"{value:.3f} expected={str(row['match']):5s} {row['left']} | {row['right']}")
    print(f"Threshold {THRESHOLD:.2f}: {counts}")


if __name__ == "__main__":
    main()
