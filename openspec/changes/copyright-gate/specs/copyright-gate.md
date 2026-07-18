# Spec (delta): copyright-gate

## ADDED: Publication rules

A work MAY be published only if all applicable rules pass. `now_year` is the current calendar year.

- **pma_70** — for every author: `author.death_year` is known and
  `now_year >= death_year + 70 + 1` (public domain from 1 Jan of the year after life+70).
  - If `death_year` is null: the work passes pma_70 only if it is old enough that any plausible
    lifespan is covered — `now_year >= publication.year + 70 + 100` (author could have lived 100
    years past publication). Otherwise pma_70 FAILS and the work is blocked.
- **us_publication** — `now_year >= publication.year + 95 + 1` (public domain from 1 Jan of the
  year after publication+95). Equivalent to: published before `now_year - 95`.
- **edition_rights** — `edition.rights_cleared` is true (with a non-empty `edition.rights_note`).
- **translation_source** — for every translation, its provenance `submitted_via`/source indicates
  derivation from our own transcription, never an external modern translation. (Enforced by
  requiring translations to reference the in-corpus `original.tex`; a `translation_source: external`
  marker FAILS.)
- **pma_100** (optional, config `strict_pma_100: true`, default false) — like pma_70 with term 100.

## ADDED: Sourced facts (§2.5)

- `sources.publication_date` MUST be non-empty — an unsourced publication date FAILS the gate.
- `sources.edition` MUST be non-empty.
- `sources.death_date` SHOULD be present (a Wikidata id enables the warn-only cross-check).

## ADDED: copyright_assessment output

The gate writes/refreshes a block recording, for each rule: the inputs used, the verdict, and a
timestamp; plus an overall `public_domain: true|false`. A work with `public_domain: false` is
excluded from the published build.

## ADDED: Status & provenance consistency

- `status` ∈ {ai-draft, spot-checked, proofread, validated}.
- `validated` requires ≥ 2 distinct reviewers in provenance.
- `model` and `prompt_version` are required on every artifact.
- The site publishes artifacts at or above a configurable minimum status (default `ai-draft`).

## ADDED: Cross-work checks

- `id` is unique across the corpus and equals the directory name.
