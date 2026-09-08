<p align="center">
  <img src="./assets/header.svg" alt="claude-founder-brand — four-pillar founder-led social" width="100%">
</p>

# claude-founder-brand

> Replace a $4K–8K/mo ghostwriter with a voice-aware content engine you control.

Founder-brand compounding is a four-pillar rotation — Pillar, Proof, Process, Person — written in the founder's voice. It refuses thought-leader cadence, engagement bait, and AI-detection filler.

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-founder-brand?style=social)](https://github.com/cmj-hub/claude-founder-brand)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-founder-brand — terminal demo of scoring a Proof post" width="100%">
</p>

Verified: `examples/proof.good.md` → **96/100**. `examples/proof.bad.md` (AI filler + engagement bait) → **37/100**.

## Install

Two commands. Works in Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, Antigravity, Goose, Continue, Roo, and the rest of the [skills CLI](https://skills.sh) agent list.

```bash
npx skills add cmj-hub/claude-founder-brand --all -g --full-depth
```

```text
/plugin marketplace add cmj-hub/claude-founder-brand
/plugin install founder-brand
```

The first line is the cross-harness install. The second is Claude Code's plugin (slash commands + reviewer agents).

npm (from GitHub — this pack is not on npmjs.com):

```bash
npm install github:cmj-hub/claude-founder-brand
npx jmc-founder-brand
```

`npx jmc-founder-brand` runs the same installer as `curl` below.

```bash
curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-founder-brand/main/install.sh | bash
```

Windows: `iwr https://raw.githubusercontent.com/cmj-hub/claude-founder-brand/main/install.ps1 -useb | iex`

## What you walk out with in 15 minutes

Artifact: one Proof post from the sample receipt (`examples/proof.good.md`). Score it, then write yours from a real receipt.

```bash
python3 scripts/score_post.py --post "$(cat examples/proof.good.md)"
python3 scripts/score_post.py --post "$(cat examples/proof.bad.md)"
```

One loop. One ICP. Example data. Then do yours.

## What this pack will not do

- It will not post for you.
- It will not fill a 12-week calendar on the first run.
- It will not invent receipts. No receipt, no Proof post.
- It will not sound like LinkedIn thought leadership. That is a refuse, not a style.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. That is the course + Operator Pass: the catalog that keeps moving, the tools that stay calibrated, the Friday room where you bring the artifact.

## Also in the pack

| Piece | Job |
|---|---|
| `founder-brand` orchestrator | Content / critique / hooks |
| `scripts/score_post.py` | Hook, specificity, voice, anti-patterns, skim, receipt |
| Four pillars | Pillar / Proof / Process / Person |
| Five hook archetypes | Contrarian, receipt, confession, pattern, reframe |

Sub-skills stay in the repo. First run is the loop above, not the operating system.

## Will this sound like LinkedIn thought leadership?

No. The scorer flags thought-leader cadence ("Stop. Read this."), engagement bait ("What's your take?"), and AI filler ("delve into", "in today's fast-paced world"). Specificity and a real receipt are required.

## Does it post for me?

No. It drafts and scores. You publish. Ghostwriting that does not sound like you is the problem this replaces; auto-posting is not in the pack.

## What is a receipt?

A named, checkable fact: "Series-B SaaS, 14 SQLs in 30 days from a PSP rewrite." Not "great results." Proof posts without a receipt fail the scorer.

## Suite, course, Operator Pass

- Suite: [https://jaymountconsulting.com/skills](https://jaymountconsulting.com/skills)
- Course: [Founder-Brand Compounding](https://jaymountconsulting.com/learn/courses/founder-brand-compounding)
- Operator Pass: [https://jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

Founder: $97/mo billed annually ($1,164/yr), locked for life if bought before October 31, 2026. After that: $197/mo billed annually ($2,364/yr), no lock.

## Companion packs

- **[Pain Signal Profile](https://github.com/cmj-hub/claude-psp)** — `claude-psp`
- **[Early Value Proposition](https://github.com/cmj-hub/claude-evp)** — `claude-evp`
- **[Signal-anchored cold email](https://github.com/cmj-hub/claude-cold-email)** — `claude-cold-email`
- **[Pricing surgery](https://github.com/cmj-hub/claude-pricing)** — `claude-pricing`
- **[Breakthrough Advertising (Schwartz)](https://github.com/cmj-hub/claude-breakthrough-advertising)** — `claude-breakthrough-advertising`
- **[Johanson / Stanley tutorial email](https://github.com/cmj-hub/claude-johanson-stanley)** — `claude-johanson-stanley`

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com). Public build: [https://jaymountconsulting.com/build](https://jaymountconsulting.com/build). Skill suite: [https://jaymountconsulting.com/skills](https://jaymountconsulting.com/skills).
