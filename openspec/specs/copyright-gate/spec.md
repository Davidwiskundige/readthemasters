# Capability: copyright-gate

Current source of truth for the publication gate. Implemented in `pipeline/validate.py`.
Established by the `copyright-gate` change (archived 2026-07-18).

## Requirement: Publication rules

A work MAY be published only if all applicable rules pass (`now_year` = current calendar year):

- **pma_70** — every author cleared life + 70. Author with known `death_year`:
  `now_year >= death_year + 71`. Anonymous author: `now_year >= publication.year + 71`. Unknown
  death date (not anonymous): only clears if `now_year >= publication.year + 170`; otherwise the
  work is blocked.
- **us_publication** — `now_year >= publication.year + 96` (US 95-year rule, Jan-1 rollover).
- **edition_rights** — `edition.rights_cleared` is true with a non-empty `edition.rights_note`.
- **translation_source** — each hosted translation has provenance `source` of `transcription`
  (default) or `external-open` (which REQUIRES a named `license`). `source: external`
  (still-copyrighted) fails; such translations may be *referenced* via `external_translations`
  but never hosted.
- **pma_100** (optional, config `--strict-pma-100`, default off) — like pma_70 with term 100.

## Requirement: Sourced facts

`sources.publication_date` and `sources.edition` MUST be non-empty (an unsourced publication date
or edition fails the gate). `sources.death_date` SHOULD be present (enables the Wikidata
cross-check).

## Requirement: copyright_assessment integrity

The gate recomputes the assessment from the sourced facts on every run. If `work.yaml` stores a
`copyright_assessment`, its per-rule verdicts and `public_domain` MUST match the recomputation, or
the gate fails (blocks stale/forged assessments). A work with `public_domain: false` is excluded
from the published build.

## Requirement: Status & provenance consistency

`status` ∈ the ladder; `validated` requires ≥ 2 distinct reviewers; `model` and `prompt_version`
required on every artifact; `effort`, if present, is a recognized value. The site publishes
artifacts at or above a configurable minimum status (default `ai-draft`).

## Requirement: Cross-work checks

`id` is unique across the corpus and equals the directory name.

## Requirement: Wikidata cross-check (warn-only)

`pipeline/wikidata_check.py` compares each author's `death_year` against Wikidata (via
`wikidata_id`); mismatches warn but never block the build.
