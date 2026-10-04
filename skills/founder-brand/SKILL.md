---
name: founder-brand
description: >
  Founder-led social system for B2B founders building a compounding personal
  brand. Generates LinkedIn-native posts on the Pillar / Proof / Process /
  Person rotation from real receipts, plans a 12-week content engine, scores
  drafts with a deterministic scorer (no thought-leader voice, no engagement
  bait, no AI-detection filler), and writes hooks across 5 archetypes.
  Drafts only — never posts. Use when the founder asks for founder content,
  a LinkedIn post, founder-led social, personal brand or LinkedIn strategy,
  content pillars, founder voice, a content engine, B2B social, or "score my
  post". Not for cold outreach (use cold-email), post-opt-in email
  sequences (use email-sequence), or landing-page copy (use landing-page).
argument-hint: "[content <pillar> | engine | critique <post> | hooks <topic> | status | onboarding]"
allowed-tools: Read Write Grep Glob Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_setup.py:*) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py:*)
license: MIT
models: ""

---

# Founder Brand — Founder-Led Social System

Compounding content engine for B2B founders. Produces LinkedIn-native
posts on a 4-pillar rotation, plans a 12-week content engine, and
critiques drafts against the founder-voice rubric (no thought-leader
voice, no LinkedIn-influencer cadence, no AI-detection signals).

## Before anything — load the operator

Every mode starts here. No exceptions.

1. Read `brand-config.json` and `SOUL.md` from the operator's project
   folder (the current working directory). Both are shared by every
   pack in the suite; this pack reads `operator`, `audience`, `pillars`,
   `cadence`, `business_outcomes`, and its own `SOUL.md` sections.
2. Either missing, or `SOUL.md` still holds `<placeholder>` lines →
   load `founder-brand-onboarding` and stop. A post without SOUL.md is
   generic by construction.
3. For state (what's filled, which pillar is next, this week's count), run:

   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_setup.py --dir .
   ```

   Exit 0 = ready. Exit 1 = setup incomplete; the `Next:` line says what.

## Quick reference

`$ARGUMENTS` picks the mode. Empty → load `founder-brand-kickoff`.

| Argument | Mode | Loads |
|---|---|---|
| *(none)* | Detect state, pick the next-best step | `founder-brand-kickoff` |
| `status` | Program status — config, SOUL, this week's queue | `founder-brand-kickoff` |
| `onboarding` / `onboarding refresh` | First-run setup or quarterly voice refresh | `founder-brand-onboarding` |
| `content <pillar>` | One post on a pillar, saved to `drafts/` | `founder-content` |
| `engine` | 12-week content plan across all 4 pillars | this file |
| `critique <post or path>` | Score + weakest-line rewrite | `linkedin-craft` (Mode C) |
| `hooks <topic>` | 5 hook variants, one per archetype | `linkedin-craft` (Mode A) |

## The framework — 4 content pillars

Rotate weekly. Don't do all four in one week (overwhelming) or skip a
pillar for 4+ weeks (drift). The 4 pillars:

| # | Pillar | Job | Example |
|---|---|---|---|
| 1 | **Pillar** | Big claim / point of view / contrarian take | "We don't run cold email programs that don't anchor on a PSP. Here's why." |
| 2 | **Proof** | Case study / specific metric / receipt | "Series-B SaaS — 14 SQLs in 30 days from one PSP rewrite. Here's the breakdown." |
| 3 | **Process** | How you actually do the work / SOP / framework | "Our 7-step Pain Signal Profile worksheet, with the 3 places teams get stuck." |
| 4 | **Person** | The human behind the work — story, stake, reason you care | "I shipped 3 outbound programs that failed before I figured out the PSP layer." |

The examples are Jay Mount Consulting's. The operator's pillars come
from `brand-config.json` → `pillars.<pillar>.topic_pool`.

## The 5 hook archetypes

The first line of any post does one of these jobs. If it doesn't,
the post won't pull demand.

| # | Hook | Pattern | Example |
|---|---|---|---|
| 1 | **Contrarian** | "Most teams do X. We do Y instead — here's why." | "Most outbound programs blame the SDRs. The actual issue is upstream." |
| 2 | **Specific receipt** | "<Specific outcome>: <metric>. <The unexpected lever>." | "14 SQLs in 30 days. The lever wasn't the sequence — it was the PSP." |
| 3 | **Confession** | "I used to think X. I was wrong. Here's what I learned." | "I used to think cold email volume was the lever. After 3 failed programs, I figured out it wasn't." |
| 4 | **Pattern observation** | "I've reviewed N <thing>. Here's the one pattern that keeps showing up." | "Reviewed 60 cold email programs this year. One pattern shows up in every program that's hitting." |
| 5 | **Question reframe** | "Stop asking <usual question>. Ask <better question> instead." | "Stop asking 'what's our ICP?' Ask 'what just happened publicly that proves we should reach out?'" |

## The voice — what makes it sound like a founder

1. **Specificity over generality.** "14 SQLs in 30 days" beats "great results."
2. **One claim per post.** Stacked claims dilute.
3. **First-person, present-tense, conversational.** "We do X" not "One should consider X."
4. **A real receipt every time.** From the operator's stories reservoir in `SOUL.md`. Never invented.
5. **No engagement-bait closer.** No "What's been your experience?" No "Agree?" No "Thoughts?"
6. **Format for skim.** 1-sentence opener. 1-line body lines. Bullet receipts. White space. ≤200 words.

## Voice anti-patterns (banned)

The skill refuses to produce any of these:

- "Thought leadership" voice (capital-T thinking, no specifics)
- LinkedIn-influencer cadence ("Stop. Read this. Slowly.")
- AI-detection signals ("delve into", "navigate the landscape", "in today's fast-paced world")
- Hook-as-listicle ("3 things I learned this week" without specifics)
- Engagement-bait closers ("What's been your experience?" / "Agree? Disagree?")
- Generic gratitude posts (no specifics, "grateful to everyone who...")
- Multi-emoji blocks
- Hashtag stacks (>3 hashtags)
- Network blasts (one post aimed at 10+ networks; one post, one network)
- Anything on the operator's `SOUL.md` → "Phrases I refuse" list

## The scorer

`scripts/score_post.py` is the single rubric for every mode. Deterministic.
No LLM, no network.

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py --file drafts/<draft>.md --soul SOUL.md
```

