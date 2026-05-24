#!/usr/bin/env bash
# install.sh — Install claude-founder-brand skill ecosystem
# Usage: curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-founder-brand/main/install.sh | bash

set -euo pipefail

REPO_URL="https://github.com/cmj-hub/claude-founder-brand"
SKILLS_DIR="${HOME}/.claude/skills"

if ! command -v git >/dev/null 2>&1; then
    echo "ERROR: git is required but not installed." >&2
    exit 1
fi

mkdir -p "$SKILLS_DIR"
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

echo "Installing claude-founder-brand..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR" >/dev/null 2>&1

echo "  + founder-brand (orchestrator)"
rm -rf "$SKILLS_DIR/founder-brand"
cp -r "$TEMP_DIR/founder-brand" "$SKILLS_DIR/"

for skill_dir in "$TEMP_DIR/skills"/*; do
    if [[ -d "$skill_dir" ]]; then
        skill_name=$(basename "$skill_dir")
        rm -rf "${SKILLS_DIR:?}/$skill_name"
        cp -r "$skill_dir" "$SKILLS_DIR/"
        echo "  + $skill_name"
    fi
done

echo ""
echo "Done. Restart Claude Code to pick up the new skill."
echo ""
echo "Try it:"
echo "  > Write a Proof pillar post — <your specific receipt>"
echo ""
echo "Course:  https://jaymountconsulting.com/learn/courses/founder-brand-compounding"
echo "Source:  $REPO_URL"
