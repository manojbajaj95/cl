from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

from .backends import Chat, OPENROUTER_MODEL, OPENROUTER_URL, ResponseCache, backends


@contextmanager
def mock_provider(responses):
    requests = []
    pending = iter(responses)

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            requests.append((self.path, self.headers, body))
            status, retry_after = next(pending)
            self.send_response(status)
            if retry_after is not None:
                self.send_header("Retry-After", retry_after)
            self.end_headers()
            if status == 200:
                self.wfile.write(b'{"choices":[{"message":{"content":"ok"}}]}')

        def log_message(self, *args):
            pass

    with ThreadingHTTPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}/api/v1", requests
        finally:
            server.shutdown()
            thread.join()


class BackendTest(unittest.TestCase):
    @patch.dict("os.environ", {"OPENROUTER_API_KEY": "test-token", "OPENROUTER_HTTP_REFERER": "https://example.test",
                              "OPENROUTER_X_TITLE": "HW1"}, clear=True)
    def test_openrouter_default_configuration(self):
        evolver, _, name, _ = backends("api")
        self.assertEqual(name, OPENROUTER_MODEL)
        self.assertEqual(evolver.chat.url, OPENROUTER_URL + "/chat/completions")
        self.assertEqual(evolver.chat.key, "test-token")
        self.assertEqual(evolver.chat.headers["HTTP-Referer"], "https://example.test")
        self.assertEqual(evolver.chat.headers["X-Title"], "HW1")
        self.assertEqual(evolver.chat.interval, 3)
        self.assertEqual(evolver.chat.options, {"reasoning": {"enabled": False}})

    def test_retry_and_disk_resume(self):
        responses = [(429, "1.3"), (503, None), (200, None), (200, None)]
        with mock_provider(responses) as (url, requests), tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "responses.sqlite3"
            start = time.monotonic()
            with ResponseCache(path) as cache, patch("pilots.convergent_edit.backends.random.uniform", return_value=0):
                client = Chat(url, OPENROUTER_MODEL, "test-token", cache=cache)
                self.assertEqual(client("base", "question", 11, 0.4, 16), "ok")
            self.assertGreaterEqual(time.monotonic() - start, 3.29)
            with ResponseCache(path) as cache:
                client = Chat(url, OPENROUTER_MODEL, cache=cache)
                self.assertEqual(client("base", "question", 11, 0.4, 16), "ok")
                self.assertEqual(len(requests), 3)
                self.assertEqual(client("base", "question", 29, 0.4, 16), "ok")
            self.assertEqual(len(requests), 4)
            path, headers, body = requests[0]
            self.assertEqual(path, "/api/v1/chat/completions")
            self.assertEqual(headers["Authorization"], "Bearer test-token")
            self.assertEqual(body["seed"], 11)
            self.assertEqual(body["model"], OPENROUTER_MODEL)

    def test_long_retry_after_exits_without_caching_error(self):
        with mock_provider([(429, "86400"), (200, None)]) as (url, requests), tempfile.TemporaryDirectory() as directory:
            with ResponseCache(Path(directory) / "responses.sqlite3") as cache:
                with self.assertRaisesRegex(RuntimeError, "HTTP 429.*86400s"):
                    Chat(url, OPENROUTER_MODEL, cache=cache)("base", "question", 11, 0.4, 16)
                self.assertEqual(Chat(url, OPENROUTER_MODEL, cache=cache)("base", "question", 11, 0.4, 16), "ok")
            self.assertEqual(len(requests), 2)

    def test_attempt_limit_persists_and_cache_hits_do_not_count(self):
        with mock_provider([(200, None), (200, None)]) as (url, requests), tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "responses.sqlite3"
            with ResponseCache(path) as cache:
                first = Chat(url, OPENROUTER_MODEL, cache=cache, track_attempts=True, limit=1)
                self.assertEqual(first("base", "question", 11, 0.4, 16), "ok")
                self.assertEqual(cache.attempts(first.scope), 1)
            with ResponseCache(path) as cache:
                second = Chat(url, OPENROUTER_MODEL, cache=cache, track_attempts=True, limit=1)
                self.assertEqual(second("base", "question", 11, 0.4, 16), "ok")
                with self.assertRaisesRegex(RuntimeError, "attempt cap"):
                    second("base", "new question", 11, 0.4, 16)
                self.assertEqual(cache.attempts(second.scope), 1)
            self.assertEqual(len(requests), 1)


if __name__ == "__main__":
    unittest.main()
