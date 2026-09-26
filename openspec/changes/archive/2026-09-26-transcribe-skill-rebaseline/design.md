## Context

The evidence is `openspec/changes/transcribe-cost-rebaseline/measurements.md`, sections "Effort A/B
on Opus 5.5", "Batch size", and "Levers (task 4.2)". In short, on Picard 1885 pp. 321–332, all on
Opus 5.5, verified, every substantive difference adjudicated against the source scan:

| arm | $/page | readings wrong | paragraph breaks wrong |
|---|---|---|---|
| N=4, `medium` | 0.41 | 0 | 2 |
| N=12, `medium` | 0.37 | 0 | 1 |
| N=28, `medium` | 0.32 | 1 | 8 |
| N=4, `low` | 0.27 | 5 substantive defects (kill criterion) | — |
| Opus 5 `high` reference | — | 2 | 5 |

One run per arm. The differences in readings are few and partly verifier variance; the paragraph
pattern is systematic (per-page rates constant across a run's context). This change applies the
levers the measurement change decided; it does not re-open them.

`transcribe-turn-cost` is unarchived and edits the same skill text (Phase 3 magnification, Phase 5
ordering and concurrency) and three requirements. This change lands after it.

## Goals / Non-Goals

**Goals:**

- Transcription at 12 pages per batch, with the rationale in the skill replaced by what was measured.
- Verification decoupled from transcription batch size, at 4 pages, concurrent.
- A stated recommended effort, with the measured reason.
- Paragraph breaks at displays checked by the pass that can see the page.
- A magnification cap that holds against the caller.

**Non-Goals:**

- **Crop targeting.** The model's region coordinates land 40–150px off; `magnify.py` crops exactly
  where told (checked at shift 0). A fix — padding, or a coordinate grid on prepared pages — needs
  its own measurement.
- **A shipped proofread checker.** ~19% of a Picard run went into a proofread re-deriving its own
  check scripts. Worth doing; a different change.
- **Resolution.** Images are 5–12% of cost; the 1568px sizing stays although Claude Code delivers up
  to 2000px. Measured as not worth it for cost; not measured for quality.
- **Whole-work batches.** N=28 was tested and not adopted. Not re-litigated here.
- The Antigravity skill; the Tier-3 pipeline; the corpus corrections to Picard 1885.

## Decisions

### D1. Transcription batch: 12 pages, snapped to a nearby structural boundary

Default 12. When a chapter, part, or numbered-article boundary falls within about three pages of the
12-page mark, the batch ends there instead, so a batch holds whole units where the print offers them
and the batch join falls where the text itself breaks. No batch exceeds ~15 pages: the N=28 run is
the only evidence above 12, and it was worse.

Rationale kept in the skill, replacing "measured optimum 2–4, curve flat": per-batch turns are ~6
whatever the page count, because the four-message shape (read all, magnify once, read crops, write
all) does not scale with N; the fixed part per batch is ~$0.11 warm ($0.23 for a run's first batch,
which writes the shared prefix); so larger batches are cheaper, and the limit is quality — one agent's
habit reaches every page of its batch.

*Considered:* keeping 4 (no measured quality gain from it, 10% dearer); whole chapters of any length
(N=28 evidence against); "as many as fit" (no bound on the habit's reach).

### D2. The short-work threshold stays absolute

The inline threshold is written today as "about two batches". At N=12 that would silently move from
~8 to ~24 pages transcribed inline, with scan images accumulating in the orchestrating session — the
failure the subagent architecture exists to prevent. The threshold is restated as about 8 pages.

### D3. Verification batch: 4 pages, concurrent, stated as its own decision

The skill currently says verification's batch size is "inherited from transcription rather than
measured". With transcription at 12 that inheritance would triple verifier size silently. Verification
stays at 4 pages: its subagents run concurrently, so smaller batches shorten wall-clock, and four
adjacent pages still let a verifier compare a doubtful glyph against a clearer instance. A 12-page
transcription batch is verified by three 4-page verifiers. Verification cost per page was flat
across arms ($0.22–0.24), so this costs nothing measurable.

### D4. Effort: `medium` recommended, not enforced

A skill cannot set its session's effort (and a session cannot change its own effort). The skill
states the recommendation up front, with the evidence, tells the contributor how to check it
(`CLAUDE_EFFORT` in the environment, or the `effort` field on transcript rows), and Phase 6 already
records the effort actually used in provenance. `low` is named as measured and rejected, with the
reason that matters most: its verifier *introduced* errors.

### D5. Paragraph breaks at displays are checked by the verifiers

The proofread cannot settle these — it has no scan. The verifier prompt gains one explicit check: for
every paragraph break immediately before or after a display, look at whether the next text line is
indented (new paragraph) or flush left (continuation), correct the fragment, and list each change in
the discrepancy list. Worded as a rule about the print, not about this scan: indentation is the
signal, and a new sentence after a display is not by itself a new paragraph.

### D6. The magnification cap lives in a ledger beside the prepared pages

`magnify.py` writes `magnify-ledger.json` in the `--prepared` directory, recording crops per page and
per pass (`--pass transcribe|verify`, default `transcribe`). The cap applies to (page, pass) whatever
`--out` is. `--cap` may lower the cap but not raise it above the default. The two loopholes this
closes were both observed or present: a fresh `--out` (used by a verifier to take 7 regions on one
page) and `--cap` (available to any caller).

The pass is still the caller's word. That is the honest limit of enforcement inside a tool the model
invokes; the prompt names the pass, and the ledger makes a caller that lies about it visible
afterwards, which the per-directory count did not.

## Risks / Trade-offs

- **One run per arm.** The batch decision rests on N=12 being at least as good as N=4 on twelve pages
  of one work. Mitigation: the next real transcription under this change is measured with
  `measure_session.py` and its verification discrepancy lists reviewed; revert to 4 if quality drops.
- **Larger batches concentrate a bad habit.** One agent's convention reaches 12 pages instead of 4.
  Mitigation: D5 targets the habit actually observed; the glossary still carries decisions forward.
- **Snapping to boundaries needs structure the orchestrator can see.** It does not read scans. It
  knows chapter and article boundaries only from earlier batches' reports and the glossary; for the
  first batch it uses 12. Acceptable: snapping is a preference, not a requirement.
- **Ledger in the prepared directory.** A contributor re-running a range keeps the old ledger and
  finds the cap spent. `prepare_pages.py` reuses the directory (`makedirs(exist_ok=True)`), so it
  must clear the ledger entries for the pages it prepares — re-preparing a page is a fresh start — and
  the cap-exceeded message names the ledger.
