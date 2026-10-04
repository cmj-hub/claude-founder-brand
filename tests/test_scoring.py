#!/usr/bin/env python3
"""Scorer calibration and setup-state checks. Standard library only."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_setup  # noqa: E402
import score_post  # noqa: E402

GOOD = (ROOT / "examples" / "proof.good.md").read_text(encoding="utf-8")
BAD = (ROOT / "examples" / "proof.bad.md").read_text(encoding="utf-8")


def axis(result, name):
    return next(a for a in result.axes if a.name == name)


class Calibration(unittest.TestCase):
    def test_examples_hold_their_scores(self):
        self.assertEqual(score_post.score_post(GOOD).total, 100)
        self.assertEqual(score_post.score_post(BAD).total, 37)

    def test_receipts_count_plurals_and_symbols(self):
        found = score_post.NUMBER_RE.findall("14 SQLs in 30 days. 2% to 11%. $80k ACV. 3 meetings.")
        self.assertEqual(len(found), 6)

    def test_numbers_do_not_cross_lines(self):
        self.assertEqual(score_post.NUMBER_RE.findall("Tier 3\n\nReply rate"), [])

    def test_listicle_hook_is_flagged(self):
        result = score_post.score_post("3 things I learned this week about hiring.")
        self.assertTrue(any("Listicle" in n for n in axis(result, "hook").notes))

    def test_emoji_block_is_flagged(self):
        result = score_post.score_post(GOOD + "\n🚀🔥💯")
        self.assertEqual(axis(result, "format-skim").score, 12)

    def test_over_200_words_is_flagged(self):
        result = score_post.score_post(GOOD + " word" * 140)
        self.assertTrue(any("≤200" in n for n in axis(result, "format-skim").notes))


class Blockers(unittest.TestCase):
    def test_engagement_bait_blocks_a_high_score(self):
        result = score_post.score_post(GOOD + "\n\nThoughts?")
        self.assertGreaterEqual(result.total, 85)
        self.assertTrue(result.blockers)
        self.assertTrue(result.verdict.startswith("Blocked"))

    def test_refused_phrase_blocks(self):
        result = score_post.score_post(GOOD + "\nPure synergy.", phrases_refused=["Synergy"])
        self.assertIn("Refused phrase (SOUL.md): 'Synergy'", result.blockers)

    def test_hashtag_stack_blocks(self):
        result = score_post.score_post(GOOD + "\n#a #b #c #d")
        self.assertTrue(any("hashtags" in b for b in result.blockers))

    def test_overlap_is_not_reported_twice(self):
        result = score_post.score_post(BAD, phrases_refused=["Delve into"])
        self.assertEqual(sum("delve" in b.lower() for b in result.blockers), 1)

    def test_cli_exits_1_when_blocked(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "score_post.py"), "--post", GOOD + "\n\nAgree?"],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Blockers", proc.stdout)


class NetworkBlast(unittest.TestCase):
    TEN = ["LinkedIn", "X", "Threads", "Facebook", "Instagram", "TikTok", "YouTube", "Reddit", "Bluesky", "Mastodon"]

    def test_ten_networks_list_blocks(self):
        result = score_post.score_post(GOOD, networks=self.TEN)
        self.assertEqual(result.total, 100)
        self.assertTrue(any(b.startswith("Network blast") for b in result.blockers))

    def test_nine_networks_do_not_block(self):
        self.assertEqual(score_post.score_post(GOOD, networks=self.TEN[:9]).blockers, [])

    def test_network_string_with_ten_parts_blocks(self):
        self.assertIsNotNone(score_post.find_blast("a, b | c / d, e, f, g, h, i, j"))

    def test_blast_wording_blocks(self):
        for network in ("ten-network push", "10 networks", "Network blast"):
            self.assertIsNotNone(score_post.find_blast(network), network)

    def test_one_network_and_no_network_pass(self):
        self.assertIsNone(score_post.find_blast("LinkedIn"))
        self.assertIsNone(score_post.find_blast())

    def test_post_body_is_not_checked(self):
        result = score_post.score_post(GOOD + "\nWe tried 10 networks once.", network="LinkedIn")
        self.assertFalse(any("Network blast" in b for b in result.blockers))

    def test_examples_pass_and_refuse(self):
        script = str(ROOT / "scripts" / "score_post.py")
        for name, code in (("post-one-network.json", 0), ("post-blast.json", 1)):
            proc = subprocess.run(
                [sys.executable, script, "--stdin", "--format", "json"],
                input=(ROOT / "examples" / name).read_text(encoding="utf-8"),
                capture_output=True, text=True,
            )
            self.assertEqual(proc.returncode, code, name)
            self.assertEqual(json.loads(proc.stdout)["total"], 100)

    def test_network_flag_blocks(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "score_post.py"), "--post", GOOD, "--network", ",".join(self.TEN)],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 1)
        self.assertIn("Network blast", proc.stdout)


class SoulParsing(unittest.TestCase):
    def test_template_phrases_are_cleaned(self):
        used, refused = score_post.parse_soul_md(str(ROOT / "SOUL.md"))
        self.assertIn("The lever is", used)
        self.assertIn("Specifically", used)
        self.assertIn("Leverage", refused)
        self.assertFalse(any(p.startswith("<") for p in used + refused))

    def test_file_flag_strips_draft_frontmatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft = Path(tmp) / "d.md"
            draft.write_text("---\ndate: 2026-10-05\npillar: proof\n---\n" + GOOD, encoding="utf-8")
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "score_post.py"), "--file", str(draft), "--format", "json"],
                capture_output=True, text=True,
            )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(json.loads(proc.stdout)["total"], 100)


FILLED_SOUL = """# SOUL.md

