#!/usr/bin/env python3
"""score.py prints one post, one network, and one receipt, or refuses a blast."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CELL = "super-secret-cell"


def run(args, stdin=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "score.py"), *args],
        input=stdin,
        capture_output=True,
        text=True,
    )


class ScoreSocialPost(unittest.TestCase):
    def test_good_draft_prints_three(self):
        result = run(["--file", str(ROOT / "examples" / "post-good.json")])
        self.assertEqual(result.returncode, 0)
        self.assertIn("post: One claim for one buyer on one network.", result.stdout)
        self.assertIn("network: LinkedIn", result.stdout)
        self.assertIn("receipt: 14 replies in 30 days from this single post.", result.stdout)
        self.assertNotIn("a ten-network blast", result.stdout)

    def test_blast_exits_1(self):
        result = run(["--file", str(ROOT / "examples" / "post-blast.json")])
        self.assertEqual(result.returncode, 1)
        self.assertIn("a ten-network blast", result.stdout)
        self.assertNotIn("post:", result.stdout)

    def test_bad_json_hides_input(self):
        bad = run(["--stdin"], stdin='{"post": "' + CELL)
        self.assertNotEqual(bad.returncode, 0)
        self.assertNotIn(CELL, bad.stdout + bad.stderr)
        self.assertIn("invalid JSON", bad.stderr)
        array = run(["--stdin"], stdin='["' + CELL + '"]')
        self.assertNotEqual(array.returncode, 0)
        self.assertNotIn(CELL, array.stdout + array.stderr)
        self.assertIn("JSON must be an object", array.stderr)


if __name__ == "__main__":
    unittest.main()
