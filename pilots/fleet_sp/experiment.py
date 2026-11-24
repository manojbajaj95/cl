import argparse
from concurrent.futures import ProcessPoolExecutor
from functools import partial
import json
from pathlib import Path
import random

import numpy as np
from scipy.special import digamma, expit, softmax


N_AGENTS = 20
N_EXPOSED = 4
K = 4
ROUTES = (
    ("create-record", "POST", "PUT"),
    ("read-record", "GET", "HEAD"),
    ("edit-record", "PATCH", "PUT"),
    ("remove-record", "DELETE", "POST"),
)
ARMS = ("elicited_sp", "logprob_sp", "mean_pi", "majority", "confidence",
        "minority", "bp_td", "regime_retrieval")
SYSTEM = "You are an agent learning a private API. Use successful calls as evidence."


class Model:
    def __init__(self, path, threads):
        from llama_cpp import Llama

        self.llm = Llama(model_path=path, n_ctx=512, n_threads=threads,
                         n_threads_batch=threads, verbose=False)

    def tokens(self, prompt):
        return self.llm.tokenize(prompt.encode(), add_bos=False, special=True)

    def distribution(self, prompt, labels, temperature=1):
        continuations = [self.tokens(f"{prompt} {label}") for label in labels]
        tokens = continuations[0][:-1]
        if any(continuation[:-1] != tokens for continuation in continuations):
            raise ValueError(f"Expected single-token answers: {labels}")
        if len(tokens) >= self.llm.n_ctx():
            raise ValueError("Prompt exceeds context")
        prefix = 0
        for old, new in zip(self.llm.input_ids[:self.llm.n_tokens], tokens[:-1]):
            if old != new:
                break
            prefix += 1
        self.llm.n_tokens = prefix
        self.llm.eval(tokens[prefix:])
        logits = self.llm._ctx.get_logits()
        return softmax([logits[continuation[-1]] / temperature for continuation in continuations])


def chat(text, completion):
    return (f"<|im_start|>system\n{SYSTEM}<|im_end|>\n"
            f"<|im_start|>user\n{text}<|im_end|>\n<|im_start|>assistant\n{completion}")


def draw_agent(model, rng, regimes, history):
    proposals = []
    for regime_id, regime in enumerate(regimes):
        for route_id, (route, *methods) in enumerate(ROUTES):
            choices = methods if rng.randrange(2) else methods[::-1]
            prefix = (f"Your accepted API calls:\n{history}\n\n"
                      f"Write one proposed lesson for {regime} /{route}. "
                      "Choose the method you would recommend, even if you must infer it "
                      f"from other calls. A: {choices[0]}. B: {choices[1]}.")
            probs = model.distribution(chat(prefix, "Choice:"), ("A", "B"), temperature=0.7)
            method = choices[int(rng.random() >= probs[0])]
            prompt = (f"{prefix}\nYou chose {method}. How confident are you this is correct? "
                      "Answer 1 (guess), 2 (somewhat), 3 (very), or 4 (certain).")
            confidence = 1 + int(model.distribution(chat(prompt, "Confidence:"), "1234").argmax())
            proposals.append((regime_id, route_id, method, confidence))
    return proposals


def lesson_text(lesson, regimes):
    regime, route, method = lesson
    return f"{regimes[regime]} /{ROUTES[route][0]}: {method}"


def rating_prefix(history, lesson):
    return (f"Your accepted API calls:\n{history}\n\n"
            f"Proposed lesson (regime, endpoint, method): {lesson}.\n")


def support(model, prefix):
    question = "Would you endorse this lesson as correct? Answer Yes or No."
    return float(model.distribution(chat(prefix + question, "Answer:"), ("Yes", "No"))[0])


def forecast(model, prefix):
    question = ("Predict how many of the 20 agents will endorse this lesson. Others may "
                "have seen different calls. Answer a digit 0 to 9: 0 means nobody, "
                "9 means everyone and intermediate digits are evenly spaced.")
    return int(model.distribution(chat(prefix + question, "Prediction:"), "0123456789").argmax()) / 9


def vote_confidence(model, prefix, vote):
    answer = "Yes" if vote else "No"
    question = (f"You voted {answer}. How confident are you in that vote? "
                "Answer 1 (guess), 2 (somewhat), 3 (very), or 4 (certain).")
    return 1 + int(model.distribution(chat(prefix + question, "Confidence:"), "1234").argmax())


def write_json(path, data):
    pending = path.with_suffix(".tmp")
    pending.write_text(json.dumps(data, indent=2) + "\n")
    pending.replace(path)


