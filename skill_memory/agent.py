"""Shared agent prompt and action interpreter."""

from dataclasses import dataclass
from json import dumps, loads
from random import Random
from urllib.request import Request, urlopen

from .entropy import ACTION_TEMPERATURE, TOP_K, token_entropy
from .environment import FAMILIES, Outcome, Task, public_evidence, score
from .memory import Experience, Memory, Recall, encode


SYSTEM = (
    "You operate a mock API. Complete the requested workflow in order. "
    'Return only JSON {"calls":[["endpoint","argument"],["endpoint","argument"]]}. '
    "The runtime supplies the same entity as each argument value. "
    "Current operator instructions override memory. Registry entries may be obsolete or unrelated."
)


def registry(task: Task) -> list:
    focal = FAMILIES[task.family]
    other = FAMILIES[task.family ^ 1]
    candidates = sorted(set(focal.original + (focal.migrated or ()) + other.original))
    Random(task.entity).shuffle(candidates)
    return candidates


def prompt(task: Task, recall: Recall) -> str:
    lines = [f"Goal: {task.goal} ({task.entity})", f"Registry: {dumps(registry(task))}"]
    if recall.text:
        lines.append(recall.text)
    if recall.tools:
        lines.append('You may instead return {"tool":"name"} to invoke a listed workflow:')
        lines.extend(f'{tool["name"]}: {tool["description"]}' for tool in recall.tools)
    if task.coaching:
        lines.append(f"Current operator instructions; use this workflow: {encode(task.coaching)}")
    return "\n".join(lines)


class Scripted:
    def act(self, task: Task, recall: Recall, seed: int) -> "Decision":
        if task.coaching:
            return Decision(encode(task.coaching))
        concept = FAMILIES[task.family].name
        for tool in recall.tools:
            if tool["description"].startswith(f"Run workflow: {concept}:"):
                return Decision(dumps({"tool": tool["name"]}))
        return Decision(encode(recall.hint or tuple(registry(task)[:2])))

    def reflect(self, task: Task, attempted: str, outcome: Outcome, seed: int) -> str:
        return outcome.feedback


@dataclass(frozen=True)
class Decision:
    raw: str
    entropy: float | None = None


@dataclass(frozen=True)
class LocalModel:
    url: str
    model: str
    temperature: float = ACTION_TEMPERATURE
    timeout: float = 180

    def generate(self, system: str, message: str, seed: int, measure: bool) -> Decision:
        data = {"model": self.model, "messages": [{"role": "system", "content": system},
                                                  {"role": "user", "content": message}],
                "seed": seed, "temperature": 0, "max_tokens": 55}
        if measure:
            data.update(temperature=self.temperature, top_k=TOP_K, samplers=["top_k", "temperature"],
                        logprobs=True, top_logprobs=TOP_K, post_sampling_probs=True)
        request = Request(self.url.rstrip("/") + "/chat/completions", data=dumps(data).encode(),
                          headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=self.timeout) as response:
            choice = loads(response.read())["choices"][0]
        raw = (choice["message"]["content"] or "").strip()
        if not measure:
            return Decision(raw)
        if raw and not choice.get("logprobs"):
            raise ValueError("llama-server did not return action token probabilities")
        return Decision(raw, token_entropy(choice["logprobs"]) if choice.get("logprobs") else 0.0)

    def act(self, task: Task, recall: Recall, seed: int) -> Decision:
        return self.generate(SYSTEM, prompt(task, recall), seed, True)

    def reflect(self, task: Task, attempted: str, outcome: Outcome, seed: int) -> str:
        return self.generate(
            "Write one short actionable lesson for future API attempts. "
            "Identify the failure and suggest a correction only when supported by the feedback.",
            f"{prompt(task, Recall())}\nAttempt: {attempted}\nRuntime feedback: {outcome.feedback}",
            seed, False).raw


def interpret(raw: str, memory: Memory, task: Task, migrated: bool) -> Outcome:
    try:
        answer = loads(raw)
    except ValueError:
        return Outcome(False, "Invalid JSON")
    if not isinstance(answer, dict):
        return Outcome(False, "Expected a JSON object")
    if set(answer) == {"tool"} and isinstance(answer["tool"], str):
        program = memory.invoke(answer["tool"])
        return score(task, program, migrated) if program else Outcome(False, "Unknown memory tool")
    calls = answer.get("calls")
    if set(answer) != {"calls"} or not isinstance(calls, list) or len(calls) != 2 or not all(
        isinstance(call, list) and len(call) == 2 and all(isinstance(part, str) for part in call)
        for call in calls
    ):
        return Outcome(False, "Expected two [endpoint, argument] pairs or one listed memory tool")
    return score(task, tuple((op, key) for op, key in calls), migrated)


def episode(agent: Scripted | LocalModel, memory: Memory, task: Task, seed: int,
            migrated: bool, learn: bool) -> tuple[Decision, Outcome, str, int]:
    decision = agent.act(task, memory.read(task), seed)
    outcome = interpret(decision.raw, memory, task, migrated)
    first_feedback = outcome.feedback
    attempts = 1
    if not outcome.success and (retry := memory.after_failure(task, outcome)) is not None:
        retry = Recall(f"First attempt failed: {first_feedback}. {retry.text}", retry.hint, retry.tools)
        decision = agent.act(task, retry, seed)
        outcome = interpret(decision.raw, memory, task, migrated)
        attempts += 1
    if learn:
        memory.write(Experience(task, outcome, decision.raw,
                                lambda: agent.reflect(task, decision.raw, outcome, seed),
                                lambda: public_evidence(task)))
    return decision, outcome, first_feedback, attempts
