#!/usr/bin/env python3
"""
score_post.py — Deterministic founder-voice post scorer.

Scores a LinkedIn/X-style post 0-100 across 6 axes:
- Hook strength (matches one of the 5 archetypes; specific opener)
- Specificity (numbers, names, dates — not abstract)
- Voice fingerprint hits (uses operator's phrases-I-use list)
- Anti-pattern hits (AI-detection signals, engagement bait, banned phrases)
- Format-for-skim (single-line body sentences, white space, ≤200 words)
- Receipt presence (at least one concrete claim with a number/name)

Banned phrases (AI-detection, engagement bait, the operator's refused list)
and hashtag stacks are blockers: the post exits 1 whatever its score.

USAGE:
    python3 score_post.py --post "..." [--soul SOUL.md]
    python3 score_post.py --file draft.md [--soul SOUL.md] [--format json]
    python3 score_post.py --stdin   # JSON: {"post", "phrases_used", "phrases_refused"}

EXIT: 0 = ship (score >= --min-score, no blockers), 1 = rewrite, 2 = bad input.

NO LLM. NO network. Pure regex + heuristics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional


MAX_INPUT_BYTES = 2_000_000


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_text(path: str) -> str:
    try:
        with open(path, "rb") as handle:
            raw = handle.read(MAX_INPUT_BYTES + 1)
    except IsADirectoryError:
        fail_input(f"not a file: {path}")
    except FileNotFoundError:
        fail_input(f"file not found: {path}")
    except OSError:
        fail_input(f"cannot read file: {path}")
    if len(raw) > MAX_INPUT_BYTES:
        fail_input(f"file is too large: {path}")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input(f"file is not UTF-8 text: {path}")


def parse_json(text: str) -> dict:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")
    if not isinstance(data, dict):
        fail_input("JSON must be an object")
    return data


def read_stdin_text() -> str:
    raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        fail_input("input is too large")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("input is not UTF-8 text")


def _phrases(value: object) -> list:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


# A number with a unit, a currency sign, or a percent. "14 SQLs", "$80k",
# "2% to 11%", "30 days". Units may be plural; whitespace never crosses a line.
NUMBER_RE = re.compile(
    r"(?:\$[ \t]?\d[\d,]*(?:\.\d+)?[ \t]?(?:k|m|mm|b)?\b"
    r"|\b\d[\d,]*(?:\.\d+)?[ \t]*(?:%|\+|×|x\b|k\b|m\b"
    r"|(?:days?|weeks?|months?|quarters?|years?|hours?|hrs?|mins?|minutes?"
    r"|sqls?|mqls?|leads?|meetings?|repl(?:y|ies)|customers?|clients?|accounts?"
    r"|deals?|calls?|demos?|hires?|reps?|users?|signups?|programs?|campaigns?"
    r"|posts?|people|companies|teams?)\b))",
    re.IGNORECASE,
)

# Emoji and pictographs — a block of them reads as influencer cadence.
EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")

# Listicle hook without a receipt: "3 things I learned this week".
LISTICLE_HOOK_RE = re.compile(
    r"^(here are |my )?(\d+|three|five|seven|ten) (things|lessons|ways|tips|mistakes|truths)\b",
    re.IGNORECASE,
)


# AI-detection signals — high-confidence "this was written by an LLM" phrases.
AI_DETECTION_PHRASES = [
    "delve into", "delve deeper", "navigate the landscape",
    "in today's fast-paced world", "in today's digital age",
    "in this article", "without further ado",
    "it is important to note", "it's worth noting",
    "let's dive in", "dive deep", "tapestry", "evolving landscape",
    "ever-evolving", "game-changing", "game changer",
    "ushers in", "paradigm shift", "treasure trove",
    "in the realm of", "at the forefront of",
    "transformative power", "harness the power",
]

# Engagement bait closers — banned.
ENGAGEMENT_BAIT = [
    "what's your take",
    "what's your experience",
    "what's your thought",
    "thoughts?",
    "agree?",
    "agree or disagree",
    "let me know in the comments",
    "what would you add",
    "comment below",
    "drop your thoughts",
    "share if you agree",
    "double tap if",
]

# Thought-leader voice patterns.
TL_VOICE_PHRASES = [
    "hot take:",
    "unpopular opinion:",
    "stop. read this.",
    "the secret to",
    "what nobody tells you",
    "the truth about",
    "the harsh reality",
    "wake up,",
    "stop scrolling",
    "you need to hear this",
    "thread:",
    "grateful to everyone",
    "humbled and honored",
    "i'm humbled",
]

# Hook archetypes — first-line patterns.
HOOK_PATTERNS = {
    "contrarian": [
        r"most (teams|people|founders|companies|operators) (do|think|believe)",
        r"the (real|actual) lever is",
        r"the (real|actual) issue is",
        r"everyone (does|thinks) X[\.\,]? we",
    ],
    "specific_receipt": [
        r"\d+\s*(\+|%|sql|mql|day|week|month|x|×|deal|meeting|reply|customer)",
        r"in \d+ (day|week|month)s?",
        r"hit \d+",
        r"shipped \d+",
    ],
    "confession": [
        r"i (used to|thought|was wrong)",
        r"i (made|shipped) \d+ (failed|broken|bad)",
        r"after (\d+|N) (years?|months?|attempts?)",
    ],
    "pattern_observation": [
        r"(reviewed|looked at|analyzed) \d+",
        r"i've seen (this|the same) pattern",
        r"one pattern keeps showing up",
        r"every (program|campaign|company) that",
    ],
    "question_reframe": [
        r"stop asking",
        r"the better question is",
        r"instead of asking",
        r"ask (this|that|the) instead",
    ],
}


@dataclass
class AxisScore:
    name: str
    score: int
    max_score: int
    notes: List[str] = field(default_factory=list)


@dataclass
class PostScore:
    post: str
    total: int
    max_total: int
    word_count: int
    line_count: int
    hook_archetype: Optional[str]
    verdict: str
    blockers: List[str]
    axes: List[AxisScore]


def detect_hook_archetype(first_line: str) -> Optional[str]:
    fl = first_line.lower()
    for archetype, patterns in HOOK_PATTERNS.items():
        if any(re.search(p, fl) for p in patterns):
            return archetype
    return None


def score_hook(post: str) -> tuple:
    """20 points. First sentence matches a hook archetype."""
    score = 20
    notes = []
    first_line = post.strip().split("\n")[0].strip()
    archetype = detect_hook_archetype(first_line)

    if archetype:
        notes.append(f"Hook archetype: {archetype}")
    else:
        score -= 15
        notes.append("No clear hook archetype — first line doesn't match contrarian / specific-receipt / confession / pattern / question-reframe")

    # Penalize TL-voice in first line
    if any(p in first_line.lower() for p in TL_VOICE_PHRASES):
        score -= 10
        notes.append(f"Thought-leader voice in hook")

    if LISTICLE_HOOK_RE.search(first_line) and not NUMBER_RE.search(first_line[2:]):
        score -= 10
        notes.append("Listicle hook without a receipt — lead with the number that happened")

    # Length check
    if len(first_line.split()) > 25:
        score -= 3
        notes.append(f"Hook is {len(first_line.split())} words — ≤25 ideal")

    return AxisScore("hook", max(0, score), 20, notes), archetype


def score_specificity(post: str) -> AxisScore:
    """20 points. Numbers, named entities, dates."""
    score = 20
    notes = []
    numbers = NUMBER_RE.findall(post)
    if len(numbers) == 0:
        score -= 12
        notes.append("No specific numbers / metrics — receipts need concrete numbers")
    elif len(numbers) < 2:
        score -= 4
        notes.append(f"Only {len(numbers)} number — could use more receipts")

    # Look for named entities (capitalized words mid-sentence)
    named_entities = re.findall(r"(?<=\.\s)[A-Z][a-z]+|(?<=\s)[A-Z][a-z]{3,}", post)
    if len(named_entities) == 0:
        score -= 4
        notes.append("No named entities (companies / people / products) — anonymize but specify")

    return AxisScore("specificity", max(0, score), 20, notes)


def score_voice_fingerprints(post: str, phrases_used: List[str]) -> AxisScore:
    """15 points. Operator's phrases-I-use list shows up."""
    score = 15
    notes = []
    if not phrases_used:
        notes.append("No SOUL.md phrases-I-use list provided — score skipped")
        return AxisScore("voice-fingerprints", score, 15, notes)

    post_lower = post.lower()
    hits = [p for p in phrases_used if p.lower() in post_lower]
    if not hits:
        score -= 10
        notes.append(f"None of your {len(phrases_used)} voice fingerprints appear")
    else:
        notes.append(f"Voice hits: {len(hits)}/{len(phrases_used)}")

    return AxisScore("voice-fingerprints", max(0, score), 15, notes)


