"""Post hoc assay check: remove the binding, not just its rule marker."""
import argparse
import json
import random
from pathlib import Path

from run import OLD, QUEUES, SYLLABLES, TARGET, Reader, line, prompt, rows

HERE = Path(__file__).resolve().parent


def unbound_key(case, reader):
    rng = random.Random(2000 + case["seed"])
    excluded = {OLD, *case["focal"], *case["control"], *case["notes"]}
    length = len(reader.tokens(line(OLD, TARGET)))
    while True:
        key = "".join(rng.choices(SYLLABLES, k=3))
        if key not in excluded and len(reader.tokens(line(key, TARGET, active=False))) == length:
            return key


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8089")
    args = parser.parse_args()
    reader = Reader(args.url)
    result = []
    for case in json.loads((HERE / "run.json").read_text())["holdout"]:
        active = rows(case, "focal", 0)
        vacant = active[:]
        key = unbound_key(case, reader)
        vacant[case["old_slot"]] = line(key, TARGET, active=False)
        tokens = reader.tokens(prompt(vacant, OLD, 0))
        if len(tokens) != case["old_reads"][0]["token_count"]:
            raise ValueError("Token length changed on binding removal")
        result.append(dict(seed=case["seed"], removed_key=key,
                           active=case["old_reads"][0]["empty"], removed=reader.score(tokens)))

    (HERE / "binding_audit.json").write_text(json.dumps(result, separators=(",", ":")) + "\n")
    for condition in ("active", "removed"):
        n = sum(max(QUEUES, key=lambda q: row[condition][q - 1]) == TARGET
                for row in result)
        print(f"{condition}: {n}/{len(result)} old answers correct")


if __name__ == "__main__":
    main()
