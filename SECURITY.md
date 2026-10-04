# Security

## What this pack does on your machine

- Two scripts run locally: `scripts/score_post.py` and `scripts/check_setup.py`. Both are standard-library Python 3. No dependencies are installed.
- They read only what you point them at: a draft file or post text, `SOUL.md`, `brand-config.json`, and the `drafts/*.md` frontmatter in your project folder.
- The skill writes only to your project folder: `brand-config.json` and `SOUL.md` (field-level merge, this pack's own keys and sections), and post drafts under `drafts/`.
- Network: none. No script opens a network connection, and the skill is granted no web tool.
- No telemetry. Nothing is logged or sent anywhere.
- No credentials are asked for or stored. The pack never needs a LinkedIn login or API key.
- Nothing is posted or published. The pack drafts and scores; you publish.
- `install.sh` / `install.ps1` print where the pack lives and exit. They download and execute nothing.

## Reporting a vulnerability

Email jay@jaymountconsulting.com with "security" and the repo name in the subject, or open a private advisory under this repo's Security tab. Do not open a public issue for a vulnerability. Expect a reply within five business days.

## Supported versions

Only the latest release on `main` gets fixes.