def fleet(seed, model_path, threads, out):
    path = out / f"fleet-{seed}.json"
    if path.exists():
        return json.loads(path.read_text())
    rng = random.Random(seed)
    model = Model(model_path, threads)
    regimes = rng.sample(["red", "blue", "gold", "pink", "lime", "gray"], 2)
    exposed = sorted(rng.sample(range(N_AGENTS), N_EXPOSED))
    histories, proposals = [], []
    for agent in range(N_AGENTS):
        facts = [
            f"{regimes[regime]} /{route}/{rng.randrange(1000, 5000)}: {methods[regime]} accepted"
            for regime in range(2 if agent in exposed else 1)
            for route, *methods in ROUTES
        ]
        rng.shuffle(facts)
        history = "\n".join(facts)
        histories.append(history)
        proposals.append(draw_agent(model, rng, regimes, history))

    pool = sorted({proposal[:3] for agent in proposals for proposal in agent})
    if len(pool) < K:
        raise ValueError("Not enough distinct authored lessons to fill memory")
    authors = [max(conf for agent in proposals for *key, conf in agent if tuple(key) == lesson)
               for lesson in pool]
    p0 = [support(model, rating_prefix("(no calls recorded)", lesson_text(item, regimes)))
          for item in pool]
    pi, predicted, confidence = [], [], []
    for agent, history in enumerate(histories):
        votes, meta, certainty = [], [], []
        for item in pool:
            prefix = rating_prefix(history, lesson_text(item, regimes))
            p = support(model, prefix)
            votes.append(p)
            meta.append(forecast(model, prefix))
            certainty.append(vote_confidence(model, prefix, p >= .5))
        pi.append(votes)
        predicted.append(meta)
        confidence.append(certainty)
        if (agent + 1) % 5 == 0:
            print(f"fleet {seed}: rated {agent + 1}/{N_AGENTS}", flush=True)

    data = dict(seed=seed, regimes=regimes, exposed=exposed, histories=histories,
                proposals=proposals, pool=pool, authors=authors, p0=p0, pi=pi,
                predicted=predicted, confidence=confidence)
    write_json(path, data)
    return data


def exposure_r(data, subset="true"):
    rare = [i for i, (regime, route, method) in enumerate(data["pool"])
            if regime == 1 and (subset == "all" or (method == ROUTES[route][2]) == (subset == "true"))]
    if not rare:
        return 0.0
    forecasts = np.asarray(data["predicted"])[:, rare].mean(axis=1)
    experienced = np.isin(np.arange(N_AGENTS), data["exposed"])
    return float(np.corrcoef(forecasts, experienced)[0, 1]) if np.ptp(forecasts) else 0.0


def bp_td(votes, family=False):
    votes = votes.astype(float)
    n_agents, n_lessons = votes.shape
    agreement = (votes[:, None, :] == votes[None, :, :]).mean(axis=2)
    agree = 2 * agreement - 1
    np.fill_diagonal(agree, 0)
    weights = (np.full(n_agents, 1 / n_agents) if family
               else 1 / (1 + (agree >= .5).sum(axis=1)))
    prior = np.asarray([2., 1.])
    alpha, beta = (np.full(n_agents, param) for param in prior)
    signed_votes = 2 * votes - 1
    beliefs = np.full(n_lessons, .5)
    degrees = np.abs(agree).sum(axis=1)
    for iteration in range(100):
        update = expit((weights * (digamma(alpha) - digamma(beta))) @ signed_votes)
        new_beliefs = .7 * update + .3 * beliefs if iteration else update
        if np.max(np.abs(new_beliefs - beliefs)) < 1e-4:
            return new_beliefs
        beliefs = new_beliefs
        correct = (votes * beliefs + (1 - votes) * (1 - beliefs)).sum(axis=1)
        alpha, beta = prior[0] + correct, prior[1] + n_lessons - correct
        total = alpha + beta
        centered = alpha / total - .5
        neighborhood = np.divide(agree @ centered, degrees,
                                 out=np.zeros_like(centered), where=degrees > 0)
        reliability = np.clip(.5 + .6 * centered + .4 * neighborhood, 1e-3, 1 - 1e-3)
        alpha, beta = reliability * total, (1 - reliability) * total
    return beliefs


def rank(data, controls=True):
    pi = np.asarray(data["pi"])
    votes = pi >= .5
    actual = votes.mean(axis=0)
    scores = {
        "elicited_sp": actual - np.mean(data["predicted"], axis=0),
        "logprob_sp": pi.mean(axis=0) - data["p0"],
        "mean_pi": pi.mean(axis=0),
    }
    if not controls:
        return scores
    confidence = np.asarray(data["confidence"])
    authors = np.asarray(data["authors"])
    return scores | {
        "majority": actual,
        "confidence": (confidence * votes).sum(axis=0) / confidence.sum(axis=0),
        "minority": 5 * (actual < .5) + authors,
        "bp_td": bp_td(votes),
        "bp_td_family": bp_td(votes, family=True),
    }


def memory_for(arm, scores, pool, tie, regime, route):
    if arm == "regime_retrieval":
        keys = lambda i: (pool[i][0] == regime, pool[i][1] == route, scores["majority"][i], tie[i])
    else:
        keys = lambda i: (scores[arm][i], tie[i])
    indices = sorted(range(len(pool)), key=keys, reverse=True)[:K]
    return tuple(sorted(indices, key=lambda i: tie[i]))


