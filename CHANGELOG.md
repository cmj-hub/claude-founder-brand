# Changelog

## [0.3.0] — 2026-09-08

Public magnet pass. Instrument stays public. First loop is 15 minutes.

### Added
- Definition-first README (GEO paragraph, 15-minute artifact, FAQ H2s, current Pass price).
- Cross-agent installer: `npx skills add cmj-hub/claude-founder-brand --all -g --full-depth` (Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, Antigravity, Goose, and the rest of the skills CLI list). Fallback copies into well-known `*/skills` dirs.
- `package.json` (`jmc-founder-brand`) so `npm install github:cmj-hub/claude-founder-brand` and `npx jmc-founder-brand` work. Not published to npmjs.com.
- `examples/` golden good/bad pair for the first loop.

### Changed
- Removed pricing copy from the public pack; CTAs point at the free hosted tools.
- `plugin.json` description is the definition, homepage is /skills.

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