def score_anti_patterns(post: str, phrases_refused: List[str]) -> AxisScore:
    """20 points. AI detection + engagement bait + TL voice + operator's refused list."""
    score = 20
    notes = []
    post_lower = post.lower()

    ai_hits = [p for p in AI_DETECTION_PHRASES if p in post_lower]
    if ai_hits:
        score -= min(15, len(ai_hits) * 6)
        notes.append(f"AI-detection phrases: {ai_hits}")

    bait_hits = [b for b in ENGAGEMENT_BAIT if b in post_lower]
    if bait_hits:
        score -= 10
        notes.append(f"Engagement bait closer: {bait_hits}")

    tl_hits = [t for t in TL_VOICE_PHRASES if t in post_lower]
    if tl_hits:
        score -= 6
        notes.append(f"Thought-leader voice: {tl_hits}")

    if phrases_refused:
        ref_hits = [p for p in phrases_refused if p.lower() in post_lower]
        if ref_hits:
            score -= min(10, len(ref_hits) * 4)
            notes.append(f"Operator's refused phrases: {ref_hits}")

    return AxisScore("anti-patterns", max(0, score), 20, notes)


def score_format_skim(post: str) -> AxisScore:
    """15 points. Single-line body sentences, white space, ≤200 words."""
    score = 15
    notes = []
    lines = [l for l in post.split("\n") if l.strip()]
    long_lines = [l for l in lines if len(l) > 250]
    if long_lines:
        score -= 5
        notes.append(f"{len(long_lines)} run-on lines (>250 chars) — break into shorter sentences for skim")

    words = len(post.split())
    if words > 200:
        score -= 5
        notes.append(f"{words} words — LinkedIn-optimal is ≤200")
    elif words < 30:
        score -= 3
        notes.append(f"{words} words — likely too short to land")

    # Hashtag count
    hashtags = re.findall(r"#\w+", post)
    if len(hashtags) > 3:
        score -= 3
        notes.append(f"{len(hashtags)} hashtags — keep to ≤3 specific tags")

    emoji = EMOJI_RE.findall(post)
    if len(emoji) > 2:
        score -= 3
        notes.append(f"{len(emoji)} emoji — multi-emoji blocks read as influencer cadence")

    return AxisScore("format-skim", max(0, score), 15, notes)