- 0-100 across 6 axes: hook 20, specificity 20, voice fingerprints 15,
  anti-patterns 20, format 15, receipt 10.
- Banned phrases, engagement bait, refused phrases, and >3 hashtags are
  **blockers** — exit 1 at any score.
- Pass `--network LinkedIn` (or `network`/`networks` in `--stdin` JSON)
  when the operator names a target. 10+ networks, or "ten-network" /
  "network blast", is a blocker. Optional; omitted means not checked.
- Exit 0 = ship (≥70, no blockers). Exit 1 = rewrite. Exit 2 = bad input.

Calibration pair: [a good Proof post](../../examples/proof.good.md)
scores 100; [an AI-pattern post](../../examples/proof.bad.md) scores 37
and is blocked.

If `cadence.auto_critique_before_post` is true (the default), every
draft runs through the scorer before it is shown. Never skip it.

## Workflow

### Mode: content generation

Load `founder-content`. It locks the pillar, the hook, and the receipt,
drafts the post, scores it, and saves it to `drafts/`.

### Mode: 12-week engine planning

1. Read the pillar topic pools from `brand-config.json` and the stories
   reservoir from `SOUL.md`.
2. Plan 12 weeks at `cadence.posts_per_week` (default 4 → 48 posts), in
   `cadence.rotation_order`. No pillar goes 4+ weeks without a slot.
3. For each slot, give:
   - Pillar
   - Hook archetype
   - Topic (from the operator's pool — never invented)
   - Receipt it rests on (story from `SOUL.md`, or "needs a receipt")
   - Drive-to (`business_outcomes.drive_to` / `lead_magnet` / `call_url`)
4. Output as one table per month. Save to `drafts/engine-<YYYY-MM-DD>.md`
   if the operator asks to keep it.
5. Flag every slot that has no receipt yet. Those are the operator's
   homework, not the agent's to fill.

### Mode: critique

Load `linkedin-craft`, Mode C. Run the scorer first; the score is the
scorer's, not a guess.

## Never

- Post to LinkedIn / X. Drafts only — the operator publishes.
- Invent a receipt. No story in the reservoir → ask, or mark the line
  `[hypothetical]`.
- Skip the scorer when `auto_critique_before_post` is true.

## Sub-skills

- [`founder-brand-kickoff`](../founder-brand-kickoff/SKILL.md) — state router + weekly queue + status
- [`founder-brand-onboarding`](../founder-brand-onboarding/SKILL.md) — writes `brand-config.json` + `SOUL.md`
- [`founder-content`](../founder-content/SKILL.md) — one post on a specific pillar
- [`linkedin-craft`](../linkedin-craft/SKILL.md) — hooks, skim format, critique

## Works with the suite

This is step 10 of the GTM operator suite (`/plugin marketplace add cmj-hub/gtm-operator-skills`). It runs standalone.

- **Reads:** `operator`, `audience`, `pillars`, `cadence`, `business_outcomes` from `brand-config.json`; `psp.vocabulary` (the buyer's words for the audience) and `evp.primary` (a Pillar post's claim) if present.
- **Writes:** `audience`, `pillars`, `cadence`, `business_outcomes`, and this pack's `SOUL.md` sections. Merge at the field level; never overwrite another pack's keys.
- **Before this:** psp (`/psp:psp`) and evp (`/evp:evp`), optional, when the posts should use the buyer's words and the outreach line.
- **After this:** nothing. The operator publishes the drafts.

If a companion pack is not installed, name it and its install line (`/plugin install <name>@gtm-operator-skills`); do not do its job inline.

## References

- [SOUL.md template](../../SOUL.md) — the founder-brand voice sections onboarding fills in

## Course

This skill is the agent form of the
[Founder-Brand Compounding](https://jaymountconsulting.com/learn/courses/founder-brand-compounding)
course. The course covers:

- 12-week content engine design end-to-end
- Per-pillar production cadences
- Drive-to-business mechanics (post → lead magnet → call)
- Format-by-platform (LinkedIn / X / Threads / podcast / newsletter)
- The "compounding" framework — why post #100 is 10x the lever of post #10
