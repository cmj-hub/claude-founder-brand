# claude-founder-brand

A Claude Code skill for building a **compounding personal brand** as a
B2B founder. LinkedIn-native posts on the 4-pillar framework (Pillar /
Proof / Process / Person), 12-week content engine planning, and draft
critique against the JMC voice rubric.

No thought-leader voice. No LinkedIn-influencer cadence. No
AI-detection signals. Just the founder voice that actually pulls
demand.

Based on the **[Founder-Brand Compounding](https://jaymountconsulting.com/learn/courses/founder-brand-compounding)**
course from The Compounding Engine.

## The framework

**4 content pillars** rotated weekly:

| # | Pillar | Job |
|---|---|---|
| 1 | **Pillar** | Big claim / point of view / contrarian take |
| 2 | **Proof** | Case study / specific metric / receipt |
| 3 | **Process** | How you actually do the work / SOP |
| 4 | **Person** | The human behind the work — story, stake, why you care |

**5 hook archetypes** — every post's opening line does one of these:

1. Contrarian
2. Specific receipt
3. Confession
4. Pattern observation
5. Question reframe

## Sub-skills

| Sub-skill | Job |
|---|---|
| `founder-content` | Generate a single post on a specific pillar with one of the 5 hooks |
| `linkedin-craft` | LinkedIn-specific format, hook generation, draft critique |

## Install

### Claude Code

```bash
/plugin marketplace add cmj-hub/claude-founder-brand
/plugin install founder-brand
```

### One-line install

```bash
curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-founder-brand/main/install.sh | bash
```

## Usage

```
> Write a Proof pillar post — Series-B SaaS, 14 SQLs in 30 days from a PSP rewrite
```

Claude generates a LinkedIn-native post with:

- 1-sentence hook (matches one of the 5 archetypes)
- Single-line body sentences (scannable)
- Receipt block with specific numbers
- 1-line close (no engagement bait)
- ≤3 hashtags

Or:

```
> Plan my 12-week content engine
```

Claude walks you through capturing your 4-pillar material, then builds
a 12-week (52-post) rotation with hook archetype, topic, and
business-outcome connection per post.

Or:

```
> Critique this LinkedIn draft: [paste]
```

Claude returns a voice score (0-100), the single weakest line + rewrite,
and any anti-pattern flags.

## Voice rubric (what makes it sound like a founder)

1. **Specificity over generality.** "14 SQLs in 30 days" beats "great results."
2. **One claim per post.** Stacked claims dilute.
3. **First-person, present-tense, conversational.**
4. **A real receipt every time.** No abstract "here's how" without showing the actual receipt.
5. **No closer-line bullshit.** No "Thoughts?" / "Agree?" / "What's been your experience?"
6. **Format for skim.** 1-sentence opener. 1-line body lines. Bullets. White space.

## Voice anti-patterns (skill refuses)

- "Thought leadership" voice (capital-T thinking, no specifics)
- LinkedIn-influencer cadence ("Stop. Read this. Slowly.")
- AI-detection signals ("delve into", "navigate the landscape", "in today's fast-paced world")
- Hook-as-listicle without specifics
- Engagement bait closers
- Generic gratitude posts
- Multi-emoji blocks
- Hashtag stacks

## Plugs into

- **[claude-psp](https://github.com/cmj-hub/claude-psp)** — Process pillar content often maps to PSP insights
- **[claude-cold-email](https://github.com/cmj-hub/claude-cold-email)** — Process pillar content makes great PSP / framework / sequence assets
- **[claude-evp](https://github.com/cmj-hub/claude-evp)** — Pillar pillar (the big claim) is often a Tier 2 EVP reformatted

## Course

This skill is the agent-form of the **Founder-Brand Compounding**
course. The full course covers 12-week content engine design,
per-pillar production cadences, drive-to-business mechanics (post →
lead magnet → call), format-by-platform, and why post #100 is 10x the
lever of post #10.

→ [jaymountconsulting.com/learn/courses/founder-brand-compounding](https://jaymountconsulting.com/learn/courses/founder-brand-compounding)

Want it all-access? **[Operator Pass](https://jaymountconsulting.com/operator-pass)**.

## License

MIT. Built by [Jay Mount Consulting](https://jaymountconsulting.com).
