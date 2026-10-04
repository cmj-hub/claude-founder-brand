#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PASSED=0; FAILED=0
check() { local n="$1"; shift; if "$@" > /dev/null 2>&1; then echo "  ✓ $n"; PASSED=$((PASSED+1)); else echo "  ✗ $n"; FAILED=$((FAILED+1)); fi; }
refute() { local n="$1"; shift; if "$@" > /dev/null 2>&1; then echo "  ✗ $n"; FAILED=$((FAILED+1)); else echo "  ✓ $n"; PASSED=$((PASSED+1)); fi; }

echo "=== score_post.py ==="
check  "good example ships"                python3 scripts/score_post.py --file examples/proof.good.md
check  "good example ships with SOUL.md"   python3 scripts/score_post.py --file examples/proof.good.md --soul SOUL.md
refute "bad example is rejected"           python3 scripts/score_post.py --file examples/proof.bad.md
refute "engagement bait blocks a 90+ post" python3 scripts/score_post.py --post "$(cat examples/proof.good.md)

Thoughts?"

echo "=== check_setup.py ==="
refute "template repo is not 'ready'"      python3 scripts/check_setup.py --dir .
check  "json output parses"                bash -c 'python3 scripts/check_setup.py --dir . --format json | python3 -c "import json,sys; json.load(sys.stdin)"'

echo ""; echo "Passed: $PASSED, Failed: $FAILED"
[ "$FAILED" -eq 0 ]
