## Context

`proposal.md` has the motivation and `measurements.md` the evidence. The cost model the last two
changes optimized was

```
tokens/page ≈ s·(B+P)/N  +  t·(B+P)  +  t·m·N/2          (raw volume, logged output)
```

Priced honestly on Opus 5.5 it looks more like

```
$/page ≈ c_w·(image + text written once)  +  c_o·(visible output + THINKING)  +  c_r·t·(B+P + …)
          28–39%                              35–47%                             14–32%
          c_w = $5/MTok                       c_o = $20/MTok                     c_r = $0.20/MTok
```

— five runs re-scored (`measurements.md`), on Opus 5 tokens re-priced: the structure holds across
works; how Opus 5.5 itself behaves is what the new runs test.

## Goals / Non-Goals

**Goals:**

- A `measure_session.py` whose headline figure is what a run is billed for, validated against probes
  with known answers.
- The price-weighted cost structure of every run we already have transcripts for.
- Cost per page and quality on **Opus 5.5 at the effort this app actually runs**, and at one lower
  effort, on the same pages.
- A written list of which levers earn a skill change, with numbers.

**Non-Goals:**

- **Deciding skill rules.** No edits to `.claude/skills/transcribe/`, `prepare_pages.py` defaults or
  `magnify.py` in this change. The follow-up change writes them, from these numbers.
- Re-fitting batch size `N`. The re-score put subagent setup at 5–7% of cost, and the 14–32% of
  reads sits in a few long subagents, not in batch count. A perfect `N` is worth a few percent.
- The Antigravity skill (`.agents/skills/transcribe/`), whose economics are separate by design.
- Measuring the subscription meter precisely. The probe settled the question that matters (price-
  weighted, not volume-weighted); a finer ratio would cost a large share of a window per point.

## Decisions

### D1. Headline metric: API list price of the model that ran

The plan meter is not observable per token (`get_usage` reports whole percent of a 5-hour window).
The 2026-09-25 probe pair found both an output-heavy and a cache-read-heavy window at ~$0.43 per
meter point, so API list price is a good proxy for what a contributor's plan is charged, and it is
the actual bill for anyone on an API key. The price table is per model; cache writes are priced by
TTL (the transcript's `cache_creation` split says which).

Raw volume stays as a second column. The archived 4.2M/page and 509k/page figures are raw volume,
and a comparison must say which metric it is on.

### D2. Output is reconstructed, not read

Per turn: `output_i ≈ ctx_{i+1} − ctx_i − tool_results_i`, with image tool results at `w·h/750` from
the image as stored in the transcript and text at a chars-per-token estimate. The final turn of a
subagent has no successor; use its visible content as a floor.

Validated on 2026-09-25: probe B (known ≈42.7k output) reconstructs to 42.8k; probe A (60 near-empty
turns) to ~100 tokens/turn.

*As built (2026-09-26):* the text estimate matters more than this section first assumed, because it
enters twice — as the visible floor and as the fed-in tool results subtracted from the growth. It is
**1.9 chars/token** for corpus LaTeX, measured by a verbatim-copy subagent and confirmed on 285
historical turns whose logged count is final (aggregate error < 4%; at the 3.5 first assumed, +24–
36%). Where a logged count is at least half the estimate it is taken as final. Two further transcript
defects surfaced while building this and are corrected: rows repeat a message's `usage` once per
content block, and `<synthetic>` placeholder rows carry zero usage. Thinking comes out at about two
thirds of output, not the 80–90% first estimated.

### D3. Re-score before running anything

Every lever below is chosen by the re-score, not by this design. Order of the experiment follows
from which term is largest across Picard, Clebsch and castelnuovo: if output dominates everywhere,
effort goes first; if image writes rival it, resolution does. The proofread outlier is read, not
re-run: its transcript says whether 33 turns was real work or a loop.

### D4. The effort arms: same pages, isolated, adjudicated against the scan

- **Arm M**: Opus 5.5, effort `medium`, the current skill unchanged. The new baseline.
- **Arm L**: Opus 5.5, effort `low`, same pages, same skill.
- **Pages**: an untranscribed range on a work with a one-image-per-page scan (`prepare_pages.py`
  warns on few pages), ~12 pages = 3 batches per arm. Picard is fully transcribed and cannot serve.
- **Isolation**: each arm runs in a sandbox holding the scans, style files and glossary only — no
  `original.tex`, no fragments from the other arm. The archived A/B produced a byte-identical,
  "validating" result by reading the answer; byte-identical output between arms is a failed
  measurement, not agreement.
- **Quality**: diff the two outputs; adjudicate every difference against the scan. `houselint`
  passing is not evidence of faithfulness.
- **Kill criterion**: if arm L gets wrong any reading arm M gets right, `low` is not adopted for that
  pass. Transcription and verification are judged separately — they may land on different effort.

### D5. The resolution arm is conditional, and capped at 2000

Only run if D3 shows image writes are a material share. `Read` re-encodes images over 2000px as JPEG,
which on bilevel scans adds ringing at glyph edges — precisely where magnification looks — so the arm
uses `--max-edge 2000`, never above. Measure: magnified regions per page, turns, cost, and the same
adjudicated quality comparison as D4.

## Risks / Trade-offs

- **One run per arm.** Batch-to-batch variance in the Picard run was 3× in turns (batching
  discipline). Report per-batch figures, not only means, and treat a difference smaller than the
  spread as no difference.
- **Effort is set per session, not per subagent.** If subagents inherit the parent's effort, each arm
  needs its own session started at that effort; confirm how `CLAUDE_EFFORT` reaches subagents before
  trusting the arm labels, and record the effort per subagent from its transcript where visible.
- **Prices are list prices at launch.** Opus 5.5 cache-write prices are derived from the standard
  multipliers; re-check before quoting dollar figures externally.
