# Changelog

## [0.4.0] — 2026-10-04

The skills now run the scorer, know where the operator's files live, and load as a plugin.

### Fixed
- The `founder-brand` skill moved to `skills/founder-brand/`. Plugins only load skills under `skills/`, so the entry point was not loading.
- `score_post.py` missed plural and symbol receipts ("14 SQLs", "30 days", "2% to 11%", "$80k") and counted numbers across line breaks. The good example now scores 100 (was 96).
- `SOUL.md` phrases are cleaned before matching — `"Leverage" (as verb)` and `"The lever is..."` now match post text.
- 12-week engine planned "52 posts" at 1 per pillar per week; it's 48, and now follows `cadence.posts_per_week`.
- `founder-content` required every post to point at the JMC course. Drive-to now comes from the operator's `business_outcomes`.
- Stray code fence in `founder-brand-kickoff`; dangling course links in `founder-content` and `linkedin-craft`.
- `brand-config.example.json` drive-to URLs are placeholders, so a copied config no longer sends the operator's readers to JMC.

### Added
- Blockers in `score_post.py`: AI-detection phrases, engagement bait, the operator's refused phrases, and >3 hashtags exit 1 at any score (AGENTS.md: "banned, always").
- `score_post.py --file` (strips draft frontmatter) and `--min-score`. Listicle-hook and emoji-block checks. Word limit is 200, matching AGENTS.md.
- `scripts/check_setup.py` — deterministic state for the kickoff router: files present, `<placeholder>` lines left, pillar pools, phrases, stories, cadence, drafts this week, next pillar, drift.
- Drafts are saved to `drafts/<date>-<pillar>-<slug>.md` with frontmatter, so the weekly queue counts real posts.
- `linkedin-craft` critique uses the scorer's six axes instead of a separate rubric.
- Onboarding says where the files go, copies the shipped templates, refreshes without overwriting, and verifies with `check_setup.py`. It is now user-invocable.
- `argument-hint` on `founder-brand` and onboarding.
- `tests/test_scoring.py` (calibration, blockers, SOUL parsing, setup state). CI runs the unit tests and fails on any SKILL.md outside `skills/` or a version mismatch between `plugin.json` and `package.json`.

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
