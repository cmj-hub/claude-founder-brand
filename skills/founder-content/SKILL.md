---
name: founder-content
description: Generate a single LinkedIn-native post for a founder, on a specific pillar (Pillar / Proof / Process / Person) and using one of the 5 hook archetypes, from a receipt in the operator's SOUL.md. Scores the draft with scripts/score_post.py, saves it to drafts/, and never posts. Use when the main founder-brand skill gets "write a LinkedIn post about...", "draft a founder post", "generate a Proof pillar post".
user-invocable: false
allowed-tools: Read Write Grep Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py:*)
license: MIT
models: ""

---

# Founder Content — sub-skill

Generates a single founder-voice LinkedIn post.

## Activation

Loaded by `founder-brand` on:
- "Write a LinkedIn post about..."
- "Draft a founder post..."
- "Generate a Proof pillar post on..."

## Workflow

### 0. Load the operator

Read `brand-config.json` and `SOUL.md` from the project folder. Either
missing → load `founder-brand-onboarding` instead. From them, hold:

- `SOUL.md` voice settings, phrases-I-use, phrases-I-refuse, stories
- `brand-config.json` audience, pillar topic pools, `business_outcomes`

### 1. Lock the pillar

If user didn't specify, ask:

> Which pillar?
> - **Pillar** — a big claim or POV
> - **Proof** — a case study / specific receipt
> - **Process** — how you actually do the work
> - **Person** — the human story / stake behind it

### 2. Lock the hook archetype

Pick from the 5:
1. Contrarian
2. Specific receipt
3. Confession
4. Pattern observation
5. Question reframe

Suggest based on pillar fit:
- **Pillar** → Contrarian or Question reframe
- **Proof** → Specific receipt or Pattern observation
- **Process** → Pattern observation or Confession
- **Person** → Confession

### 3. Capture the specifics

Required:

- **The actual receipt** — specific numbers, names (or anonymized
  but specific descriptions), timeframes. No abstract "great results."
- **The unexpected lever** — what surprised you / what's the contrarian
  insight buried in the story
- **The drive-to** — which of the operator's `business_outcomes`
  (`drive_to` / `lead_magnet` / `call_url`) this post earns, if any.
  Most posts earn none; that's fine.

The receipt comes from the operator: a story in `SOUL.md` → "Stories I
lean on", or a fact they give you now. Never invent one. A new fact
the operator gives you is worth keeping — offer to add it to the
stories reservoir.

Don't proceed without these. If user gives abstract material, push
back: "What's the actual receipt? Numbers, names, dates — not 'we
helped a client improve outbound.'"

Check the topic against `SOUL.md` → "Topics I will NOT write about".
A hit → say so and stop.

### 4. Generate the post

Structure:

```
Line 1: Hook (matches the archetype)

Line 2-5: Body — single-line sentences, scannable.
Each sentence does ONE job:
- Set up the receipt
- Drop the unexpected lever
- Name the obvious thing the receipt would suggest (then disqualify it)

Receipt block:
- Bullet 1: specific number/metric
- Bullet 2: specific number/metric
- Bullet 3: the lever that mattered

Line N: Close — ONE specific direct line. NO engagement bait.
Optional: 1-line drive to the operator's own offer ("If you're hunting
<pain>, the worksheet for this is at <business_outcomes.lead_magnet>.")

0-3 hashtags. Specific, not category-broad.
```

### 5. Score it

Save the draft first (step 6), then run the scorer with the operator's SOUL:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py --file drafts/<file>.md --soul SOUL.md
```

- Exit 1 or any **Blockers** → rewrite the flagged lines and re-score.
  Up to 3 rounds; then show the operator the draft with the scorer's notes.
- Exit 0 → record the score in the draft's frontmatter.

If Bash is unavailable, run the checklist below by hand and say the
scorer did not run. Either way, check:

| Check | Pass criterion |
|---|---|
| Hook is one sentence | One line, ≤25 words |
| Hook matches the picked archetype | Verbatim pattern match |
| Body sentences are single-line each | No multi-clause run-ons |
| Receipt block has specifics | Numbers, names, dates |
| Close is direct (not engagement bait) | No "What's your take?" type endings |
| ≤3 hashtags | Specific to the topic |
| No banned phrases | Cross-check against banned-patterns list |
| Total ≤200 words | LinkedIn-optimal length |

### 6. Save the draft

Write to `drafts/<YYYY-MM-DD>-<pillar>-<slug>.md` in the project folder:

```
---
date: 2026-10-05
pillar: proof
hook: specific_receipt
topic: "Series-B SaaS hit 14 SQLs in 30 days from a PSP rewrite"
receipt: "SOUL.md → Stories I lean on #1"
score: 96
status: draft
---
<the post, exactly as it should be pasted>
```

`founder-brand-kickoff` counts these files for the weekly queue. When
the operator says they published it, set `status: published`.

### 7. Output + offer the critique pass

Show the post, the score, and the file path. Never post it. Then offer:

> "Want me to identify the single weakest line and rewrite it? (1
> sentence + rationale.)"

## Banned patterns (always refuse)

- "Stop. Read this." opener
- "Hot take:" opener
- "Unpopular opinion:" opener (overused; signals trying-too-hard)
- "Thread:" prefix (LinkedIn isn't Twitter)
- Multi-emoji blocks
- Hashtag stacks (>3)
- "Engagement bait" closers ("Agree?" / "Thoughts?" / "What's your experience?")
- "Delve into" / "Navigate the landscape" / "In today's fast-paced world" (AI-detection)
- Generic gratitude posts
- Posts without a receipt
- Anything on the operator's `SOUL.md` → "Phrases I refuse" list

If the user requests one, push back with the founder-voice alternative.

## References

- [`../founder-brand/SKILL.md`](../founder-brand/SKILL.md) — the framework
- [Founder-Brand Compounding](https://jaymountconsulting.com/learn/courses/founder-brand-compounding) — the course
