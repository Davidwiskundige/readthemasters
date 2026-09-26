## MODIFIED Requirements

### Requirement: Verification pass

This requirement SHALL govern the Claude Code Tier-2 skill at `.claude/skills/transcribe/` only. The
corpus is transcribed by two skills whose cost dynamics differ on purpose — this one, built around
bounded-context subagents on Claude models, and the Antigravity skill at `.agents/skills/transcribe/`
built around Gemini 3.8 Flash's long context. Everything below about subagents, turns and
magnification governs the Claude Code skill; the Antigravity skill carries its own requirements in
this spec and is not bound by these.

Before proposing anything, the skill SHALL verify the transcription against each scan page, resolve
or flag discrepancies, and record the flagged pages in `provenance.yaml`.

Verification SHALL run in bounded context on the same terms as transcription: one subagent per
batch, reading that batch's fragments together with that batch's scan images in a fresh context and
returning only a discrepancy list. It MUST NOT depend on scan images still being resident from the
transcription phase.

Because each verification subagent re-reads its own images and consumes no other subagent's output,
the batch verifiers have no ordering dependency among themselves and SHALL be dispatched
**concurrently**.

The text-only proofread described below SHALL run **before** the batch verifiers, not after them,
and each verifier SHALL be given the proofread's `needs scan` findings for its own pages. A
`needs scan` finding is by definition one only the print can settle, and the verifiers are the only
pass that reads the print; resolving them afterwards requires a further subagent and a second
reading of the same images.

The model tier used for verification SHALL be recorded in `provenance.yaml`, so that a run's
verification tier is stated rather than inferred. A tier below the one used for transcription MAY be
used only where a like-for-like comparison on the same pages has shown it misses none of the
corrections the higher tier found.

The mechanical house-style linter (`pipeline/houselint.py`) SHALL run over each batch's fragments as
they land, not only over the assembled `original.tex`, so that a batch which drifts from house style
is identified as the batch that caused it.

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
one batch. It runs once, over the assembled file, ahead of the batch verifiers.

#### Scenario: Discrepancies are flagged before proposing

- **WHEN** the verification pass finds a discrepancy between the transcription and a scan page
- **THEN** it is resolved or recorded as a flagged page in `provenance.yaml` before anything is proposed

#### Scenario: Verification re-reads its own images

- **WHEN** a batch is verified
- **THEN** its subagent reads that batch's scan images itself rather than relying on images read during transcription

#### Scenario: Batch verifiers run concurrently

- **WHEN** more than one batch is to be verified against the scans
- **THEN** their subagents are dispatched concurrently rather than one after another

#### Scenario: A needs-scan finding is settled by the pass that reads the scan

- **WHEN** the text-only proofread classifies a finding as `needs scan`
- **THEN** it is handed to the batch verifier covering that page, and settled during that verifier's own reading of the scan rather than by a further subagent afterwards

#### Scenario: The verification tier is recorded

- **WHEN** a transcription run completes
- **THEN** `provenance.yaml` states the model tier the verification pass ran on

#### Scenario: House-style drift is localized to its batch

- **WHEN** a batch's fragments violate a house-style ruling
- **THEN** `houselint` reports it as those fragments land, before the work is assembled

#### Scenario: A defect spanning a page join is caught

- **WHEN** a word, sentence, or convention is broken across a page or batch boundary
- **THEN** the text-only proofread reports it, even though every page passed its own check against its own scan image

#### Scenario: The proofread does not re-report documented misprints

- **WHEN** the work reproduces a printer's error that `provenance.yaml` already records under R4
- **THEN** the proofread leaves it alone rather than reporting it as a defect

#### Scenario: A proofread finding is verified before it is applied

- **WHEN** the text-only proofread asserts that some markup is broken
- **THEN** the claim is tested before any edit is made, because the pass cannot see the print and may be reasoning rather than observing

### Requirement: Capped per-page escalation

This requirement SHALL govern the Claude Code Tier-2 skill at `.claude/skills/transcribe/` only.
Magnification exists because that skill sends one downscaled image per page and must buy the lost
resolution back a region at a time. The Antigravity skill ingests high-resolution scans or split
tiles directly and is explicitly exempted from interactive `magnify.py` escalation by its own
requirement; nothing here binds it.

A batch subagent SHALL be able to crop and magnify a specific doubtful region of its own pages into a
scratch directory, and the number of magnified regions per page MUST be capped (default 3).

