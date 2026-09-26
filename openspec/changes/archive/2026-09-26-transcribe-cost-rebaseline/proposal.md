## Why

The last two transcription changes optimized a cost curve — batch size `N`, then turns `t` — measured
in **raw token volume**, with output taken from logged usage. Both foundations turned out wrong on
2026-09-25 (evidence in `measurements.md`):

- **The plan meter weights by API price, not volume.** A 3M-token cache-read probe moved the 5-hour
  meter about as much as its API price predicts (+2 points), not what raw volume predicts (~+7).
- **Logged output is a stream-start snapshot.** A 42.7k-token reply is recorded as 4 output tokens,
  so `measure_session.py` has undercounted the most expensive token class in every measurement we
  have.

Re-scoring five past runs at API prices with reconstructed output reverses the picture the curve
was built on (figures as corrected by the finished instrument; the first prototype overstated
output — see `measurements.md`):

| | share of cost at Opus 5.5 prices |
|---|---|
| cache reads — the `t·(B+P)` term the curve optimizes | 14–32%, concentrated in a few long subagents |
| cache writes — of which subagent setup 5–7%, images 5–12% | 28–39% |
| output | **35–47%**, of which about two thirds is **thinking** (23–34% of cost) |

And the model changed underneath us: Opus 5.5 is 20% cheaper per token, 60% cheaper per cache read,
thinks at a different rate per effort level, and this app now runs it at effort `medium` where
Picard ran Opus 5 at `high`. Separately, Claude Code's `Read` caps images at a **2000px** long edge,
while the pipeline still sizes everything for 1568px.

So the question "should we remeasure the curve?" has a short answer — the curve (`N`) is a minor term
now — and a longer one: **we do not know what a transcription page costs on the model we actually
run, or which lever moves it.** This change finds out. **It deliberately decides no skill rules**:
what `.claude/skills/transcribe/` should dictate follows from the measurements and belongs to a
follow-up change, including the outcome "change nothing".

## What Changes

- **Fix the instrument.** `pipeline/measure_session.py` gains:
  - a **price-weighted** cost column from a per-model price table, alongside the existing raw-volume
    figure so older numbers stay comparable;
  - **reconstructed output** per turn (context growth minus the tool results fed in), replacing the
    logged snapshot, with thinking and visible output reported separately as an estimate;
  - **per-turn subagent data** read from `<session>/subagents/*.jsonl`, which Claude Code now
    persists — retiring the standing caveat that subagent cost is modelled from endpoints;
  - image tokens from the dimensions actually stored in the transcript, not the file on disk.
- **Re-score the runs we already have** — Picard (both sessions), Clebsch pp. 223–243, castelnuovo —
  at no cost, and read the proofread outlier (one text-only subagent, 33 turns, ~20% of the Picard
  run) before spending anything on new pages.
- **Measure on Opus 5.5**, on fresh pages, in isolation: effort `medium` against `low` first, because
  thinking is the largest term; image resolution 1568 against 2000 second, and only if the re-score
  shows image writes are a material share.
- Record everything in `measurements.md`, then write down which levers are worth a skill change.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `transcription-pipeline`: adds one requirement — transcription cost is measured at what it is
  billed for (price-weighted, reconstructed output, per-turn subagent data). No requirement about
  how the skill transcribes is added or changed here.

## Impact

- **Modified**: `pipeline/measure_session.py` and its tests under `pipeline/tests/`. Standard library
  only, as now; `pipeline/validate.py` and CI are untouched.
- **New**: `openspec/changes/transcribe-cost-rebaseline/measurements.md`.
- **Unchanged by this change**: `.claude/skills/transcribe/SKILL.md`, `prepare_pages.py`,
  `magnify.py`, the house style, the Antigravity skill. The resolution arm uses `prepare_pages.py
  --max-edge 2000`, which already exists.
- **Overlap with `transcribe-turn-cost`**: its open tasks 6.6 (verification batch size) and 7.x
  (verification on a cheaper tier) are measurements of the same kind, taken with the metric this
  change corrects. Proposed: land `transcribe-turn-cost` without them and carry them here — the
  contributor decides.
- **Spend**: the two effort arms on ~12 pages each are roughly $20 at API prices — about half a Pro
  5-hour window. Re-scoring costs nothing.
