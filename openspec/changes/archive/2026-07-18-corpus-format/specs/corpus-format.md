# Spec (delta): corpus-format

## ADDED: Work directory layout

Each work lives in `corpus/<id>/` where `<id>` is the canonical work id (PLAN.md §3.2):

```
corpus/<id>/
  work.yaml           # metadata + copyright assessment (required)
  provenance.yaml     # per-artifact status/model/effort/reviewers (required)
  original.tex        # faithful transcription, original language (required once transcribed)
  translations/
    <lang>.tex        # one file per translation language
  figures/            # figure crops from the PD scan (optional)
    fig-01.png
```

## ADDED: work.yaml schema

Required fields:

- `id` (string) — canonical id; must equal the directory name; unique across the corpus.
- `title` (string) — original-language title.
- `title_en` (string, optional) — English title for display.
- `authors` (list, ≥1) — each: `name`, `wikidata_id` (`Q…` or null), `death_year` (int or null),
  `birth_year` (int, optional), `anonymous` (bool, optional).
- `publication`:
  - `year` (int) — first-publication year (the year that matters for the US rule).
  - `venue` (string) — must be a key in `vocab.yaml: venues`.
  - `title_full` (string, optional) — full citation string.
- `edition`:
  - `year` (int) — year of the specific scanned edition.
  - `is_transcribed_edition` (bool) — true for the edition we transcribed from.
  - `rights_cleared` (bool) — true if this edition carries no fresh edition/critical-apparatus copyright.
  - `rights_note` (string) — justification for `rights_cleared`.
- `discipline` (string) — key in `vocab.yaml: disciplines`.
- `tags` (list of strings, optional) — each a key in `vocab.yaml: tags`.
- `language` (string) — ISO 639-1 code; key in `vocab.yaml: languages`.
- `type` (string) — key in `vocab.yaml: types` (paper, book, chapter, letter, lecture).
- `source`:
  - `scan_url` (string) — link to the scan.
  - `scan_id` (string) — stable identifier (Archive.org id, permalink, …).
- `sources` — citations for the copyright-critical facts (PLAN.md §2.5):
  - `death_date` (string) — e.g. `wikidata:Q42` (per author, or a map keyed by author name).
  - `publication_date` (string) — catalog/bibliography/DOI reference.
  - `edition` (string) — catalog reference for the edition.
- `external_translations` (list, optional) — existing translations elsewhere, referenced not
  hosted. Each: `language`, `title`, `translator`, `year`, `license`, `venue` (optional), `url`,
  `note` (optional). Pure metadata (a link is always allowed); separate from hosted
  `translations/<lang>.tex`.
- `copyright_assessment` — written/verified by the gate; see copyright-gate spec.

## ADDED: provenance.yaml schema

Top-level keys `transcription` and `translations.<lang>`, each an artifact record:

- `status` — one of `ai-draft | spot-checked | proofread | validated`.
- `model` (string) — model that produced the current text.
- `effort` (string or null, optional) — thinking/effort level; provider-agnostic
  (`low|medium|high|xhigh|max|adaptive|extended|standard`) or null.
- `prompt_version` (string) — pinned pipeline/chat prompt version.
- `submitted_via` (string, optional) — `pipeline | chat`.
- `produced` (date) — ISO date.
- `reviewers` (list, optional) — each `{name, level, date}`.

## ADDED: Controlled vocabulary

`corpus/vocab.yaml` defines allowed values for `disciplines`, `tags`, `venues`, `types`,
`languages`. The validator rejects any metadata value not present here (prevents facet drift, e.g.
"Ann. d. Physik" vs "Annalen der Physik").

## ADDED: LaTeX house style

Every `.tex` uses `corpus/preamble/readmasters.sty`. Apparatus macros: `\origpage{n}`,
`\uncertain{text}`, `\illegible`, `\ednote{text}`, `\rmfigure{file}{caption}{alt}`. Content and
notation stay faithful to the original; typography is normalized; markup is standardized.
