# Contributing

Thanks for opening this repo. A few notes on how this project works
before you contribute.

## What kinds of contributions land

- **Bug reports** — open an issue with a reproducible case. The
  scripts in `scripts/` are deterministic, so bugs there are usually
  one-line fixes.
- **New modes** (`skills/founder-brand/modes/<mode>.md`) that extend the existing framework. Discuss in
  an issue first if it's a substantial addition.
- **Calibration improvements** to the scoring scripts — if you can
  show a case where the script scores wrong, that's gold.
- **Cross-runtime ports** (Cursor, Gemini CLI, Codex) — ship as
  separate plugins; clone this repo to work on the files locally.
- **Translation** of the framework reference docs.

## What doesn't land

- Renaming the JMC framework concepts (Signal → Pain → EVP → Ask, the
  5 Schwartz tiers, the 4 content pillars) — these are course-anchored.
- Adding LLM calls inside the skills. The whole point is that the
  skills are deterministic.
- Adding third-party packages to scripts. Scripts must work with the
  Python standard library only.
- Renaming `claude-*` → `<other-runtime>-*`. We ship per-runtime ports
  as separate plugins instead.

## Development setup

```
git clone https://github.com/cmj-hub/claude-founder-brand.git
cd claude-founder-brand
python3 scripts/score_post.py --help
python3 -m unittest discover -s tests
bash scripts/smoke-test.sh
```

## Pull-request checklist

- [ ] Skill names follow the spec (lowercase, hyphens, ≤64 chars,
      directory matches `name:` in frontmatter)
- [ ] The pack keeps one skill, `skills/founder-brand/SKILL.md`; new jobs are mode files
- [ ] If you touch a script, run `python3 -m unittest discover -s tests` and
      `bash scripts/smoke-test.sh` and paste output in the PR
- [ ] If you add a new mode, list it in the README table, the routing
      table and `argument-hint` in `skills/founder-brand/SKILL.md`, and add
      a trigger eval under `evals/`
- [ ] CHANGELOG.md updated
- [ ] No new dependencies (pip packages or npm packages)

## Reporting calibration issues with scoring scripts

If `score_post.py` scores something obviously wrong:

1. Paste the input that produced the wrong score
2. State your expected score + actual score
3. Note which axis is mis-calibrated

New calibration cases go in `tests/test_scoring.py` alongside the
lexicon change in `score_post.py`. The examples in `examples/` are
pinned (100 and 37) — a change that moves them updates the README too.

## License

By contributing, you agree your contributions ship under the MIT
license already on this repo.

## About

Built by [Jay Mount Consulting](https://jaymountconsulting.com).
Part of the JMC public-build spine — see [/build](https://jaymountconsulting.com/build).
