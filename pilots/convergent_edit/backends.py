import hashlib
import json
import os
import random
import re
import sqlite3
import threading
import time
import urllib.error
from email.utils import parsedate_to_datetime
import urllib.request

from .environment import TASK_SHAPES, TRAIN, harness


def unit(*parts):
    return int.from_bytes(hashlib.sha256(repr(parts).encode()).digest()[:8], "big") / 2**64


class ResponseCache:
    def __init__(self, path):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.lock = threading.Lock()
        self.request_locks = [threading.Lock() for _ in range(64)]
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS responses (hash TEXT PRIMARY KEY, content TEXT NOT NULL)")
        self.db.execute("CREATE TABLE IF NOT EXISTS attempts (scope TEXT PRIMARY KEY, count INTEGER NOT NULL)")

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.db.close()

    def lookup_or_request(self, url, body, request):
        digest = hashlib.sha256(url.encode() + b"\0" + body).hexdigest()
        with self.request_locks[int(digest[:2], 16) % len(self.request_locks)]:
            with self.lock:
                row = self.db.execute("SELECT content FROM responses WHERE hash = ?", (digest,)).fetchone()
            if row is not None:
                return row[0]
            content = request()
            with self.lock, self.db:
                self.db.execute("INSERT OR IGNORE INTO responses VALUES (?, ?)", (digest, content))
            return content

    def attempts(self, scope):
        with self.lock:
            row = self.db.execute("SELECT count FROM attempts WHERE scope = ?", (scope,)).fetchone()
            return row[0] if row else 0

    def reserve_attempt(self, scope, limit):
        with self.lock, self.db:
            self.db.execute("BEGIN IMMEDIATE")
            row = self.db.execute("SELECT count FROM attempts WHERE scope = ?", (scope,)).fetchone()
            count = row[0] if row else 0
            if limit and count >= limit:
                raise RuntimeError(f"Evolver HTTP attempt cap ({limit}) reached; raise it only after quota permits")
            self.db.execute("INSERT OR REPLACE INTO attempts VALUES (?, ?)", (scope, count + 1))


OPENROUTER_URL = "https://openrouter.ai/api/v1"
OPENROUTER_MODEL = "nvidia/nemotron-3.5-lightning:free"


class Chat:
    def __init__(self, url, model, key=None, *, cache=None, headers=None, options=None, rpm=0, retries=5,
                 max_retry_wait=300, track_attempts=False, limit=0):
        self.url = url.rstrip("/") + "/chat/completions"
        self.model = model
        self.key = key
        self.cache = cache
        self.headers = {"Content-Type": "application/json", **(headers or {})}
        self.options = options or {}
        self.interval = 60 / rpm if rpm else 0
        self.retries = retries
        self.max_retry_wait = max_retry_wait
        self.scope = self.url + "\n" + model if track_attempts else None
        self.limit = limit
        self.rate_lock = threading.Lock()
        self.ready_at = 0.0
        self.stopped = threading.Event()

    def next_request(self):
        while not self.stopped.is_set():
            with self.rate_lock:
                now = time.monotonic()
                remaining = self.ready_at - now
                if remaining <= 0:
                    self.ready_at = now + self.interval
                    return
            self.stopped.wait(remaining)
        raise RuntimeError("Request queue stopped after HTTP errors; rerun with the same cache to resume")

    def __call__(self, system, prompt, seed, temperature, max_tokens, **options):
        payload = dict(model=self.model, messages=[dict(role="system", content=system),
                                                   dict(role="user", content=prompt)],
                       seed=seed, temperature=temperature, max_tokens=max_tokens, **{**self.options, **options})
        body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        if self.cache is not None:
            return self.cache.lookup_or_request(self.url, body, lambda: self.send(body))
        return self.send(body)

    def send(self, body):
        request = urllib.request.Request(self.url, body, headers=self.headers)
        if self.key:
            request.add_header("Authorization", f"Bearer {self.key}")
        for attempt in range(self.retries + 1):
            self.next_request()
            if self.cache is not None and self.scope is not None:
                try:
                    self.cache.reserve_attempt(self.scope, self.limit)
                except RuntimeError:
                    self.stopped.set()
                    raise
            try:
                with urllib.request.urlopen(request, timeout=300) as response:
                    return json.load(response)["choices"][0]["message"]["content"] or ""
            except urllib.error.HTTPError as exc:
                status = exc.code
                retry_after = exc.headers.get("Retry-After")
                exc.close()
                if not (status == 429 or 500 <= status < 600):
                    self.stopped.set()
                    raise
                delay = min(60, 2**min(attempt, 6))
                delay += random.uniform(0, delay / 4)
                if retry_after:
                    try:
                        delay = max(delay, float(retry_after))
                    except ValueError:
                        try:
                            delay = max(delay, parsedate_to_datetime(retry_after).timestamp() - time.time())
                        except (ValueError, OverflowError):
                            pass
                if attempt == self.retries or delay > self.max_retry_wait:
                    self.stopped.set()
                    raise RuntimeError(
                        f"HTTP {status}; retry budget exhausted or server asked to wait {delay:.0f}s. "
                        "Rerun with the same cache after quota or service recovers."
                    ) from exc
                with self.rate_lock:
                    self.ready_at = max(self.ready_at, time.monotonic() + delay)