The capability is required because one image per page costs roughly 21% of the text width; without
it, a subagent's `\uncertain{}` flags measure the tooling it was given rather than the legibility of
the scan, which would invalidate any quality comparison. The cap is required because the capability
is used freely when ungoverned — an observed run produced 32 magnified crops for 4 pages, which would
add more turns than the one-image-per-page design removes.

Magnification SHALL be **batched**: a page's regions are produced by a single invocation of the
magnification helper, and a batch's invocations and crop reads are issued together rather than one
per turn. Per-region cropping is forbidden, because each region cropped on its own costs a
compute-and-save turn plus a read turn, and at a measured 1.7 regions per page that escalation tax
roughly doubled the turns per page — the dominant term in the cost of a run.

The per-page cap MUST hold **across invocations, not merely within one**. A second call for the same
page buys no further regions. Measured: a batch given a per-call cap took "3 + 1 follow-up" regions
on one page — inside the cap twice, past it in total — and silently overwrote its own first crop,
because output names restart at `r1` on each call.

**Batching is a property of the instruction, not of the helper, and MUST be stated to the subagent.**
Measured across five batches of four pages with identical tooling: a batch that wrote its four
fragments in four separate messages cost **12 turns**, against **4** for batches that issued the
reference reads, the chained magnification, the crop reads and the fragment writes as one message
each. Three times the cost for the same work. The instruction SHALL therefore tell the subagent to
issue every independent call together, naming the fragment writes explicitly.

Magnification is preferred over raising `\uncertain{}` where it settles the reading, and
`\uncertain{}` is preferred over guessing where it does not.

Each batch report SHALL additionally state how many regions it magnified — alongside the pages,
flags, notation decisions and trailing lines it already carries — so that a run which begins
magnifying freely once magnification is cheap is visible rather than silent.

#### Scenario: A doubtful glyph is magnified rather than guessed

- **WHEN** a subagent cannot resolve a glyph at the prepared page's resolution
- **THEN** it magnifies that region into its scratch directory rather than guessing, and flags `\uncertain{}` only if magnification does not settle it

#### Scenario: A page's regions are produced in one invocation

- **WHEN** a subagent needs more than one magnified region on the same page
- **THEN** it produces them all in a single invocation of the helper and reads them in a single turn

#### Scenario: A second call does not raise the per-page cap

- **WHEN** a subagent has already magnified the cap's worth of regions on a page and calls the helper again for that page
- **THEN** the helper refuses, rather than writing further crops or overwriting the ones already read

#### Scenario: Independent calls are issued together

- **WHEN** a batch subagent writes its fragments, or issues its magnification calls and crop reads
- **THEN** the calls that do not depend on one another are issued in a single message, because turns rather than tool calls are what re-send the fixed payload

#### Scenario: Escalation stays bounded

- **WHEN** a page would need more magnified regions than the cap allows
- **THEN** the subagent stops magnifying and flags the remaining doubtful passages instead

#### Scenario: Magnification volume is reported

- **WHEN** a batch subagent returns its report
- **THEN** the report states the number of magnified regions it used

### Requirement: Prepared pages carry a coordinate mapping back to the scan

The page-preparation helper SHALL emit, alongside the prepared images, a machine-readable mapping
from each prepared image's coordinate space back to its source scan — an offset and a scale per
page, such that `source = offset + prepared / scale`.

A batch subagent sees the prepared image but must magnify out of the source scan, which is cropped
and downscaled differently on every page. Without the mapping it has to infer one: a measured batch
that did so landed two of its three magnification crops on the wrong lines, spending its entire
per-page escalation budget without settling anything.

Emitting the mapping is a property of the shared page-preparation helper and therefore applies
whichever skill prepares the pages. The clause below concerns `magnify.py`, and so governs **the
Claude Code skill at `.claude/skills/transcribe/`** only.

The mapping SHALL be applied by the magnification helper rather than by the subagent. The subagent
names regions in the coordinate space of the image it can actually see — the prepared page — and the
helper converts them and crops from the source scan. Coordinate arithmetic performed by hand in a
subagent is a repeat of a measured failure, so it is not merely discouraged but replaced.

#### Scenario: A subagent magnifies without converting coordinates

- **WHEN** a batch subagent needs to magnify a doubtful region
- **THEN** it names the region in prepared-image coordinates and the helper converts them and crops from the source scan

#### Scenario: The mapping is emitted with the prepared pages

- **WHEN** pages are prepared for transcription
- **THEN** an offset and a scale per page are written alongside the prepared images
