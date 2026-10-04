---
name: founder-brand-kickoff
description: Adaptive router for the founder-brand skill pack. Runs scripts/check_setup.py to detect state (brand-config? SOUL filled? pillars filled? cadence set? this week's drafts?) and picks the next-best step. Use when the main founder-brand skill runs with no arguments or "status", or when the operator asks "where do I start", "what's next for my content", "founder-brand status".
user-invocable: false
allowed-tools: Read Grep Glob Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_setup.py:*)
license: MIT
models: ""

---

# Founder-Brand Kickoff — adaptive router

## Activation

Loaded by `founder-brand` on bare invocation or `status`, or:
- "Where do I start"
- "What's next for my content"

## State detection

Don't guess state — run the checker from the operator's project folder:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_setup.py --dir . --format json
```

It reads `brand-config.json`, `SOUL.md`, and `drafts/*.md` and returns:

| Field | Meaning |
|---|---|
| `checks.has_brand_config` / `checks.has_soul` | Files exist |
| `checks.soul_filled` | No `<placeholder>` lines left in `SOUL.md` |
| `checks.pillars_filled` | All 4 pillars have ≥3 topics |
| `checks.voice_fingerprints` | ≥5 phrases-I-use |
| `checks.stories_reservoir` | ≥3 stories |
| `checks.cadence_set` | `cadence.posts_per_week` > 0 |
| `posts_this_week` / `this_week_done` | Drafts dated Monday→today vs cadence |
| `next_pillar` | Next slot after the last draft, in `rotation_order` |
| `drifting_pillars` | Pillars with no draft in 4+ weeks |
| `next_step` | The one thing to do now |

If Bash is unavailable, read the files directly and apply the same rules.

| State | Route to |
|---|---|
| `!has_brand_config OR !has_soul OR !soul_filled` | `founder-brand-onboarding` |
| `!pillars_filled` | "Fill pillar topic pools (need ≥3 per pillar)." → onboarding Step 7 |
| `!voice_fingerprints` | "Mine phrases-I-use list — need ≥5. Read your last 10 posts/emails." → onboarding Step 2 |
| `!stories_reservoir` | "Capture ≥3 stories. Anonymized but specific." → onboarding Step 5 |
| `!cadence_set` | "Pick weekly cadence — default 4 posts/week, 1 per pillar." → onboarding Step 8 |
| `this_week_done` | "This week's queue done. Re-run on Monday for next rotation." |
| else | Weekly mode for `next_pillar` |

## Welcome flow

```
> /founder-brand

Welcome.

[Detected: brand-config.json missing]

You're at step 1 of 5:
1. ⬜ Onboarding — voice + 4-pillar pools + cadence (15 min)   ← YOU ARE HERE
2. ⬜ Mine ≥5 voice fingerprints from your existing writing
3. ⬜ Capture ≥3 stories for the Proof reservoir
4. ⬜ Generate first week's posts (1 per pillar in rotation)
5. ⬜ Iterate weekly — draft → score → ship → mark published

Step 1 takes ~15 minutes. Ready? (y/n)
```

Tick the steps the checker already passes.

## Weekly mode

When setup is complete and `this_week_done == false`:

```
# This week's queue — <posts_this_week> of <posts_per_week> drafted

You're on the <next_pillar> rotation slot. Topic suggestion from your pool:

  "<Topic from brand-config.pillars.<next_pillar>.topic_pool>"

Want me to draft it? (y/n)

Other pool options for this slot:
  "<Topic 2>"
  "<Topic 3>"
```

Prefer topics not already used in `drafts/` (grep the `topic:` lines).
If `drifting_pillars` is non-empty, say so and offer that pillar first.

On "y", load `founder-content` with the pillar and topic locked.

## Status mode

`/founder-brand status` → run the checker with `--format text` and show
its output as-is, then one line on the next step:

```
# Founder-brand status

Brand config:  ✓ brand-config.json
SOUL:          ✓ SOUL.md (8 phrases, 7 refused, 5 stories, 0 placeholders left)
Pillar pools:  ✓ pillar 3, proof 3, process 3, person 3
Cadence:       ✓ 4 posts/week, Pillar → Proof → Process → Person
This week:     2 of 4 drafted (1 published) since 2026-10-05

Next: Draft this week's Process post from your topic pool.
```
