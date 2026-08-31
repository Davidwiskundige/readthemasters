## MODIFIED Requirements

### Requirement: Work directory layout

Each work SHALL live in `corpus/<id>/`, where `<id>` is the canonical work id.

- `work.yaml` (required) — metadata + copyright assessment.
- `provenance.yaml` (required) — per-artifact status/model/effort/reviewers.
- `original.tex` (required once transcribed) — faithful transcription, original language.
- `notation.md` (optional) — the work's cross-page rendering decisions (see transcription-pipeline).
- `translations/<lang>.tex` — one file per hosted translation language.
- `figures/` (optional) — figure crops taken from the public-domain scan.
- `pdf/<name>.pdf` (optional) — pre-made PDF override (see site-catalog PDF build).

`notation.md` is a permanent work artifact, not a working file: it is committed with the
transcription and kept after the transcription reaches `verified`. It records the decisions a later
transcriber, translator, or reviewer would otherwise have to re-derive from the scan — which glyph
the author's summation sign is, whether a house-style ruling applies to this print at all, how a
recurring symbol is disambiguated. Keeping it makes re-transcription, translation, and review of the
same work cheaper, and makes those decisions reviewable in a pull-request diff rather than implicit
in the LaTeX.

#### Scenario: Work stored under its canonical id

- **WHEN** a work with canonical id `<id>` is added
- **THEN** it lives in `corpus/<id>/` with `work.yaml` and `provenance.yaml` present (and `original.tex` once transcribed)

#### Scenario: Notation decisions are kept with the work

- **WHEN** a transcription required a cross-page rendering decision
- **THEN** `corpus/<id>/notation.md` records it and is committed alongside `original.tex`, and it is retained after the transcription is marked `verified`

#### Scenario: A work needing no such decision has no notation.md

- **WHEN** a work is transcribed without any cross-page rendering decision
- **THEN** no `notation.md` is written and `pipeline/validate.py` passes
