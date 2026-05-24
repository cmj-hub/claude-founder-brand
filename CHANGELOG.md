# Changelog

## [0.2.1] — 2026-05-24

Marketplace-submission compliance pass. No functional changes.

### Fixed
- `plugin.json` `author` field now an object `{ "name": "..." }` per Claude Code plugin manifest schema. `claude plugin validate` now passes.

## [0.2.0] — 2026-05-23

Polish pass matching claude-cold-email + claude-psp + claude-evp v0.2.

### Added
- 3-tier config: brand-config.example.json + SOUL.md + AGENTS.md
- skills/founder-brand-onboarding (15-min setup), skills/founder-brand-kickoff (state router)
- scripts/score_post.py — 6-axis scoring (hook, specificity, voice, anti-patterns, format, receipt). Catches AI-detection phrases, engagement bait, thought-leader voice
- README rewrite: cost-replacement positioning, mermaid

### Verified
- Strong founder-voice post → 96/100; AI-pattern post → 40/100 (caught 3 AI phrases + bait closer + TL voice)

## [0.1.0] — 2026-05-23

Initial release.
