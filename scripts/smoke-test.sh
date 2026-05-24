#!/usr/bin/env bash
set -euo pipefail
PASSED=0; FAILED=0
check() { local n="$1"; shift; if "$@"; then echo "  ✓ $n"; PASSED=$((PASSED+1)); else echo "  ✗ $n"; FAILED=$((FAILED+1)); fi; }

echo "=== score_post.py ==="
check "strong founder-voice post" \
  python3 scripts/score_post.py \
    --post "Most outbound programs blame the SDRs. The real issue is upstream.

Series-B SaaS, 30 days, 14 SQLs.
The lever wasn't the sequence — it was a PSP rewrite.

Specifically:
- Killed 'VP Marketing at Series-B SaaS' as a target
- Anchored on 'just posted Demand Gen Lead role'
- Rewrote the EVP to Tier 3

Reply rate went 2% to 11%.

Try anchoring outbound on what they just did, not who they are."

# AI-pattern post should fail
echo "  (testing inverse — AI-pattern post should exit non-zero)"
if python3 scripts/score_post.py --post "In today's fast-paced world, let me delve into the truth about cold email. Stop. Read this. You won't believe what I learned. What's your take?" > /dev/null 2>&1; then
  echo "  ✗ AI-pattern post should have failed but passed"
  FAILED=$((FAILED+1))
else
  echo "  ✓ AI-pattern post correctly rejected"
  PASSED=$((PASSED+1))
fi

echo ""; echo "Passed: $PASSED, Failed: $FAILED"
[ "$FAILED" -eq 0 ]
