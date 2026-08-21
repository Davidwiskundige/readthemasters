---
layout: ../layouts/Md.astro
title: Contribute
description: How to contribute transcriptions and translations using your own AI.
---

# Contribute

You can help in three ways: point out an error, add a work to the corpus — by **transcribing** it
from its scan or **translating** one we've already transcribed — or **review** a text that's already
here.

## Report an error

Every text has a **"Report an error"** link. Click it to open a pre-filled issue naming the work
and passage.

## Add a work: transcribe or translate

The two are the same story with one word changed. Here it is in three steps.

**1. Pick what to work on, and claim it.**

- **Transcribing** — pick an unclaimed public-domain work (check the [claims list] and search the
  catalog first — or browse the [journals](/journals/) for original runs worth reviving). It must
  pass the copyright gate: both the life+70 and the US 95-year rules, with sourced dates.
- **Translating** — pick a work already in the catalog and a target language. There's no new
  copyright check to clear — the original already passed the gate — as long as you translate from
  our transcription, not from a modern, in-copyright translation.

Then open a quick [**claim**] so nobody doubles your effort. Claims are short-lived: if you haven't
opened a pull request within 24 hours the claim expires automatically, so the list always reflects
who's actually working right now.

**2. Produce the LaTeX, in whichever way suits you.**

- **Your own AI chat, no coding** — copy our pinned prompt ([`transcribe-chat.md`] or
  [`translate-chat.md`]) into your AI app (Claude, ChatGPT, etc.). For a transcription, upload a few
  scan pages at a time; for a translation, paste our `original.tex` for the section. The prompt
  makes it produce LaTeX in our house style.
- **A guided skill** — run [`/transcribe <work> <pages>`][skills] or `/translate <work> <lang>`.
  The skill reads the house-style rules, produces the LaTeX, validates it, and opens a pull request
  for you. See [using the skills elsewhere](#using-the-skills-elsewhere) below — it isn't only for
  Claude Code.
- **Full pipeline, your own API key** — technical contributors run the `pipeline/` scripts with
  their own API key (Batch API), which emits full provenance automatically, then open a pull
  request.

**3. Submit — through whichever door fits you.**

- **Issue form (no coding needed).** Send the LaTeX through the [**"Chat transcription"**] or
  [**"Chat translation"**] issue form, which records the work, pages or language, and which
  model/app you used. A maintainer then assembles it into the corpus format and credits you.
- **Pull request (open to anyone, not just maintainers).** If you're comfortable with git, you can
  add the files under `corpus/<work-id>/` yourself, run `python pipeline/validate.py` and the
  tests, and open a PR with a DCO sign-off. This gives you full provenance and CI checks up front.
  The skill and the full pipeline take this door for you automatically.

### Using the skills elsewhere

The `/transcribe` and `/translate` skills are just folders of Markdown instructions under
[`.claude/skills/`][skills] — nothing about them is locked to one app. A skill does two things:
produce house-style LaTeX, and assemble it into the corpus and open a PR.

- **In Claude Code, or any agent with the repo checked out** (for example via the Claude Agent SDK),
  both halves run: you get the LaTeX *and* an opened pull request, because the tool can read the
  repo, run `validate.py`, and use `git`.
- **On a chat surface without the repo** (a plain AI chat app, or another platform that supports
  Claude Skills but has no checkout), only the first half applies. There, use the matching pinned
  prompt above — it's the same house-style rules without the automation — and submit the result
  through the issue form.

## Quality status: AI draft → skimmed → verified

Your text starts as an **AI draft** (machine output, not yet human-checked) and is credited to
you. From there it can move up as people read it: *skimmed* once someone has given it a quick
pass, and *verified* after a full, rigorous check against the source. Each step records who
reviewed it, so the quality status always reflects the care a text has actually received.

You can do those review steps yourself — no need to be the original author. Open a work, read it
side by side with the linked scan, and:

- **Spot something wrong?** Use the **"Report an error"** link to flag the passage — that alone
  helps the next reviewer.
- **Want to promote it? (no coding needed)** Fill in the [**"Review a work"**] issue form: say
  which text you read, the level you reached (*skimmed* or *verified*), and what you checked. A
  maintainer records you in the reviewers list and advances the status.
- **Prefer a pull request?** Edit the work's `provenance.yaml` directly: add yourself to
  `reviewers` with the `level` and date, a short note on what you checked, and raise the artifact's
  `status` to match. A maintainer confirms it against the scan and merges.

Even a partial check is worth recording — just say in your note what you did and didn't cover.

## Values

- **Notation is faithful, presentation follows house style.** We keep the author's own symbols,
  wording, and choices exactly as printed. How the same math is *set* (spacing, display vs
  inline, labels, headings) follows our house style so the corpus reads consistently.
  See [HOUSESTYLE.md] for more details.
- **Public domain only.** New works must pass the copyright gate (both the life+70 and US
  95-year rules) with sourced dates.
- **Credit & licensing.** Contributions are released under CC0 via a sign-off; you are credited in
  the work's provenance and on its page.

[claims list]: https://github.com/Davidwiskundige/readthemasters/issues?q=is%3Aissue+is%3Aopen+label%3Aclaim
[**claim**]: https://github.com/Davidwiskundige/readthemasters/issues/new?template=claim.yml
[**"Chat transcription"**]: https://github.com/Davidwiskundige/readthemasters/issues/new?template=chat-transcription.yml
[**"Chat translation"**]: https://github.com/Davidwiskundige/readthemasters/issues/new?template=chat-translation.yml
[**"Review a work"**]: https://github.com/Davidwiskundige/readthemasters/issues/new?template=review.yml
[`transcribe-chat.md`]: https://github.com/Davidwiskundige/readthemasters/blob/main/prompts/transcribe-chat.md
[`translate-chat.md`]: https://github.com/Davidwiskundige/readthemasters/blob/main/prompts/translate-chat.md
[skills]: https://github.com/Davidwiskundige/readthemasters/tree/main/.claude/skills
[HOUSESTYLE.md]: https://github.com/Davidwiskundige/readthemasters/blob/main/corpus/HOUSESTYLE.md
