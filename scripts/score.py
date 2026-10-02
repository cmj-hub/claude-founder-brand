#!/usr/bin/env python3
"""Score one social post: one post, one network, and one receipt.

Stdlib only. No network call. Does not publish.

  python3 scripts/score.py --file draft.json
  python3 scripts/score.py --stdin
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MAX_INPUT_BYTES = 2_000_000
BLAST_RE = re.compile(
    r"ten[- ]network|10 networks|ten networks|network blast",
    re.IGNORECASE,
)


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_text(path: Path) -> str:
    try:
        if not path.exists():
            fail_input("file not found")
        if not path.is_file():
            fail_input("not a file")
        if path.stat().st_size > MAX_INPUT_BYTES:
            fail_input("file is too large")
        raw = path.read_bytes()
    except SystemExit:
        raise
    except OSError:
        fail_input("cannot read file")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("file is not UTF-8 text")


def load_payload(args: argparse.Namespace) -> object:
    if args.file and args.stdin:
        fail_input("pass --file or --stdin, not both")
    if args.stdin:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            fail_input("input is too large")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            fail_input("input is not UTF-8 text")
    elif args.file:
        text = read_text(Path(args.file))
    else:
        fail_input("pass --file or --stdin")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")


def nonempty_text(value: object) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return ""


def is_blast(data: dict, network: str, post: str) -> bool:
    extra = data.get("networks")
    if isinstance(extra, list) and len(extra) >= 10:
        return True
    parts = [part.strip() for part in re.split(r"[,|/]", network) if part.strip()]
    if len(parts) >= 10:
        return True
    blob = f"{network}\n{post}"
    return BLAST_RE.search(blob) is not None


def main() -> int:
    parser = argparse.ArgumentParser(description="Score one social post")
    parser.add_argument("--file", help="Path to a JSON object")
    parser.add_argument("--stdin", action="store_true", help="Read a JSON object from stdin")
    args = parser.parse_args()
    data = load_payload(args)
    if not isinstance(data, dict):
        fail_input("JSON must be an object")

    post = nonempty_text(data.get("post"))
    network = nonempty_text(data.get("network"))
    receipt = nonempty_text(data.get("receipt"))

    if is_blast(data, network, post):
        print("a ten-network blast")
        return 1

    if not post or not network or not receipt:
        print("draft is incomplete")
        return 1

    print(f"post: {post}")
    print(f"network: {network}")
    print(f"receipt: {receipt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