def evaluate(data, model_path, threads, arms, out):
    seed = data["seed"]
    path = out / f"eval-{seed}.json"
    if path.exists():
        saved = json.loads(path.read_text())
        if set(saved["correct"]) == set(arms):
            return saved
    model = Model(model_path, threads)
    rng = random.Random(seed + 100_000)
    regimes, pool = data["regimes"], data["pool"]
    tie = rng.sample(range(len(pool)), len(pool))
    scores = rank(data, controls="regime_retrieval" in arms)
    correct = {arm: [[], []] for arm in arms}
    cache = {}
    contexts = []
    for regime, name in enumerate(regimes):
        for route, (endpoint, *verbs) in enumerate(ROUTES):
            memories = {arm: memory_for(arm, scores, pool, tie, regime, route) for arm in arms}
            contexts.append(dict(regime=regime, route=route, memories=memories))
            for sample in range(4):
                identifier = rng.randrange(5000, 9999)
                options = verbs if (sample + route) % 2 else verbs[::-1]
                token_counts = set()
                for arm, indices in memories.items():
                    lines = "\n".join(lesson_text(pool[i], regimes) for i in indices)
                    prompt = chat(f"Fleet lessons (some may be mistaken):\n{lines}\n\n"
                                  f"Choose the method for {name} /{endpoint}/{identifier}. "
                                  f"A: {options[0]}. B: {options[1]}.", "Choice:")
                    token_counts.add(len(model.tokens(prompt)))
                    if prompt not in cache:
                        cache[prompt] = int(model.distribution(prompt, "AB").argmax())
                    correct[arm][regime].append(int(options[cache[prompt]] == verbs[regime]))
                if len(token_counts) != 1:
                    raise ValueError("Unequal evaluation prompt lengths across arms")
    result = dict(seed=seed, correct=correct, contexts=contexts,
                  scores={arm: score.tolist() for arm, score in scores.items()})
    write_json(path, result)
    print(f"fleet {seed}: evaluated {len(arms)} arms", flush=True)
    return result


def summarize(values):
    values = np.asarray(values)
    rng = np.random.default_rng(8175)
    index = rng.integers(len(values), size=(20_000, len(values)))
    return [float(values.mean()), *map(float, np.quantile(values[index].mean(axis=1), [.025, .975]))]


def pool_statistics(data):
    rare = [i for i, (regime, route, method) in enumerate(data["pool"])
            if regime == 1 and method == ROUTES[route][2]]
    holders = set(data["exposed"])
    proposals = [{tuple(row[:3]) for row in agent} for agent in data["proposals"]]
    rare_proposals = [len({tuple(data["pool"][i]) for i in rare} & authored)
                      for authored in proposals]
    endorsed = np.asarray(data["pi"])[:, rare] >= .5
    return dict(seed=data["seed"], pool_size=len(data["pool"]), true_rare=len(rare),
                mean_true_rare_proposed_exposed=float(np.mean(
                    [count for i, count in enumerate(rare_proposals) if i in holders])),
                mean_true_rare_proposed_unexposed=float(np.mean(
                    [count for i, count in enumerate(rare_proposals) if i not in holders])),
                true_rare_vote_shares=endorsed.mean(axis=0).tolist())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seeds", nargs="+", type=int, default=list(range(4)))
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--threads", type=int, default=2)
    args = parser.parse_args()
    if len(set(args.seeds)) != len(args.seeds) or len(args.seeds) < 3:
        parser.error("Provide at least three distinct fleet seeds")
    args.out.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        fleets = list(executor.map(partial(fleet, model_path=args.model, threads=args.threads,
                                          out=args.out), args.seeds))
        per_fleet_r = [exposure_r(data) for data in fleets]
        gate = summarize(per_fleet_r)
        print(f"Gate r mean, 95% CI: {gate}; per fleet: {per_fleet_r}", flush=True)
        arms = ARMS + ("bp_td_family",) if gate[0] >= .2 else ARMS[:3]
        results = list(executor.map(partial(evaluate, model_path=args.model, threads=args.threads,
                                           arms=arms, out=args.out), fleets))
    accuracy = {arm: np.asarray([result["correct"][arm] for result in results]).mean(axis=2)
                for arm in arms}
    summary = dict(seeds=args.seeds, gate=gate, per_fleet_r=per_fleet_r, gate_passed=gate[0] >= .2,
                   exposure_diagnostics={key: summarize([exposure_r(data, key) for data in fleets])
                                         for key in ("all", "false")},
                   pools=[pool_statistics(data) for data in fleets],
                   by_fleet={arm: values.tolist() for arm, values in accuracy.items()},
                   accuracy={arm: [summarize(values[:, i]) for i in range(2)]
                             for arm, values in accuracy.items()},
                   differences={f"{a}_minus_{b}": [summarize((accuracy[a] - values)[:, i])
                                                       for i in range(2)]
                                for a in ("elicited_sp", "logprob_sp")
                                for b, values in accuracy.items() if a != b})
    write_json(args.out / "summary.json", summary)
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
