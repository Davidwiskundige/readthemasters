# Delta: corpus-format — optional LaTeX title fields

## ADDED Requirements

### Requirement: Optional LaTeX title fields

`work.yaml` MAY carry `title_tex` and/or `title_en_tex`: LaTeX renderings of `title` / `title_en`
that carry inline `$…$` math for on-page display. They are optional and additive; the plain `title`
(required) and `title_en` (optional) remain the canonical, machine-readable forms used for the
browser tab, search index, and structured data. The copyright gate does not consider these fields.

#### Scenario: A work supplies a LaTeX title

- **WHEN** a `work.yaml` sets `title_tex` (and optionally `title_en_tex`)
- **THEN** validation still passes with the plain `title` as the canonical field
- **AND** the build carries `title_tex` / `title_en_tex` into `works.json` for the site to render

#### Scenario: LaTeX title fields are optional

- **WHEN** a `work.yaml` omits `title_tex` / `title_en_tex`
- **THEN** it validates and builds unchanged, with the plain title used everywhere