## My voice in 3 sentences

I write short. I lead with the number. I don't hedge.

## Phrases I use a lot

- "The lever is..."
- "Specifically:"
- "Here's the receipt:"
- "What moved the number"
- "Most teams blame"

## Phrases I refuse

- "Synergy"

## Stories I lean on

- Series-B SaaS, 14 SQLs in 30 days
- Agency, 2% to 11% reply rate
- DevTools, $80k ACV in 90 days
"""


def draft(folder, name, date, pillar, status="draft"):
    (folder / name).write_text(
        f"---\ndate: {date}\npillar: {pillar}\nstatus: {status}\n---\nbody\n", encoding="utf-8"
    )


class SetupState(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "SOUL.md").write_text(FILLED_SOUL, encoding="utf-8")
        (self.root / "brand-config.json").write_text(
            (ROOT / "brand-config.example.json").read_text(encoding="utf-8"), encoding="utf-8"
        )
        self.drafts = self.root / "drafts"
        self.drafts.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def state(self, today="2026-10-07"):
        return check_setup.build_state(self.root, check_setup.dt.date.fromisoformat(today))

    def test_shared_soul_reads_founder_sections_only(self):
        shared = (
            "# SOUL.md — pricing section\n\n"
            "## My stance on pricing\n\n<unfilled pricing line>\n\n"
            "## How the skill uses this file\n\n<footer>\n\n---\n\n"
            + FILLED_SOUL
        )
        (self.root / "SOUL.md").write_text(shared, encoding="utf-8")
        soul = check_setup.check_soul(self.root / "SOUL.md")
        self.assertEqual(soul["placeholders_left"], 0)
        self.assertEqual(soul["phrases_used"], 5)
        self.assertEqual(soul["stories"], 3)

    def test_template_soul_is_not_filled(self):
        (self.root / "SOUL.md").write_text((ROOT / "SOUL.md").read_text(encoding="utf-8"), encoding="utf-8")
        s = self.state()
        self.assertFalse(s["ready"])
        self.assertFalse(s["checks"]["soul_filled"])
        self.assertFalse(s["checks"]["stories_reservoir"])

    def test_missing_config_routes_to_onboarding(self):
        (self.root / "brand-config.json").unlink()
        s = self.state()
        self.assertEqual(s["missing"], ["Run onboarding — brand-config.json is missing."])

    def test_ready_starts_at_first_pillar(self):
        s = self.state()
        self.assertTrue(s["ready"], s["missing"])
        self.assertEqual(s["next_pillar"], "pillar")

    def test_rotation_advances_and_wraps(self):
        draft(self.drafts, "a.md", "2026-10-05", "pillar")
        self.assertEqual(self.state()["next_pillar"], "proof")
        draft(self.drafts, "b.md", "2026-10-06", "person")
        self.assertEqual(self.state()["next_pillar"], "pillar")

    def test_week_counts_from_monday(self):
        draft(self.drafts, "old.md", "2026-10-04", "pillar")  # Sunday, last week
        for i, p in enumerate(["proof", "process", "person", "pillar"]):
            draft(self.drafts, f"{i}.md", f"2026-10-0{5 + i % 3}", p, "published" if i == 0 else "draft")
        s = self.state()
        self.assertEqual(s["posts_this_week"], 4)
        self.assertEqual(s["published_this_week"], 1)
        self.assertTrue(s["this_week_done"])

    def test_drift_needs_four_weeks_of_history(self):
        draft(self.drafts, "a.md", "2026-10-05", "pillar")
        self.assertEqual(self.state()["drifting_pillars"], [])
        draft(self.drafts, "b.md", "2026-08-01", "proof")
        self.assertEqual(self.state()["drifting_pillars"], ["proof", "process", "person"])

    def test_bad_config_exits_2(self):
        (self.root / "brand-config.json").write_text("{", encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "check_setup.py"), "--dir", str(self.root)],
            capture_output=True, text=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stderr)


if __name__ == "__main__":
    unittest.main()
