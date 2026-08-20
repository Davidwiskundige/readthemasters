# copyright-gate

## Purpose

The publication gate that decides whether a work may appear on the site. Implemented in
`pipeline/validate.py`. Established by the `copyright-gate` change (archived 2026-07-18).

## Requirements

### Requirement: Publication rules

A work SHALL be published only if all applicable rules pass (`now_year` = current calendar year):

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

#### Scenario: Author cleared life + 70

- **WHEN** an author has a known `death_year` and `now_year >= death_year + 71`
- **THEN** the pma_70 rule passes for that author

#### Scenario: US 95-year rule not yet met

- **WHEN** `now_year < publication.year + 96`
- **THEN** us_publication fails and the work is not published

#### Scenario: Still-copyrighted translation is refused

- **WHEN** a hosted translation records provenance `source: external`
- **THEN** the translation_source rule fails and the build is blocked

### Requirement: Sourced facts

`sources.publication_date` and `sources.edition` MUST be non-empty (an unsourced publication date
or edition fails the gate). `sources.death_date` SHOULD be present (enables the Wikidata
cross-check).

#### Scenario: Unsourced publication date fails

- **WHEN** `sources.publication_date` is empty
- **THEN** the gate fails the work

### Requirement: copyright_assessment integrity

The gate MUST recompute the assessment from the sourced facts on every run. If `work.yaml` stores a
`copyright_assessment`, its per-rule verdicts and `public_domain` MUST match the recomputation, or
the gate fails (blocks stale/forged assessments). A work with `public_domain: false` is excluded
from the published build.

#### Scenario: Stale stored assessment is rejected

- **WHEN** a stored `copyright_assessment` disagrees with the gate's recomputed verdicts
- **THEN** the gate fails

#### Scenario: Non-public-domain work is excluded

- **WHEN** a work computes `public_domain: false`
- **THEN** it is excluded from the published build

### Requirement: Status & provenance consistency

Every artifact MUST carry a `status` on the ladder plus a `model` and `prompt_version`; `effort`, if
present, MUST be a recognized value. The site publishes artifacts at or above a configurable minimum
status (default `ai-draft`).

#### Scenario: Below-minimum status is withheld

- **WHEN** an artifact's status is below the configured minimum
- **THEN** the site does not publish that artifact

### Requirement: Cross-work checks

Each work `id` MUST be unique across the corpus and MUST equal its directory name.

#### Scenario: Duplicate id fails

- **WHEN** two works share the same `id`
- **THEN** the gate fails

### Requirement: Wikidata cross-check (warn-only)

A Wikidata death-year mismatch MUST NOT block the build: `pipeline/wikidata_check.py` compares each
author's `death_year` against Wikidata (via `wikidata_id`) and only warns.

#### Scenario: Mismatch warns but does not block

- **WHEN** an author's `death_year` differs from the Wikidata value
- **THEN** a warning is emitted and the build still succeeds
