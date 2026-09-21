## MODIFIED Requirements

### Requirement: Verification pass

Before proposing anything, the skill SHALL verify the transcription against each scan page, resolve
or flag discrepancies, and record the flagged pages in `provenance.yaml`.

Verification SHALL run in bounded context on the same terms as transcription: one subagent per
batch, reading that batch's fragments together with that batch's scan images in a fresh context and
returning only a discrepancy list. It MUST NOT depend on scan images still being resident from the
transcription phase.

The mechanical house-style and math linter (`pipeline/houselint.py`, backed by `site/scripts/lint-math.mjs`)
SHALL run over each batch's fragments as they land, not only over the assembled `original.tex`. This
verifies that both house-style presentation rules and KaTeX mathematical syntax parse cleanly with
zero errors, so that any batch which introduces broken math or drifts from house style is identified
and corrected immediately.

**Verification against the scans is not sufficient on its own.** A per-batch pass compares page N's
text to page N's image, so it is structurally blind to any defect that spans a page or batch join,
or that makes two parts of the work disagree — which is the failure mode a batched architecture
most endangers. The skill SHALL therefore ALSO run a **text-only proofread of the assembled
`original.tex`**: one subagent, one context, reading the whole file together with the work's
notation glossary and **no scan images**, returning findings only.

That pass SHALL classify each finding as a **defect** (the transcription is internally broken), an
**inconsistency** (two parts of the work, or the work and its glossary, disagree), or **needs scan**
(only the print can settle it). It SHALL be given `provenance.yaml` so it does not re-report the
printer's errors already documented there. Its findings MUST be verified before they are acted on:
it cannot see the print, so a confident-sounding claim may be inference rather than observation.

This pass is cheap relative to what it covers — a 130KB work is roughly 32k tokens, about a
twentieth of the cost of scan-verifying the same pages — and it covers the whole work rather than
one batch.

#### Scenario: Discrepancies are flagged before proposing

- **WHEN** the verification pass finds a discrepancy between the transcription and a scan page
- **THEN** it is resolved or recorded as a flagged page in `provenance.yaml` before anything is proposed

#### Scenario: Verification re-reads its own images

- **WHEN** a batch is verified
- **THEN** its subagent reads that batch's scan images itself rather than relying on images read during transcription

#### Scenario: House-style drift is localized to its batch

- **WHEN** a batch's fragments violate a house-style ruling
- **THEN** `houselint` reports it as those fragments land, before the work is assembled

#### Scenario: Math syntax error in a fragment fails early linting

- **WHEN** a batch's fragment contains invalid KaTeX syntax, unsupported macros, or bare display environments
- **THEN** early linting reports the line and error and fails immediately before proceeding to the next batch

#### Scenario: A defect spanning a page join is caught

- **WHEN** a word, sentence, or convention is broken across a page or batch boundary
- **THEN** the text-only proofread reports it, even though every page passed its own check against its own scan image

#### Scenario: The proofread does not re-report documented misprints

- **WHEN** the work reproduces a printer's error that `provenance.yaml` already records under R4
- **THEN** the proofread leaves it alone rather than reporting it as a defect

#### Scenario: A proofread finding is verified before it is applied

- **WHEN** the text-only proofread asserts that some markup is broken
- **THEN** the claim is tested before any edit is made, because the pass cannot see the print and may be reasoning rather than observing
