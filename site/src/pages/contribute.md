---
layout: ../layouts/Md.astro
title: Contribute
description: How to contribute transcriptions and translations using your own AI.
---

# Contribute

You can help at whatever level suits you. **The project pays for no AI compute** — every AI step
runs on *your* own account, so contributions cost the project nothing.

## Tier 0 — Report an error (no account needed but GitHub)

Every text has a **"Report an error"** link. Click it to open a pre-filled issue naming the work
and passage. This is the fastest way to improve quality.

## Tier 1 — Transcribe in your own AI chat (no coding)

1. Pick an unclaimed public-domain work (check the [claims list] and search the catalog first).
2. Copy our pinned prompt — [`prompts/transcribe-chat.md`] — into your AI app (Claude, etc.).
3. Upload a few scan pages at a time and let it produce LaTeX in our house style.
4. Submit the result through the **"Chat transcription" issue form**, which records the work,
   pages, and which model/app you used.

A maintainer assembles submissions into the corpus format. Your text starts as an **AI draft** and
is credited to you.

## Tier 2 — Claude Code skill

If you use Claude Code with a Pro/Max subscription, run the repo's `/transcribe <work> <pages>`
skill; it runs the pipeline and opens a pull request for you.

## Tier 3 — Full pipeline (your API key)

Technical contributors run the `pipeline/` scripts with their own API key (Batch API), which emits
full provenance automatically, then open a pull request.

## Ground rules

- **Faithful, not modernized.** Transcribe exactly what the original says; don't update notation.
- **Public domain only.** New works must pass the copyright gate (both the life+70 and US
  95-year rules) with sourced dates.
- **Credit & licensing.** Contributions are released under CC0 via a sign-off; you are credited in
  the work's provenance and on its page.

[claims list]: https://github.com/OWNER/readthemasters/blob/main/corpus/CLAIMS.md
[`prompts/transcribe-chat.md`]: https://github.com/OWNER/readthemasters/blob/main/prompts/transcribe-chat.md
