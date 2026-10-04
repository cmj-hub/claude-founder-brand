<p align="center">
  <img src="./assets/lockup.png" width="880" alt="LinkedIn posts skill for Claude Code. LinkedIn posts for founders are posts a buyer can tell came from the operator, written from a real receipt.">
</p>

# LinkedIn posts skill for Claude Code

LinkedIn posts for founders are posts a buyer can tell came from the operator, written from a real receipt.

> "In today's fast-paced world, what's your take?" is not a founder post. A named receipt is.

Founder-brand compounding is a four-pillar rotation — Pillar, Proof, Process, Person — written in the founder's voice. It refuses thought-leader cadence, engagement bait, and AI-detection filler.

You have paid a ghostwriter who does not sound like you. Or you have stared at a blank LinkedIn box and written "3 things I learned this week" because the feed rewards it. The feed also trains a reader to skip you.

The mechanism is the rotation plus a scorer. Pillar is the claim. Proof is the receipt. Process is how you actually do the work. Person is why you care. Skip a pillar for a month and the feed forgets which one you are.

A Proof post with a named receipt — Series-B, 14 SQLs, 30 days — scores **100**. The AI-pattern post (`delve into`, `fast-paced world`, `What's your take?`) scores **37** and is blocked outright. `scripts/score_post.py` is Python. No LLM. No paid API.

The build guide teaches a human. The pack teaches an agent.

<p align="center">
  <img src="./assets/demo.gif" alt="LinkedIn posts skill — proof post 96, AI-pattern post 37" width="100%">
</p>

## What this replaces

A $4K–8K/mo ghostwriter who cannot pass the scorer. You still have to live the stories. The pack writes in the voice you actually use.

## Install

Claude Code:

```text
/plugin marketplace add cmj-hub/gtm-operator-skills
/plugin install founder-brand@gtm-operator-skills
```

Then run `/founder-brand:founder-brand`.

Other agents (Cursor, Codex, Grok, Copilot, Windsurf, Cline, OpenCode):

```text
npx skills add cmj-hub/claude-founder-brand --all -g --full-depth
```

Every skill lives at `skills/<name>/SKILL.md`, so the repo also loads as a Claude Code plugin from a local clone. The scorer is Python 3 in this repo, standard library only.

## What's in the pack

| Skill | Job |
|---|---|
| `founder-brand` | Entry point. Loads your `brand-config.json` + `SOUL.md`, routes by argument: `content <pillar>`, `engine`, `critique`, `hooks`, `status`, `onboarding` |
| `founder-brand-onboarding` | 15-minute setup — writes `SOUL.md` (voice, phrases, stories) and `brand-config.json` (audience, pillar pools, cadence) in your project folder |
| `founder-brand-kickoff` | Reads state, says what's next, runs the weekly queue |
| `founder-content` | One post on one pillar, from one of your receipts, scored and saved to `drafts/` |
| `linkedin-craft` | Five hook variants, skim formatting, scored critique |

| Script | Job |
|---|---|
| `scripts/score_post.py` | 0–100 across hook, specificity, voice, anti-patterns, format, receipt. Banned phrases, engagement bait, your refused phrases, >3 hashtags, and a 10+ network blast block at any score |
| `scripts/check_setup.py` | What's filled, what's missing, which pillar is next, how many drafts this week |

## What you walk out with in 15 minutes

Artifact: `examples/proof.good.md`.

```
python3 scripts/score_post.py --file examples/proof.good.md
python3 scripts/score_post.py --file examples/proof.bad.md
```

One Proof post from the sample receipt. Then yours — from a fact that actually happened:

```
python3 scripts/score_post.py --file drafts/<your-draft>.md --soul SOUL.md
python3 scripts/check_setup.py --dir .
```

Exit 0 is ship. Exit 1 is rewrite. `--format json` for tooling.

## What this pack will not do

It will not post for you. It will not fill a 12-week calendar on the first run. It will not invent a receipt.

This pack drafts and scores. It will not pick this quarter's PSP, ingest your CRM, or update when Gmail changes the spam window. Those are judgement calls and live data. This pack gives you the instrument and the rubric; you bring the account.

## Will this sound like LinkedIn thought leadership?

No. The scorer flags "Stop. Read this.", "What's your take?", "delve into", and "in today's fast-paced world". A real receipt is required. That is a refuse, not a style.

## Does it post for me?

No. It drafts and scores. You publish. Auto-posting is not the job. Sounding like you is.

## What is a receipt?

A named, checkable fact. "Series-B SaaS, 14 SQLs in 30 days from a PSP rewrite." Not "great results." Proof posts without a receipt fail the scorer.

## On the site

- [Founder Brand pack](https://jaymountconsulting.com/skills/claude-founder-brand) — this pack's page
- [Skill packs catalog](https://jaymountconsulting.com/skills) — install paths + every pack
- [Course twin](https://jaymountconsulting.com/learn/courses/founder-brand-compounding) — human build guide for this pack

## Free, no signup

- **[LinkedIn Post Critic](https://jaymountconsulting.com/tools/linkedin-post-critic)** — the same job as this pack, hosted. No account, no key.
- [Founder-Led Social Selling framework](https://jaymountconsulting.com/frameworks/founder-led-social-selling)
- [Prompt Library](https://jaymountconsulting.com/resources/prompt-library)

## Free, by email

[**Growth Audit**](https://jaymountconsulting.com/growth-audit) — where your go-to-market stack is leaking, sent to your inbox.

That one does ask for an email, and it enrols you in a short follow-up on the same topic. Unsubscribe whenever.

[**The Friday Signal**](https://jaymountconsulting.com/newsletter/signal) — one free edition a week on building GTM systems that compound. No pitch in it.

## Privacy and security

Everything runs on your machine. The scripts are standard-library Python; they read your draft, `SOUL.md`, and `brand-config.json` and open no network connection. Skills write only `brand-config.json`, `SOUL.md`, and `drafts/` in your project folder. No telemetry, no credentials, and nothing is posted for you. See [SECURITY.md](SECURITY.md).

## Next

Previous: [Generative engine optimization](https://github.com/cmj-hub/claude-geo)

Next: [Cold email](https://github.com/cmj-hub/claude-cold-email)

## License

MIT. See [LICENSE](./LICENSE).

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
