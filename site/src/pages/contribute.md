---
layout: ../layouts/Md.astro
title: Contribute
description: How to contribute transcriptions and translations using your own AI.
---

# Contribute

You can help by pointing out an error, or by transcribing a work yourself.

## Report an error

Every text has a **"Report an error"** link. Click it to open a pre-filled issue naming the work
and passage. This is the fastest way to improve quality — no account needed but GitHub.

## Transcribe a work yourself

1. Pick an unclaimed public-domain work (check the [claims list] and search the catalog first).
2. Produce the LaTeX transcription, in whichever way suits you:
   - **Your own AI chat, no coding** — copy our pinned prompt — [`prompts/transcribe-chat.md`] —
     into your AI app (Claude, etc.), upload a few scan pages at a time, and let it produce LaTeX
     in our house style.
   - **Claude Code skill** — if you use Claude Code with a Pro/Max subscription, run the repo's
     `/transcribe <work> <pages>` skill; it runs the pipeline and opens a pull request for you.
   - **Full pipeline, your own API key** — technical contributors run the `pipeline/` scripts with
     their own API key (Batch API), which emits full provenance automatically, then open a pull
     request.
3. Submit the result. Chat transcriptions go through the **"Chat transcription" issue form**,
   which records the work, pages, and which model/app you used — a maintainer then assembles it
   into the corpus format. The skill and full pipeline open a pull request directly.

Your text starts as an **AI draft** and is credited to you.

## Values

- **Notation is faithful, presentation follows house style.** Keep the author's own symbols,
  wording, and choices exactly as printed. How the same math is *set* (spacing, display vs
  inline, labels, headings) follows our house style so the corpus reads consistently. See
  [HOUSESTYLE.md] for the full rules.
- **Public domain only.** New works must pass the copyright gate (both the life+70 and US
  95-year rules) with sourced dates.
- **Credit & licensing.** Contributions are released under CC0 via a sign-off; you are credited in
  the work's provenance and on its page.

[claims list]: https://github.com/Davidwiskundige/readthemasters/blob/main/corpus/CLAIMS.md
[`prompts/transcribe-chat.md`]: https://github.com/Davidwiskundige/readthemasters/blob/main/prompts/transcribe-chat.md
[HOUSESTYLE.md]: https://github.com/Davidwiskundige/readthemasters/blob/main/corpus/HOUSESTYLE.md