def score_receipt(post: str) -> AxisScore:
    """10 points. At least one concrete claim with a number/name/date."""
    score = 10
    notes = []
    # Look for a sentence containing a number AND a noun
    has_receipt = bool(NUMBER_RE.search(post))
    if not has_receipt:
        score -= 8
        notes.append("No concrete receipt — needs at least one number-anchored claim")
    else:
        notes.append("Concrete receipt present")
    return AxisScore("receipt", max(0, score), 10, notes)


def find_blockers(post: str, phrases_refused: List[str]) -> List[str]:
    """Hits that fail the post at any score. AGENTS.md: banned, always."""
    post_lower = post.lower()
    blockers = []
    for p in AI_DETECTION_PHRASES:
        if p in post_lower:
            blockers.append(f"AI-detection phrase: {p!r}")
    for b in ENGAGEMENT_BAIT:
        if b in post_lower:
            blockers.append(f"Engagement bait: {b!r}")
    already = AI_DETECTION_PHRASES + ENGAGEMENT_BAIT
    for p in phrases_refused:
        if p.lower() in post_lower and p.lower() not in already:
            blockers.append(f"Refused phrase (SOUL.md): {p!r}")
    hashtags = re.findall(r"#\w+", post)
    if len(hashtags) > 3:
        blockers.append(f"{len(hashtags)} hashtags (max 3)")
    return blockers


