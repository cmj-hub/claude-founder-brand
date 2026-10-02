<p align="center">
  <img src="./assets/header.png" alt="claude-founder-brand — four-pillar founder-led social: Pillar, Proof, Process, Person" width="100%">
</p>

# Social post

## Contents

- What this replaces
- Install
- What you walk out with in 15 minutes
- What this pack will not do
- Will this sound like LinkedIn thought leadership?
- Does it post for me?
- What is a receipt?
- Free, no signup
- Free, by email
- Companion packs
- License
- About
- Regenerating the artwork

> "In today's fast-paced world, what's your take?" is not a founder post. A named receipt is.

Founder-brand compounding is a four-pillar rotation — Pillar, Proof, Process, Person — written in the founder's voice. It refuses thought-leader cadence, engagement bait, and AI-detection filler.

You have paid a ghostwriter who does not sound like you. Or you have stared at a blank LinkedIn box and written "3 things I learned this week" because the feed rewards it. The feed also trains a reader to skip you.

The mechanism is the rotation plus a scorer. Pillar is the claim. Proof is the receipt. Process is how you actually do the work. Person is why you care. Skip a pillar for a month and the feed forgets which one you are.

A Proof post with a named receipt — Series-B, 14 SQLs, 30 days — scored **96**. The AI-pattern post (`delve into`, `fast-paced world`, `What's your take?`) scored **37**. `scripts/score_post.py` is Python. No LLM. No paid API.

The build guide teaches the framework to a human. This pack teaches the same framework to an agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/cmj-hub/claude-founder-brand?style=social)](https://github.com/cmj-hub/claude-founder-brand)
[![skills.sh](https://skills.sh/b/cmj-hub/claude-founder-brand)](https://skills.sh/cmj-hub/claude-founder-brand)
![No paid APIs](https://img.shields.io/badge/paid%20APIs-none-success)
![Install](https://img.shields.io/badge/install-npx%20skills-blue)

<p align="center">
  <img src="./assets/demo.gif" alt="claude-founder-brand — scoring a Proof post 96 vs an AI-pattern post 37" width="100%">
</p>

## What this replaces

A $4K–8K/mo ghostwriter who cannot pass the scorer. You still have to live the stories. The pack writes in the voice you actually use.

## Install

Two commands. Works in Claude Code, Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode, and the rest of the [skills CLI](https://skills.sh) list.

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

It will not post for you. It will not fill a 12-week calendar on the first run. It will not invent a receipt.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. Those are judgement calls and live data. This pack gives you the instrument and the rubric; you bring the account.

## Will this sound like LinkedIn thought leadership?

No. The scorer flags "Stop. Read this.", "What's your take?", "delve into", and "in today's fast-paced world". A real receipt is required. That is a refuse, not a style.

## Does it post for me?

No. It drafts and scores. You publish. Auto-posting is not the job. Sounding like you is.

## What is a receipt?

A named, checkable fact. "Series-B SaaS, 14 SQLs in 30 days from a PSP rewrite." Not "great results." Proof posts without a receipt fail the scorer.

## Free, no signup

- **[LinkedIn Post Critic](https://jaymountconsulting.com/tools/linkedin-post-critic)** — the same job as this pack, hosted. No account, no key.
- [Founder-Led Social Selling framework](https://jaymountconsulting.com/frameworks/founder-led-social-selling)
- [Prompt Library](https://jaymountconsulting.com/resources/prompt-library)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — where your go-to-market stack is leaking, sent to your inbox.

That one does ask for an email, and it enrols you in a short follow-up on the same topic. Unsubscribe whenever.

[**The Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one free edition a week on building GTM systems that compound. No pitch in it.


## Companion packs

- [claude-psp](https://github.com/cmj-hub/claude-psp) — Pain Signal Profile, the five-part buying brief
- [claude-evp](https://github.com/cmj-hub/claude-evp) — 22-word early value proposition per awareness tier
- [claude-cold-email](https://github.com/cmj-hub/claude-cold-email) — signal, pain, EVP, binary ask
- [claude-pricing](https://github.com/cmj-hub/claude-pricing) — three-tier contrast and pocket-price leaks

## License

MIT. See [LICENSE](./LICENSE).

## About

Public MIT pack. The scorer prints one post, one network, and one receipt. It refuses a ten-network blast.

## Regenerating the artwork

`assets/social-preview.png` and `assets/header.png` are generated from `assets/spec.json` by a vendored renderer — no CI, no shared workflow, no network beyond the webfonts:

```bash
node assets/card.mjs assets/spec.json assets/          # social-preview.png + header.png
npm i playwright-core && node assets/demo.mjs assets/spec.json assets/demo.gif
```
