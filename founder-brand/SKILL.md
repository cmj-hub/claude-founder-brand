---
name: founder-brand
description: >
  Founder-led social system for B2B founders building a compounding personal
  brand. Generates LinkedIn-native posts following the Pillar / Proof /
  Process / Person framework (4 content pillars rotated weekly), plans a 12-
  week content engine, critiques drafts for the "founder voice" anti-pattern
  list (no thought-leader voice, no LinkedIn-influencer cadence, no
  AI-detection signals), and structures content around the 5 hook archetypes
  that actually pull demand on the JMC framework. Based on the Founder-Brand
  Compounding course. Triggers on: "founder content", "LinkedIn post",
  "founder-led social", "personal brand", "linkedin strategy", "content
  pillar", "founder voice", "content engine", "B2B social".
allowed-tools: Read Write Grep
license: MIT

---

# Founder Brand — Founder-Led Social System

Compounding content engine for B2B founders. Produces LinkedIn-native
posts on a 4-pillar rotation, plans a 12-week content engine, and
critiques drafts against the JMC "founder voice" rubric (no
thought-leader voice, no LinkedIn-influencer cadence, no AI-detection
signals).

## Quick reference

| Slash | What it does |
|---|---|
| `/founder-brand` | Interactive — detect intent, route to a sub-skill |
| `/founder-brand content <pillar>` | Generate a LinkedIn post on a specific pillar |
| `/founder-brand engine` | Plan a 12-week content engine across all 4 pillars |
| `/founder-brand critique <post>` | Critique a draft for voice + anti-patterns |
| `/founder-brand hooks <topic>` | Generate 5 hook variants across the 5 hook archetypes |

## The framework — 4 content pillars

Rotate weekly. Don't do all four in one week (overwhelming) or skip a
pillar for 4+ weeks (drift). The 4 pillars:

| # | Pillar | Job | Example |
|---|---|---|---|
| 1 | **Pillar** | Big claim / point of view / contrarian take | "We don't run cold email programs that don't anchor on a PSP. Here's why." |
| 2 | **Proof** | Case study / specific metric / receipt | "Series-B SaaS — 14 SQLs in 30 days from one PSP rewrite. Here's the breakdown." |
| 3 | **Process** | How you actually do the work / SOP / framework | "Our 7-step Pain Signal Profile worksheet, with the 3 places teams get stuck." |
| 4 | **Person** | The human behind the work — story, stake, reason you care | "I shipped 3 outbound programs that failed before I figured out the PSP layer." |

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
4. **A real receipt every time.** No abstract "here's how to do X" — show the actual receipt.
5. **No closer-line bullshit.** No "What's been your experience?" No "Agree?" No "Thoughts?"
6. **Format for skim.** 1-sentence opener. 1-line body lines. Bullet receipts. White space.

## Voice anti-patterns (banned)

The skill refuses to produce any of these:

- "Thought leadership" voice (capital-T thinking, no specifics)
- LinkedIn-influencer cadence ("Stop. Read this. Slowly.")
- AI-detection signals ("delve into", "navigate the landscape", "in today's fast-paced world")
- Hook-as-listicle ("3 things I learned this week" without specifics)
- "Engagement bait" closers ("What's been your experience?" / "Agree? Disagree?")
- Generic gratitude posts (no specifics, "grateful to everyone who...")
- Multi-emoji blocks
- Hashtag stacks (>3 hashtags)

## Workflow

### Mode: content generation

1. Pick the pillar (1-4) — user choice, or skill suggests based on
   recent post history if shared
2. Pick the hook archetype (1-5) — skill suggests based on the pillar
3. Capture the specifics (the metric / receipt / story)
4. Generate the post:
   - 1-sentence hook (matches the archetype)
   - 2-4 single-line body sentences (specific, scannable)
   - Receipt block (bulleted, concrete numbers)
   - 1-line close (no engagement bait)
5. Self-check against voice rubric + banned patterns
6. Output

### Mode: 12-week engine planning

1. Capture the founder's 4-pillar contents (what's the Pillar / Proof
   / Process / Person material for THIS founder)
2. Plan 12 weeks (52 posts) — 1 per pillar per week, rotation enforced
3. For each week, suggest:
   - Pillar
   - Hook archetype
   - Topic (drawn from the founder's actual material)
   - Connected business outcome (drive to course / lead magnet / call)

### Mode: critique

1. Take the draft
2. Score against voice rubric (0-100)
3. Identify the weakest line + rewrite
4. Flag any anti-pattern hits

## Sub-skills

- [`skills/founder-content`](../skills/founder-content) — generate a single post on a specific pillar
- [`skills/linkedin-craft`](../skills/linkedin-craft) — LinkedIn-specific format, hook generation, critique

## Plugs into

- **[claude-psp](https://github.com/cmj-hub/claude-psp)** — content pillars often map to PSP insights
- **[claude-cold-email](https://github.com/cmj-hub/claude-cold-email)** — Process pillar content makes great PSP / framework / sequence assets
- **JMC Founder-Brand Compounding course** — full methodology

## Course

This skill is the agent-form of the **Founder-Brand Compounding**
course in The Compounding Engine. The course covers:

- 12-week content engine design end-to-end
- Per-pillar production cadences
- Drive-to-business mechanics (post → lead magnet → call)
- Format-by-platform (LinkedIn / X / Threads / podcast / newsletter)
- The "compounding" framework — why post #100 is 10x the lever of post #10