def score_post(post: str, phrases_used: Optional[List[str]] = None, phrases_refused: Optional[List[str]] = None, min_score: int = 70) -> PostScore:
    phrases_used = phrases_used or []
    phrases_refused = phrases_refused or []

    hook_axis, archetype = score_hook(post)
    axes = [
        hook_axis,
        score_specificity(post),
        score_voice_fingerprints(post, phrases_used),
        score_anti_patterns(post, phrases_refused),
        score_format_skim(post),
        score_receipt(post),
    ]
    total = sum(a.score for a in axes)
    max_total = sum(a.max_score for a in axes)
    blockers = find_blockers(post, phrases_refused)
    if blockers:
        verdict = "Blocked — remove the banned lines, then re-score"
    elif total >= max(85, min_score):
        verdict = "Strong post — ship"
    elif total >= min_score:
        verdict = "Ship after single rewrite (weakest line)"
    elif total >= 50:
        verdict = "Iterate — multiple flags"
    else:
        verdict = "Rewrite — too many issues"

    return PostScore(
        post=post,
        total=total,
        max_total=max_total,
        word_count=len(post.split()),
        line_count=len([l for l in post.split("\n") if l.strip()]),
        hook_archetype=archetype,
        verdict=verdict,
        blockers=blockers,
        axes=axes,
    )


def format_text(s: PostScore) -> str:
    lines = [
        f"# Post Score",
        f"",
        f"Words: {s.word_count}    Lines: {s.line_count}    Hook: {s.hook_archetype or '—'}",
        f"Score: {s.total}/{s.max_total} — {s.verdict}",
    ]
    if s.blockers:
        lines += ["", "## Blockers"]
        lines += [f"  ✗ {b}" for b in s.blockers]
    lines += ["", "## Per-axis"]
    for a in s.axes:
        lines.append(f"  {a.name.ljust(20)} {a.score}/{a.max_score}")
        for n in a.notes:
            lines.append(f"    • {n}")
    return "\n".join(lines)


def clean_phrase(item: str) -> str:
    """'"Leverage" (as verb)' -> 'Leverage'; '"The lever is..."' -> 'The lever is'."""
    item = re.sub(r"\s*\([^)]*\)\s*$", "", item.strip())
    item = item.strip().strip("\"'“”‘’").strip()
    item = re.sub(r"(\.\.\.|…|:)$", "", item).strip()
    return item


def parse_soul_md(path: str) -> tuple:
    """Extract phrases-I-use / phrases-I-refuse from SOUL.md."""
    text = read_text(path)

    used = []
    refused = []
    sections = re.split(r"^##\s+", text, flags=re.MULTILINE)
    for sec in sections:
        head, _, body = sec.partition("\n")
        head_l = head.strip().lower()
        items = re.findall(r"^[-*]\s+(.+?)\s*$", body, flags=re.MULTILINE)
        items = [clean_phrase(i) for i in items if not i.strip().startswith("<")]
        items = [i for i in items if i]
        if "phrases i use" in head_l or "phrases that show up" in head_l:
            used.extend(items)
        elif "phrases i refuse" in head_l or "won't write" in head_l or "phrases i would never" in head_l:
            refused.extend(items)
    # A shared SOUL.md can repeat a heading per pack; keep each phrase once.
    return list(dict.fromkeys(used)), list(dict.fromkeys(refused))


def strip_frontmatter(text: str) -> str:
    """Drafts saved by founder-content carry YAML frontmatter; score the body only."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--post", default="", help="Post text")
    source.add_argument("--file", default=None, help="Path to a post file (a draft with --- frontmatter is fine)")
    source.add_argument("--stdin", action="store_true", help="Read a JSON object from stdin")
    parser.add_argument("--soul", default=None, help="Path to SOUL.md (extracts phrases lists)")
    parser.add_argument("--min-score", type=int, default=70, help="Exit 0 at or above this score (default 70)")
    parser.add_argument("--format", default="text", choices=["text", "json"])
    args = parser.parse_args()

    used: List[str] = []
    refused: List[str] = []
    if args.soul:
        used, refused = parse_soul_md(args.soul)

    if args.stdin:
        data = parse_json(read_stdin_text())
        post = data.get("post", "")
        if not isinstance(post, str):
            post = ""
        used = _phrases(data.get("phrases_used", used))
        refused = _phrases(data.get("phrases_refused", refused))
    elif args.file:
        post = strip_frontmatter(read_text(args.file))
    else:
        post = args.post

    if not post:
        print("--post, --file, or --stdin required.", file=sys.stderr)
        return 2

    result = score_post(post, used, refused, args.min_score)
    if args.format == "json":
        print(json.dumps(asdict(result), indent=2))
    else:
        print(format_text(result))
    return 0 if result.total >= args.min_score and not result.blockers else 1


if __name__ == "__main__":
    sys.exit(main())
