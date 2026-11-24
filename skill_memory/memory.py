"""Pluggable policy for memory read, tool dispatch, and post-episode writes."""

from collections import Counter
from dataclasses import dataclass
from hashlib import blake2b
from json import dumps, loads
from math import sqrt
import re
from typing import Callable

from .environment import FAMILIES, Outcome, Program, PublicEvidence, Task


def encode(program: Program) -> str:
    return dumps({"calls": program}, separators=(",", ":"))


@dataclass(frozen=True)
class Recall:
    text: str = ""
    hint: Program = ()
    tools: tuple[dict, ...] = ()


@dataclass(frozen=True)
class Experience:
    task: Task
    outcome: Outcome
    attempted: str
    reflect: Callable[[], str]
    search: Callable[[], PublicEvidence]


class Memory:
    def read(self, task: Task) -> Recall:
        return Recall()

    def invoke(self, name: str) -> Program | None:
        return None

    def after_failure(self, task: Task, outcome: Outcome) -> Recall | None:
        return None

    def write(self, experience: Experience) -> None:
        pass


def terms(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def embedding(text: str) -> Counter:
    tokens = terms(text)
    features = tokens + [word[i:i + 3] for word in tokens for i in range(len(word) - 2)]
    return Counter(int.from_bytes(blake2b(x.encode(), digest_size=2).digest(), "little") % 256
                   for x in features)


def cosine(a: Counter, b: Counter) -> float:
    norm = sqrt(sum(x * x for x in a.values()) * sum(x * x for x in b.values()))
    return sum(value * b[key] for key, value in a.items()) / norm if norm else 0.0


@dataclass(frozen=True)
class Entry:
    name: str
    description: str
    program: Program
    step: int
    version: int = 1
    source: str = ""


def description(task: Task) -> str:
    return task.query


class Bank(Memory):
    limit = 6

    def __init__(self):
        self.entries: dict[str, Entry] = {}

    def similarity(self, query: str, entry: Entry) -> float:
        return cosine(embedding(query), embedding(entry.description))

    def nearest(self, query: str) -> Entry | None:
        candidates = [(self.similarity(query, entry), entry.step, entry)
                      for entry in self.entries.values()]
        score, _, entry = max(candidates, key=lambda row: row[:2], default=(0, 0, None))
        return entry if score >= 0.35 else None

    def put(self, entry: Entry) -> None:
        self.entries[entry.name] = entry
        if len(self.entries) > self.limit:
            del self.entries[min(self.entries, key=lambda key: self.entries[key].step)]

    def from_trace(self, task: Task, outcome: Outcome) -> None:
        key = f"skill_{task.family}"
        self.put(Entry(key, description(task), outcome.program, task.step))


class SkillLibrary(Bank):
    def read(self, task: Task) -> Recall:
        entry = self.nearest(task.query)
        if not entry:
            return Recall()
        return Recall(f"Verified executable routine for {entry.description}: {encode(entry.program)}",
                      entry.program)

    def write(self, experience: Experience) -> None:
        if experience.outcome.success:
            self.from_trace(experience.task, experience.outcome)


class SkillMCP(Bank):
    def rpc(self, request: dict) -> dict:
        reply = {"jsonrpc": "2.0", "id": request["id"]}
        if request["method"] == "tools/list":
            return {**reply, "result": {"tools": [
                {"name": entry.name, "description": f"Run workflow: {entry.description}",
                 "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}}
                for entry in self.entries.values()
            ]}}
        if request["method"] == "tools/call":
            params = request["params"]
            entry = self.entries.get(params["name"])
            if entry and params.get("arguments", {}) == {}:
                return {**reply, "result": {"content": [{"type": "text", "text": encode(entry.program)}]}}
            return {**reply, "error": {"code": -32602, "message": "Unknown skill or invalid arguments"}}
        return {**reply, "error": {"code": -32601, "message": "Unknown method"}}

    def read(self, task: Task) -> Recall:
        reply = self.rpc({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        return Recall(tools=tuple(reply["result"]["tools"]))

    def invoke(self, name: str) -> Program | None:
        reply = self.rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                          "params": {"name": name, "arguments": {}}})
        if "result" in reply:
            return tuple(tuple(call) for call in loads(reply["result"]["content"][0]["text"])["calls"])
        return None

    def write(self, experience: Experience) -> None:
        if experience.outcome.success:
            self.from_trace(experience.task, experience.outcome)


class OpenSkill(Bank):
    def read(self, task: Task) -> Recall:
        entry = self.nearest(task.query)
        if not entry:
            return Recall()
        return Recall(f"Sandbox-checked skill from {entry.source}: {encode(entry.program)}", entry.program)

    def write(self, experience: Experience) -> None:
        task = experience.task
        evidence = experience.search()
        if evidence.recipe != evidence.sandbox_expected:
            return
        key = f"skill_{task.family}"
        self.put(Entry(key, description(task), evidence.recipe, task.step, source=evidence.source))


class AutoSkill(Bank):
    def similarity(self, query: str, entry: Entry) -> float:
        a, b = set(terms(query)), set(terms(entry.description))
        return 0.65 * super().similarity(query, entry) + 0.35 * len(a & b) / len(a | b)

    def read(self, task: Task) -> Recall:
        entry = self.nearest(task.query)
        if not entry:
            return Recall()
        return Recall(f"SKILL {entry.name} v{entry.version} | triggers: {entry.description}\n"
                      f"Instructions: {encode(entry.program)}", entry.program)

    def write(self, experience: Experience) -> None:
        task = experience.task
        if not task.coaching:
            return
        neighbor = self.nearest(task.query)
        key = f"skill_{task.family}"
        previous = neighbor if neighbor and neighbor.name == key else None
        if previous and previous.program == task.coaching:
            return
        version = previous.version + 1 if previous else 1
        self.put(Entry(key, description(task), task.coaching, task.step, version))


class Reflection(Memory):
    def __init__(self):
        self.lessons: list[str] = []

    def read(self, task: Task) -> Recall:
        if not self.lessons:
            return Recall()
        return Recall("Recent verbal reflections (use only if relevant): " + " | ".join(self.lessons))

    def write(self, experience: Experience) -> None:
        if not experience.outcome.success:
            lesson = experience.reflect()
            if lesson:
                self.lessons = (self.lessons + [f"{FAMILIES[experience.task.family].name}: {lesson[:240]}"])[-3:]


class KnowledgeCards(Bank):
    def read(self, task: Task) -> Recall:
        entry = self.nearest(task.query)
        if not entry:
            return Recall()
        card = {"concept": entry.description,
                "scope": "Current sandbox; only for this workflow; invalid if a tool rejects the schema",
                "rule": {"calls": entry.program}, "provenance": entry.source,
                "validation": "Observed workflow accepted by runtime"}
        return Recall("Knowledge Card: " + dumps(card, separators=(",", ":")), entry.program)

    def write(self, experience: Experience) -> None:
        if experience.outcome.success:
            task = experience.task
            key = f"skill_{task.family}"
            self.put(Entry(key, description(task), experience.outcome.program, task.step,
                           source=f"episode/{task.step}"))


ARMS = {
    "no-memory": Memory,
    "skill-library": SkillLibrary,
    "skills-mcp": SkillMCP,
    "openskill": OpenSkill,
    "autoskill": AutoSkill,
    "reflection": Reflection,
    "knowledge-cards": KnowledgeCards,
}
