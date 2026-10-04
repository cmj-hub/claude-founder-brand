#!/usr/bin/env python3
"""Script CLI convention: --json, fix lines on exit 1, Next: line on every run."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCORE = ROOT / "scripts" / "score_post.py"
CHECK = ROOT / "scripts" / "check_setup.py"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_scoring import FILLED_SOUL  # noqa: E402


def run(script, *args, stdin=None):
    return subprocess.run([sys.executable, str(script), *args], input=stdin, capture_output=True, text=True)


def fix_lines(stdout):
    return [line for line in stdout.splitlines() if line.startswith("- ")]


class ScorePostCli(unittest.TestCase):
    def test_json_flag_matches_format_json(self):
        good = str(ROOT / "examples" / "proof.good.md")
        a, b = run(SCORE, "--file", good, "--json"), run(SCORE, "--file", good, "--format", "json")
        self.assertEqual(a.returncode, 0)
        self.assertEqual(json.loads(a.stdout)["total"], json.loads(b.stdout)["total"])
        self.assertEqual(json.loads(a.stdout)["next"], "/founder-brand:founder-brand status")

    def test_pass_ends_with_next(self):
        result = run(SCORE, "--file", str(ROOT / "examples" / "proof.good.md"))
        self.assertEqual(result.stdout.strip().splitlines()[-1], "Next: /founder-brand:founder-brand status")
        self.assertEqual(fix_lines(result.stdout), [])

    def test_blocked_post_says_what_to_change(self):
        result = run(SCORE, "--file", str(ROOT / "examples" / "proof.bad.md"))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.strip().splitlines()[-1], "Next: fix the lines above and run this again.")
        lines = fix_lines(result.stdout)
        self.assertTrue(any(line.startswith("- blocker: AI-detection phrase") for line in lines))
        for line in lines:
            self.assertIn(" → ", line)
        data = json.loads(run(SCORE, "--file", str(ROOT / "examples" / "proof.bad.md"), "--json").stdout)
        self.assertEqual(len(data["reasons"]), len(data["fixes"]))
        self.assertTrue(data["blockers"])

    def test_blast_fix(self):
        blast = (ROOT / "examples" / "post-blast.json").read_text(encoding="utf-8")
        result = run(SCORE, "--stdin", stdin=blast)
        self.assertEqual(result.returncode, 1)
        self.assertIn("→ pick one and write for it", result.stdout)

    def test_help_shows_example(self):
        self.assertIn("examples/proof.good.md", run(SCORE, "--help").stdout)


class CheckSetupCli(unittest.TestCase):
    def test_incomplete_setup_lists_fixes(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(CHECK, "--dir", tmp)
            data = json.loads(run(CHECK, "--dir", tmp, "--json").stdout)
        self.assertEqual(result.returncode, 1)
        self.assertIn("- brand-config.json is missing → run /founder-brand:founder-brand setup", result.stdout)
        self.assertEqual(result.stdout.strip().splitlines()[-1], "Next: fix the lines above and run this again.")
        self.assertEqual(data["missing"], ["Run onboarding — brand-config.json is missing."])
        self.assertEqual(len(data["reasons"]), len(data["fixes"]))

    def test_ready_names_next_post(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "SOUL.md").write_text(FILLED_SOUL, encoding="utf-8")
            (root / "brand-config.json").write_text(
                (ROOT / "brand-config.example.json").read_text(encoding="utf-8"), encoding="utf-8")
            result = run(CHECK, "--dir", tmp, "--today", "2026-10-07")
            data = json.loads(run(CHECK, "--dir", tmp, "--today", "2026-10-07", "--json").stdout)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertTrue(result.stdout.strip().splitlines()[-1].startswith(
            "Next: /founder-brand:founder-brand content pillar"))
        self.assertEqual(data["next"], "/founder-brand:founder-brand content pillar")
        self.assertEqual(data["reasons"], [])


if __name__ == "__main__":
    unittest.main()
