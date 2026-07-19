# Capability: corpus-format

Current source of truth for how a work is stored. Established by the `corpus-format` change
(archived 2026-07-18) and extended by `site-catalog`.

## Requirement: Work directory layout

Each work lives in `corpus/<id>/`, where `<id>` is the canonical work id.

- `work.yaml` (required) — metadata + copyright assessment.
- `provenance.yaml` (required) — per-artifact status/model/effort/reviewers.
- `original.tex` (required once transcribed) — faithful transcription, original language.
- `translations/<lang>.tex` — one file per hosted translation language.
- `figures/` (optional) — figure crops taken from the public-domain scan.
- `pdf/<name>.pdf` (optional) — pre-made PDF override (see site-catalog PDF build).

## Requirement: work.yaml schema

Required: `id` (equals directory name, unique across corpus), `title`, `authors` (≥1, each
`name` + `wikidata_id` + `death_year` or `anonymous`), `publication` (`year`, `venue` ∈ vocab;
optional `volume`, `pages`, `title_full`), `edition` (`year`, `is_transcribed_edition`,
`rights_cleared`, `rights_note`), `discipline` ∈ vocab, `language` ∈ vocab, `type` ∈ vocab,
`source` (`scan_url`, `scan_id`), `sources` (citations for `death_date`, `publication_date`,
`edition`).

Optional: `title_en`, `tags` (each ∈ vocab), `external_translations` (list of referenced
translations elsewhere: `language`, `title`, `translator`, `year`, `license`, `venue`, `url`,
`note`), `copyright_assessment` (written/verified by the gate).

### Canonical work identity

`id` prefers a stable external identifier: Wikidata QID → DOI → deterministic
`author-year-shorttitle` slug. It is the directory name and the permanent URL.

## Requirement: provenance.yaml schema

Keys `transcription` and `translations.<lang>`, each an artifact record: `status`
(`ai-draft|spot-checked|proofread|validated`), `model` (required), `effort` (optional,
provider-agnostic or null), `prompt_version` (required), optional `submitted_via`, `produced`,
`reviewers` (list of `{name, level, date}`), and for translations a `source`
(`transcription` | `external-open` + `license`).

## Requirement: Controlled vocabulary

`corpus/vocab.yaml` defines allowed values for `disciplines`, `tags`, `venues`, `types`,
`languages`. Any metadata value outside it is rejected (prevents facet drift).

## Requirement: LaTeX house style

Every `.tex` uses `corpus/preamble/readmasters.sty`. Content and notation stay faithful to the
original; typography is normalized; markup is standardized. Apparatus macros: `\origpage{n}`,
`\uncertain{}`, `\illegible`, `\ednote{}`, `\rmfigure{file}{caption}{alt}` (figures are crops from
the scan, not redrawn).
