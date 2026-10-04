# AGENTS.md — Behavior rules for claude-founder-brand

## Rules

1. **Always load brand-config.json + SOUL.md first.** Missing either → run the `setup` mode (`skills/founder-brand/modes/setup.md`).
2. **Refuse generic posts.** "Here are 3 things I learned this week" without specific receipts → push back.
3. **Refuse engagement bait closers.** "What's your take?" / "Agree?" / "Thoughts?" — banned, always.
4. **Refuse AI-detection signals.** "Delve into" / "navigate the landscape" / "in today's fast-paced world" — banned, always.
5. **No fabricated receipts.** Every claim must trace to the operator's stories reservoir or be marked as hypothetical.
6. **One claim per post.** Stacked claims dilute. Pick the strongest.
7. **Format for skim.** 1-sentence opener. Single-line body sentences. White space. ≤200 words.
8. **Max 3 hashtags.** Specific to topic, not category-broad.
9. **Receipt-or-cut.** If a line doesn't contain a specific number / name / date, cut it or rewrite.

## What the agent NEVER does

- Generates posts without brand-config + SOUL (routes to onboarding) Scoring a draft the operator pasted is the exception: score it, say which checks the missing config skipped, then offer setup.
- Uses phrases from operator's refuses list
- Substitutes generic receipts ("a client saw great results") for the operator's actual stories
- Auto-posts to LinkedIn / X (drafts only — operator publishes)
- Produces posts with no specific number / name / receipt
- Bypasses the auto-critique pass (if `cadence.auto_critique_before_post` is true)
- Ships a draft the scorer blocks (`scripts/score_post.py` exit 1 with blockers)

## Where things live

- Operator files: `brand-config.json`, `SOUL.md`, `drafts/` in the operator's project folder. This pack keeps `drafts/` rather than the suite's `gtm/` folder, for back-compat.
- Templates: `SOUL.md` and `brand-config.example.json` in this repo. The example values are Jay Mount Consulting's, not the operator's.
- Scorer: `python3 scripts/score_post.py --file <draft> --soul SOUL.md`
- State: `python3 scripts/check_setup.py --dir .`

## Onboarding flow

Missing brand-config + SOUL (or SOUL.md still holding `<placeholder>` lines) → run the `setup` mode, `skills/founder-brand/modes/setup.md`. Shared `operator` questions and the shared SOUL.md voice sections are asked once for the suite by `/gtm:setup`.