class ModelEvolver:
    def __init__(self, chat):
        self.chat = chat

    def edit(self, task, completion, seed):
        system = (
            "Write one reusable instruction for a small solver's shared playbook, based on the "
            "episode summary. Prescribe a concrete check or thinking habit that still applies if "
            "the next task uses different entities and asks for a different calculation. Do not "
            "repeat the exercise description or the base prompt. Write one imperative sentence only."
        )
        prompt = f"Base instructions: {harness(())}\nEpisode summary: {json.dumps(edit_evidence(task, completion))}"
        output = self.chat(system, prompt, seed, 0.85, 48).strip()
        return clean_edit(output)

    def edit_batch(self, episodes, seed):
        system = (
            "Write reusable instructions for a small solver's shared playbook. Treat each "
            "episode summary independently. Write one imperative sentence per episode, under 25 "
            "words, prescribing a concrete check or thinking habit that still applies if the "
            "next task uses different entities and asks for a different calculation. Do not "
            "repeat the exercise description or the base prompt. "
            "Return only a JSON array of strings, one instruction per episode in input order."
        )
        rows = [edit_evidence(task, completion) for task, completion in episodes]
        prompt = f"Base instructions: {harness(())}\nEpisodes: {json.dumps(rows)}"
        candidates = parse_array(self.chat(system, prompt, seed, 0.85, 72 * len(rows)), len(rows))
        return [clean_edit(value) for value in candidates]

    def curate(self, edit, traces, seed):
        system = (
            "You curate a reusable playbook for a small task solver. Given a proposed rule and "
            "its reflection traces, score it 0-10 for actionable, nonredundant, broadly "
            "reusable advice. Discount task-specific details and lessons that regress. "
            "Return only the integer score."
        )
        prompt = f"Current playbook: {harness(())}\nProposed rule: {edit}\nTraces: {json.dumps(traces)}"
        match = re.fullmatch(r"(10|[0-9])", self.chat(system, prompt, seed, 0, 8).strip())
        return int(match[1]) if match else 0

    def curate_batch(self, candidates, seed):
        system = (
            "You curate a reusable playbook for a small task solver. Score each proposed rule "
            "0-10 for actionable, nonredundant, broadly reusable advice using its reflection "
            "traces. Discount task-specific details and lessons that regress. Return only a "
            "JSON array of integer scores, one per candidate in input order."
        )
        prompt = f"Base playbook: {harness(())}\nCandidates: {json.dumps(candidates)}"
        scores = parse_array(self.chat(system, prompt, seed, 0, 20 * len(candidates)), len(candidates))
        return [value if type(value) is int and 0 <= value <= 10 else 0 for value in scores]


def clean_edit(output):
    if not isinstance(output, str) or not output.strip():
        return None
    edit = output.strip().splitlines()[0].strip(" `-*\"")
    return edit if 12 <= len(edit) <= 280 and any(c.isalpha() for c in edit) else None


