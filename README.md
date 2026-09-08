<p align="center">
  <img src="./assets/header.svg" alt="claude-founder-brand — four-pillar founder-led social" width="100%">
</p>

# claude-founder-brand

> A ghostwriter writes like a ghostwriter. This pack refuses that cadence on purpose.

Founder-brand compounding is a four-pillar rotation — Pillar, Proof, Process, Person — written in the founder's voice. It refuses thought-leader cadence, engagement bait, and AI-detection filler.

"In today's fast-paced world, let me delve into…" scored **37**.
A Proof post with a named receipt — Series-B, 14 SQLs, 30 days — scored **96**.

The scorer is Python in this repo. No LLM. No paid API.

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-founder-brand?style=social)](https://github.com/cmj-hub/claude-founder-brand)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-founder-brand — terminal demo of scoring a Proof post" width="100%">
</p>

## Install

Two commands. Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, and the rest of the [skills CLI](https://skills.sh) list.

```bash
npx skills add cmj-hub/claude-founder-brand --all -g --full-depth
```

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install founder-brand
```

Also: `npm install github:cmj-hub/claude-founder-brand` then `npx jmc-founder-brand`. Or `curl -fsSL https://raw.githubusercontent.com/cmj-hub/claude-founder-brand/main/install.sh | bash`.

## What you walk out with in 15 minutes

Artifact: `examples/proof.good.md`.

```bash
python3 scripts/score_post.py --post "$(cat examples/proof.good.md)"
python3 scripts/score_post.py --post "$(cat examples/proof.bad.md)"
```

One Proof post from the sample receipt. Then yours — from a fact that actually happened.

## What this pack will not do

It will not post for you.
It will not fill a 12-week calendar on the first run.
It will not invent a receipt.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. That is the course + Operator Pass: the catalog that keeps moving, the tools that stay calibrated, the Friday room where you bring the artifact.

## Will this sound like LinkedIn thought leadership?

No. The scorer flags "Stop. Read this.", "What's your take?", "delve into", and "in today's fast-paced world".
A real receipt is required. That is a refuse, not a style.

## Does it post for me?

No. It drafts and scores. You publish.

## What is a receipt?

A named, checkable fact.
"Series-B SaaS, 14 SQLs in 30 days from a PSP rewrite."
Not "great results."
Proof posts without a receipt fail.

## Suite, course, Operator Pass

- Suite: [gtm-operator-skills](https://github.com/cmj-hub/gtm-operator-skills) · [jaymountconsulting.com/skills](https://jaymountconsulting.com/skills)
- Course: [Founder-Brand Compounding](https://jaymountconsulting.com/learn/courses/founder-brand-compounding)
- Operator Pass: [jaymountconsulting.com/operator-pass](https://jaymountconsulting.com/operator-pass)

Founder: $97/mo billed annually ($1,164/yr), locked for life if bought before October 31, 2026. After that: $197/mo billed annually ($2,364/yr), no lock.

## Companion packs

- [claude-psp](https://github.com/cmj-hub/claude-psp) — five-part buying brief
- [claude-evp](https://github.com/cmj-hub/claude-evp) — 22-word line per Schwartz tier
- [claude-cold-email](https://github.com/cmj-hub/claude-cold-email) — signal, pain, EVP, binary ask
- [claude-pricing](https://github.com/cmj-hub/claude-pricing) — three-tier contrast + pocket-price leaks

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
