#!/usr/bin/env python3
"""
check_setup.py — Deterministic state check for the founder-brand pack.

Reads the operator's brand-config.json, SOUL.md, and drafts/ folder and
reports what is missing, which pillar is next in the rotation, and the
next-best step. The founder-brand status mode runs this instead of
guessing state.

USAGE:
    python3 check_setup.py [--dir .] [--json] [--today YYYY-MM-DD]

OUTPUT: text by default. When setup is incomplete every gap prints as
"- <what is wrong> → <what to change>", then "Next: fix the lines above and
run this again." When ready, the last line names the next post to draft.
--json (alias of --format json) adds "reasons", "fixes" (parallel lists)
and "next"; "missing" and "next_step" are unchanged.

EXIT: 0 = ready to draft, 1 = setup incomplete, 2 = bad input.

NO LLM. NO network. Standard library only.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from score_post import clean_phrase, fail_input, read_text  # noqa: E402

PILLARS = ["pillar", "proof", "process", "person"]
SETUP = "/founder-brand:founder-brand setup"
RETRY = "fix the lines above and run this again."
MIN_TOPICS = 3
MIN_PHRASES = 5
MIN_STORIES = 3
PLACEHOLDER_RE = re.compile(r"^\s*(?:[-*]\s+)?<", re.MULTILINE)
# SOUL.md is shared by every pack in the suite. Founder-brand reads only these
# sections (by heading substring) and ignores the rest, including other
# packs' placeholders and every "How the ... uses this" footer.
FOUNDER_SECTIONS = (
    "my voice",
    "phrases i use",
    "phrases i refuse",
    "posting voice",
    "stories",
    "topics i will not write",
    "what 'good' looks like",
)


def soul_sections(text: str) -> dict:
    """Map lowercased `## heading` -> section body. Repeated headings join."""
    out = {}
    for sec in re.split(r"^##\s+", text, flags=re.MULTILINE)[1:]:
        head, _, body = sec.partition("\n")
        head = head.strip().lower()
        if head.startswith("how the"):
            continue
        # A `---` rule or a new `# ` title ends the section's own content.
        body = re.split(r"^(?:---\s*$|#\s)", body, flags=re.MULTILINE)[0]
        out[head] = out.get(head, "") + body
    return out


def bullets(body: str) -> list:
    items = re.findall(r"^[-*]\s+(.+?)\s*$", body, flags=re.MULTILINE)
    items = [clean_phrase(i) for i in items if not i.strip().startswith("<")]
    return [i for i in items if i]


def find_section(sections: dict, *keys: str) -> str:
    """Every section whose heading holds a key, joined."""
    return "".join(body for head, body in sections.items() if any(k in head for k in keys))


def check_soul(path: Path) -> dict:
    if not path.is_file():
        return {"present": False}
    sections = soul_sections(read_text(str(path)))
    placeholders = len(PLACEHOLDER_RE.findall(find_section(sections, *FOUNDER_SECTIONS)))
    return {
        "present": True,
        "placeholders_left": placeholders,
        "phrases_used": len(bullets(find_section(sections, "phrases i use"))),
        "phrases_refused": len(bullets(find_section(sections, "phrases i refuse"))),
        "stories": len(bullets(find_section(sections, "stories"))),
    }


def check_config(path: Path) -> dict:
    if not path.is_file():
        return {"present": False}
    try:
        data = json.loads(read_text(str(path)))
    except json.JSONDecodeError:
        fail_input(f"invalid JSON: {path.name}")
    if not isinstance(data, dict):
        fail_input(f"{path.name} must be a JSON object")

    pillars = data.get("pillars") if isinstance(data.get("pillars"), dict) else {}
    topic_counts = {}
    for p in PILLARS:
        pool = pillars.get(p, {}).get("topic_pool", []) if isinstance(pillars.get(p), dict) else []
        topic_counts[p] = len([t for t in pool if isinstance(t, str) and t.strip()]) if isinstance(pool, list) else 0

    cadence = data.get("cadence") if isinstance(data.get("cadence"), dict) else {}
    per_week = cadence.get("posts_per_week", 0)
    per_week = per_week if isinstance(per_week, int) and per_week > 0 else 0
    order = cadence.get("rotation_order", PILLARS)
    if not (isinstance(order, list) and order and all(o in PILLARS for o in order)):
        order = PILLARS

    return {
        "present": True,
        "topic_counts": topic_counts,
        "posts_per_week": per_week,
        "rotation_order": order,
        "auto_critique": cadence.get("auto_critique_before_post", True) is not False,
    }


def read_drafts(folder: Path) -> list:
    """Each draft is drafts/*.md with `date:` and `pillar:` frontmatter."""
    drafts = []
    if not folder.is_dir():
        return drafts
    for path in sorted(folder.glob("*.md")):
        text = read_text(str(path))
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---", 4)
        meta = dict(re.findall(r"^([a-z_]+):\s*(.*?)\s*$", text[4:end], flags=re.MULTILINE))
        try:
            date = dt.date.fromisoformat(meta.get("date", "").strip("\"'"))
        except ValueError:
            continue
        drafts.append({
            "file": path.name,
            "date": date,
            "pillar": meta.get("pillar", "").strip("\"'").lower(),
            "status": meta.get("status", "draft").strip("\"'").lower(),
        })
    return sorted(drafts, key=lambda d: (d["date"], d["file"]))


def build_state(root: Path, today: dt.date) -> dict:
    config = check_config(root / "brand-config.json")
    soul = check_soul(root / "SOUL.md")
    drafts = read_drafts(root / "drafts")

    week_start = today - dt.timedelta(days=today.weekday())
    this_week = [d for d in drafts if week_start <= d["date"] <= today]
    order = config.get("rotation_order", PILLARS)
    last = next((d["pillar"] for d in reversed(drafts) if d["pillar"] in order), None)
    next_pillar = order[(order.index(last) + 1) % len(order)] if last else order[0]

    # A pillar with no post in 4+ weeks is drift. Needs 4 weeks of history first.
    drift = []
    if drafts and (today - drafts[0]["date"]).days > 28:
        for p in order:
            dates = [d["date"] for d in drafts if d["pillar"] == p]
            if not dates or (today - max(dates)).days > 28:
                drift.append(p)

    counts = config.get("topic_counts", {p: 0 for p in PILLARS})
    short = ", ".join(f"{p} {n}" for p, n in counts.items() if n < MIN_TOPICS)
    # (name, ok, legacy message, what is wrong, what to change)
    checks = [
        ("has_brand_config", config["present"],
         "Run onboarding — brand-config.json is missing.",
         "brand-config.json is missing", f"run {SETUP}"),
        ("has_soul", soul["present"],
         "Run onboarding — SOUL.md is missing.",
         "SOUL.md is missing", f"run {SETUP}"),
        ("soul_filled", soul.get("placeholders_left", 1) == 0,
         f"Fill SOUL.md — {soul.get('placeholders_left', 0)} <placeholder> line(s) left.",
         f"SOUL.md has {soul.get('placeholders_left', 0)} <placeholder> line(s) left",
         "replace each with your own words, or run " + SETUP),
        ("pillars_filled", all(n >= MIN_TOPICS for n in counts.values()),
         f"Fill pillar topic pools — need ≥{MIN_TOPICS} per pillar: {config.get('topic_counts', {})}.",
         f"pillar topic pools under {MIN_TOPICS} topics: {short}",
         f"add topics to brand-config.json pillars.<pillar>.topic_pool until each has {MIN_TOPICS}"),
        ("voice_fingerprints", soul.get("phrases_used", 0) >= MIN_PHRASES,
         f"Mine your phrases-I-use list — need ≥{MIN_PHRASES}, have {soul.get('phrases_used', 0)}. Read your last 10 posts/emails.",
         f"SOUL.md lists {soul.get('phrases_used', 0)} phrases you use (need {MIN_PHRASES})",
         "add phrases from your last 10 posts or emails under ## Phrases I use a lot"),
        ("stories_reservoir", soul.get("stories", 0) >= MIN_STORIES,
         f"Capture ≥{MIN_STORIES} stories in SOUL.md — have {soul.get('stories', 0)}. Anonymized but specific.",
         f"SOUL.md lists {soul.get('stories', 0)} stories (need {MIN_STORIES})",
         "add anonymized but specific receipts under ## Stories I lean on"),
        ("cadence_set", config.get("posts_per_week", 0) > 0,
         "Pick a weekly cadence in brand-config.json — default 4 posts/week, 1 per pillar.",
         "no weekly cadence in brand-config.json",
         "set cadence.posts_per_week (default 4, one per pillar)"),
    ]
    flags = {name: bool(ok) for name, ok, *_ in checks}
    failed = [c for c in checks if not c[1]]
    if not (flags["has_brand_config"] and flags["has_soul"]):
        failed = [checks[0] if not flags["has_brand_config"] else checks[1]]
    missing = [c[2] for c in failed]

    per_week = config.get("posts_per_week", 0)
    this_week_done = per_week > 0 and len(this_week) >= per_week
    if missing:
        next_step = missing[0]
        next_line = RETRY
    elif this_week_done:
        next_step = "This week's queue is done. Re-run on Monday for the next rotation."
        next_line = "re-run on Monday for the next rotation."
    else:
        next_step = f"Draft this week's {next_pillar.title()} post from your topic pool."
        next_line = f"/founder-brand:founder-brand content {next_pillar}"

    return {
        "ready": not missing,
        "checks": flags,
        "missing": missing,
        "soul": soul,
        "brand_config": config,
        "week_start": week_start.isoformat(),
        "posts_this_week": len(this_week),
        "published_this_week": len([d for d in this_week if d["status"] == "published"]),
        "posts_per_week": per_week,
        "this_week_done": this_week_done,
        "next_pillar": next_pillar,
        "drifting_pillars": drift,
        "next_step": next_step,
        "reasons": [c[3] for c in failed],
        "fixes": [c[4] for c in failed],
        "next": next_line,
    }


def format_text(s: dict) -> str:
    mark = lambda ok: "✓" if ok else "✗"  # noqa: E731
    c, soul, cfg = s["checks"], s["soul"], s["brand_config"]
    lines = ["# Founder-brand status", ""]
    lines.append(f"Brand config:  {mark(c['has_brand_config'])} brand-config.json")
    if soul.get("present"):
        lines.append(
            f"SOUL:          {mark(c['soul_filled'] and c['voice_fingerprints'] and c['stories_reservoir'])} SOUL.md "
            f"({soul['phrases_used']} phrases, {soul['phrases_refused']} refused, {soul['stories']} stories, "
            f"{soul['placeholders_left']} placeholders left)"
        )
    else:
        lines.append("SOUL:          ✗ SOUL.md missing")
    if cfg.get("present"):
        counts = ", ".join(f"{p} {n}" for p, n in cfg["topic_counts"].items())
        lines.append(f"Pillar pools:  {mark(c['pillars_filled'])} {counts}")
        lines.append(f"Cadence:       {mark(c['cadence_set'])} {cfg['posts_per_week']} posts/week, "
                     + " → ".join(p.title() for p in cfg["rotation_order"]))
    lines.append(f"This week:     {s['posts_this_week']} of {s['posts_per_week']} drafted "
                 f"({s['published_this_week']} published) since {s['week_start']}")
    if s["drifting_pillars"]:
        lines.append(f"Drift:         no post in 4+ weeks — {', '.join(s['drifting_pillars'])}")
    if s["reasons"]:
        lines += ["", "## What to fix"]
        lines += [f"- {what} → {fix}" for what, fix in zip(s["reasons"], s["fixes"])]
        lines += ["", f"Next: {s['next']}"]
    else:
        lines += ["", f"Next: {s['next']} — {s['next_step']}"]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check founder-brand setup and this week's queue. Exit 0 ready, 1 setup incomplete, 2 bad input.",
        epilog="example: python3 scripts/check_setup.py --dir .   # run in your project folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--dir", default=".", help="Folder holding brand-config.json, SOUL.md, drafts/")
    parser.add_argument("--json", dest="format", action="store_const", const="json",
                        help="Print one JSON object (same as --format json)")
    parser.add_argument("--format", dest="format", default="text", choices=["text", "json"],
                        help=argparse.SUPPRESS)
    parser.add_argument("--today", default=None, help="Override today's date (YYYY-MM-DD)")
    args = parser.parse_args()

    root = Path(args.dir)
    if not root.is_dir():
        fail_input(f"not a folder: {args.dir}")
    try:
        today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    except ValueError:
        fail_input("--today must be YYYY-MM-DD")

    state = build_state(root, today)
    if args.format == "json":
        print(json.dumps(state, indent=2))
    else:
        print(format_text(state))
    return 0 if state["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