def edit_evidence(task, completion):
    value = completion.strip()
    delta = int(value) - task.answer if re.fullmatch(r"-?[0-9]{1,12}", value) else None
    grade = ("invalid integer format" if delta is None else "exact" if delta == 0
             else "too low" if delta < 0 else "too high")
    return dict(
        task_shape=TASK_SHAPES[task.family],
        row_count=len(task.records),
        picked_a_listed_integer=value in set(map(str, task.choices)),
        grading_feedback=grade,
    )


def parse_array(output, count):
    start = output.find("[")
    if start >= 0:
        try:
            candidates, _ = json.JSONDecoder().raw_decode(output[start:])
            if isinstance(candidates, list) and len(candidates) == count:
                return candidates
        except json.JSONDecodeError:
            pass
    return [None] * count


class TaskModel:
    def __init__(self, chat, constrain_choices=False):
        self.chat = chat
        self.constrain_choices = constrain_choices

    def solve(self, task, edits, seed, variant=0):
        options = {}
        if self.constrain_choices:
            options["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "answer", "schema": {"type": "integer", "enum": sorted(task.choices)}},
            }
        return self.chat(harness(edits), task.prompt(variant), seed, 0.4, 16, **options)


class Stub:
    def edit(self, task, completion, seed):
        index = task.index % 26 + 11 * TRAIN.index(task.family)
        return f"Apply simulated rule number {index} before responding."

    def curate(self, edit, traces, seed):
        return unit(edit)

    def edit_batch(self, episodes, seed):
        return [self.edit(task, completion, seed) for task, completion in episodes]

    def curate_batch(self, candidates, seed):
        return [self.curate(edit, traces, seed) for edit, traces in candidates]

    def solve(self, task, edits, seed, variant=0):
        threshold = 0.45
        if edits:
            threshold = sum(0.1 + 0.8 * unit(edit) for edit in edits) / len(edits)
        draw = unit(task.family, task.index, variant, seed if not edits else 0)
        return str(task.answer + (draw >= threshold))


def correct(task, completion):
    return completion.strip() == str(task.answer)


def backends(mode, cache=None):
    if mode == "stub":
        stub = Stub()
        return stub, stub, "stub", "stub"
    task_name = os.environ.get("TASK_MODEL", "qwen3-0.6b")
    task = TaskModel(Chat(os.environ.get("TASK_BASE_URL", "http://127.0.0.1:8082/v1"),
                          task_name, os.environ.get("TASK_API_KEY"), cache=cache),
                     constrain_choices=os.environ.get("TASK_CONSTRAIN_CHOICES", "1") == "1")
    if mode == "local":
        url = os.environ.get("EVOLVER_BASE_URL", "http://127.0.0.1:8081/v1")
        model = os.environ.get("EVOLVER_MODEL", "qwen2.5-1.5b-instruct")
    else:
        url = os.environ.get("EVOLVER_BASE_URL", OPENROUTER_URL)
        model = os.environ.get("EVOLVER_MODEL", OPENROUTER_MODEL)
    openrouter = url.rstrip("/") == OPENROUTER_URL
    key = os.environ.get("EVOLVER_API_KEY")
    headers = {}
    if openrouter:
        key = os.environ.get("OPENROUTER_API_KEY") or key
        for header, env_name in (("HTTP-Referer", "OPENROUTER_HTTP_REFERER"), ("X-Title", "OPENROUTER_X_TITLE")):
            if os.environ.get(env_name):
                headers[header] = os.environ[env_name]
    rpm = int(os.environ.get("EVOLVER_REQUESTS_PER_MINUTE", "20" if openrouter and model.endswith(":free") else "0"))
    retries = int(os.environ.get("EVOLVER_MAX_RETRIES", "5"))
    limit = int(os.environ.get("EVOLVER_MAX_REQUESTS", "0"))
    if min(rpm, retries, limit) < 0:
        raise ValueError("Evolver request rate, retry count, and HTTP attempt cap must be nonnegative")
    options = {"reasoning": {"enabled": False}} if openrouter and model.startswith("nvidia/nemotron-") else {}
    evolver = ModelEvolver(Chat(url, model, key, cache=cache, headers=headers, options=options, rpm=rpm,
                               retries=retries, track_attempts=True, limit=limit))
    return evolver, task, model, task_name
