#!/usr/bin/env python3
"""A named SOUL that cannot be read exits 2. Bad JSON is not echoed."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_post.py"
TOKEN = "incomplete-json-probe"


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(SCORE), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScorePostBadInput(unittest.TestCase):
    def test_post_scores(self):
        result = run(["--post", "We cut onboarding from 14 days to 2. Here is the checklist."])
        self.assertIn(result.returncode, (0, 1))
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_soul_exits_2(self):
        result = run(["--post", "A real post.", "--soul", str(ROOT / "no-such-soul.md")])
        self.assertEqual(result.returncode, 2)
        self.assertIn("file not found", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_bad_json_hides_bytes(self):
        result = run(["--stdin"], stdin='{"post": "' + TOKEN)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(TOKEN, result.stderr + result.stdout)

    def test_phrases_must_not_crash_when_not_a_list(self):
        result = run(["--stdin"], stdin='{"post":"A real post.","phrases_used":"nope"}')
        self.assertIn(result.returncode, (0, 1))
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
