# Contributing to ReadTheMasters

Thank you for helping preserve the classics! This project runs on contributed compute: **you use
your own AI account**, and the project pays only for a domain. There are four ways to help, from
no-code to full pipeline.

## Before you start

1. **Check it isn't already here.** Search the [catalog] and `corpus/` by author + year (or
   Wikidata QID). Duplicates are closed.
2. **Claim it.** Add a row to [`corpus/CLAIMS.md`](corpus/CLAIMS.md) (PR or the `claim` issue
   label) so nobody duplicates your effort. Claims lapse after 60 days of inactivity.
3. **Confirm it's public domain.** The work must pass the copyright gate — see below.

## The copyright gate (non-negotiable)

A work may be published only if it passes `pipeline/validate.py`, which checks:

- **life + 70** — every author died ≥ 70 years ago (with sourced death dates);
- **US 95-year rule** — first published ≥ 95 years ago;
- **edition rights** — transcribed from an original/early edition, no modern apparatus;
- **translation source** — translations derive only from our own transcription.

Publication date and edition **must be sourced** (a catalog/DOI reference in `work.yaml:sources`),
or the gate fails. Run it locally:

```bash
pip install -r pipeline/requirements.txt
python pipeline/validate.py
```

## The four tiers

| Tier | You need | What you do |
|---|---|---|
| 0 Report errors | GitHub account | Click *Report an error* on any work page |
| 1 Chat transcription | Any AI chat subscription | Use [`prompts/transcribe-chat.md`](prompts/transcribe-chat.md) in your app; submit via the issue form |
| 2 Claude Code skill | Claude Pro/Max | Run `/transcribe <work> <pages>` (see `.claude/skills/transcribe/`) |
| 3 Full pipeline | Your own API key + Python | Run `pipeline/` scripts; open a PR |

### Adding a work by pull request (tiers 2–3)

1. Create `corpus/<id>/` with `work.yaml`, `provenance.yaml`, `original.tex`, and any
   `translations/<lang>.tex`. Copy an existing work (e.g. `corpus/riemann-1868-hypothesen/`) as a
   template. `<id>` follows PLAN.md §3.2 (Wikidata QID → DOI → `author-year-shorttitle`).
2. Use the shared house style: every `.tex` does `\usepackage{readmasters}`. Transcribe
   faithfully; normalize typography; keep the author's notation. Follow the math-typography
   conventions and rulings in [`corpus/HOUSESTYLE.md`](corpus/HOUSESTYLE.md). Figures are crops
   from the scan, embedded via `\rmfigure` (PLAN.md §4.5).
3. Run `python pipeline/validate.py` and `python -m pytest pipeline/tests -q` — both must pass.
4. Open a PR **with a DCO sign-off** (see below). A maintainer reviews against the scan and, on
   approval, the status advances up the ladder.

## Provenance & status

Every artifact records `model`, `effort` (optional), `prompt_version`, and a `status`:
`ai-draft` → `skimmed` → `verified`. Record the model you actually used — any capable model is
fine; the review ladder is the quality gate, not the brand.

## Licensing & Developer Certificate of Origin

Content is released under **CC0**, code under **MIT**. Sign off every commit to certify you may
contribute it under these terms:

```bash
git commit -s -m "Add <work>"
```

This appends `Signed-off-by: Your Name <you@example.com>` — the [DCO](https://developercertificate.org/).
Chat submissions include an "I release this under CC0" checkbox instead.

## Conduct

Be kind and constructive. Maintainers review all contributions; spam and vandalism are closed and
repeat abuse is blocked.

[catalog]: https://readthemasters.pages.dev/
