## ADDED Requirements

### Requirement: Antigravity Tier-2 transcription skill

An Antigravity workspace skill at `.agents/skills/transcribe/SKILL.md` SHALL transcribe a work's scan pages into `corpus/<work-id>/` and open a pull request. Invoked within Antigravity as `/transcribe <work-id> <pages>` or in response to an agentic transcription instruction.

The skill SHALL leverage Gemini 3.8 Flash's multimodal long-context capabilities:
1. **High-resolution scan ingestion**: The skill SHALL NOT enforce lossy 1568px long-edge downscaling or require interactive multi-turn region-by-region crop calculation (`magnify.py`); it SHALL ingest high-resolution page scans or half-page splits directly.
2. **Global Phase 0 Notation Scan**: The skill SHALL scan all page images of the work prior to page-by-page transcription to generate a comprehensive `corpus/<work-id>/notation.md` glossary, eliminating cross-batch notation drift before text generation begins.
3. **Long-context retention**: The skill MAY retain the entire work's images and preceding transcriptions resident in context across turns.
4. **Thinking effort**: The skill SHALL instruct Gemini 3.8 Flash with `effort: high` for both transcription and verification, and record this setting in `provenance.yaml`.
5. **Invariants**: The skill SHALL enforce the copyright gate as a hard precondition (`pipeline/validate.py`), adhere strictly to `prompts/transcribe-chat.md` and `corpus/HOUSESTYLE.md`, and record status `ai-draft` pending human review.

#### Scenario: Invoked in Antigravity to transcribe a work
- **WHEN** a contributor asks Antigravity to transcribe a public-domain work
- **THEN** the skill executes the transcription pipeline and opens a pull request

#### Scenario: Global notation scan before transcription
- **WHEN** transcribing a multi-page work
- **THEN** all scan pages are examined upfront to establish `notation.md` before any page fragment is emitted

#### Scenario: High-resolution scans without interactive magnification turns
- **WHEN** page scans contain fine mathematical subscripts and punctuation
- **THEN** high-resolution scans or split tiles are provided upfront without requiring interactive multi-turn `magnify.py` crop escalation

#### Scenario: Copyright gate blocks non-compliant works
- **WHEN** `pipeline/validate.py` fails or the work is not public domain
- **THEN** the skill refuses to transcribe or open a PR

### Requirement: Antigravity proofread-first verification sequencing

The Antigravity transcription skill SHALL execute a whole-work text-only proofread of the assembled `original.tex` **before** the scan verification pass, and route all findings classified as `NEEDS SCAN` directly into the scan verification pass so each page's scan is opened only once.

The skill SHALL run `pipeline/houselint.py` over each page fragment as it is written to identify house-style drift immediately before file stitching.

The skill SHALL record the verification model (e.g. `gemini-3-8-flash`) and an explicit total count of `uncertainty_flags` in `provenance.yaml`.

#### Scenario: Text-only proofreading routes needs-scan queries to scan verifier
- **WHEN** the assembled text is proofread
- **THEN** structural and linguistic issues are checked without images, and any reading requiring visual confirmation is handed to the scan verification pass as a targeted `needs scan` query

#### Scenario: Early house-style linting catches fragment issues
- **WHEN** a LaTeX fragment is written to scratch
- **THEN** `pipeline/houselint.py` validates the fragment before assembly into `original.tex`

#### Scenario: Verification model and uncertainty count recorded
- **WHEN** provenance is authored
- **THEN** `provenance.yaml` includes the verification model and the explicit integer count of uncertainty flags (including 0)

### Requirement: Skill metadata and path integrity testing

The automated test suite SHALL verify the structure, YAML frontmatter, and referenced path integrity of the Antigravity skill at `.agents/skills/transcribe/SKILL.md` via `pipeline/tests/test_skills.py`.

#### Scenario: Skill file and frontmatter validation
- **WHEN** pytest runs `pipeline/tests/test_skills.py`
- **THEN** it verifies that `.agents/skills/transcribe/SKILL.md` exists, contains valid YAML frontmatter with `name: transcribe` and a non-empty `description`, and all referenced repo paths and templates exist
