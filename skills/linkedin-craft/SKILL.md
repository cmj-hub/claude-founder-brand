---
name: linkedin-craft
description: LinkedIn-native post construction — format for skim (1-sentence opener, single-line body, bulleted receipt, no engagement bait), generate 5 hook variants across the 5 hook archetypes (contrarian, specific receipt, confession, pattern observation, question reframe), and critique a draft for voice + anti-pattern compliance. Use when the main founder-brand skill needs hooks, skim formatting, or a draft critique.
user-invocable: false
allowed-tools: Read Write Grep Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py:*)
license: MIT
models: ""

---

# LinkedIn Craft — sub-skill

LinkedIn-specific post construction and critique.

## Activation

Loaded by `founder-brand` on:
- "LinkedIn post about..."
- "5 hook variants for..."
- "Critique this LinkedIn draft"
- "Better hook for this topic"

## Modes

### Mode A — generate 5 hook variants

Given a topic, produce one hook per archetype. Fill the numbers from the
operator's stories in `SOUL.md`; where none fits, leave `<metric>` for
the operator rather than inventing one.

```markdown
# Hook variants — <topic>

| # | Archetype | Hook |
|---|---|---|
| 1 | Contrarian | "Most teams do X. The lever is actually Y." |
| 2 | Specific receipt | "<Metric>: <number> in <timeframe>. The lever wasn't <obvious thing>." |
| 3 | Confession | "I used to think X. After <N> failed attempts I figured out it was Y." |
| 4 | Pattern observation | "I've reviewed <N> <thing> this year. One pattern keeps showing up." |
| 5 | Question reframe | "Stop asking <usual Q>. Ask <better Q> instead." |

## Recommended primary
<#N> — <one-sentence rationale on why this archetype fits the topic best>
```

### Mode B — format for skim

Take a finished post and reformat for LinkedIn-native skim:

```markdown
[1-sentence hook]

[single-line body sentence]

[single-line body sentence]

[single-line body sentence]

[Receipt block:]
- Bullet 1
- Bullet 2
- Bullet 3

[1-line close — direct, no engagement bait]

#hashtag1 #hashtag2
```

Max 200 words. Max 3 hashtags. No emoji blocks. Keep the operator's
words — reformatting doesn't rewrite.

### Mode C — critique a draft

Score with the scorer first. Its numbers are the score — don't
re-estimate them. Save pasted text to a scratch file, or pass a draft
path straight through:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/score_post.py --file <draft> --soul SOUL.md --format json
```

Drop `--soul` if the operator has no `SOUL.md` yet, and say the voice
axis was skipped. If Bash is unavailable, estimate each axis by hand
and label the score "estimated".

```markdown
# Draft critique

**Score:** <total>/100 — <verdict>

| Axis | Score | Issue |
|---|---|---|
| Hook | <0-20>/20 | <one sentence> |
| Specificity | <0-20>/20 | <one sentence> |
| Voice fingerprints | <0-15>/15 | <one sentence> |
| Anti-patterns | <0-20>/20 | <list any hits> |
| Format (skim) | <0-15>/15 | <one sentence> |
| Receipt | <0-10>/10 | <one sentence> |

## Blockers
<each scorer blocker — these fail the post at any score; "None" if empty>

## Single weakest line
Original: "<line>"
Rewrite: "<better>"
Rationale: <one sentence>

## Anti-pattern hits
- <hit 1>
- <hit 2>

## Verdict
<ship / ship-after-rewrite / start-over>
```

The scorer can't judge whether a receipt is true or the post makes one
claim. Read for both and add them to the issues if they fail.

### Mode D — better hook for topic

User says: "I want to write about <topic>. Give me a better hook."
Generate 3 strong hook candidates across the 5 archetypes, recommend
the strongest.

## References

- [`../founder-brand/SKILL.md`](../founder-brand/SKILL.md) — the full framework + voice rubric
- [Founder-Brand Compounding](https://jaymountconsulting.com/learn/courses/founder-brand-compounding) — the course
