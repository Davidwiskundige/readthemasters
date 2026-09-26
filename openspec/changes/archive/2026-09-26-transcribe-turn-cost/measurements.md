# Measurements

Reproduce any row with `python pipeline/measure_session.py`.

## Baseline this change is measured against (task 1.2)

From `openspec/changes/archive/2026-09-02-transcribe-per-batch-subagents/measurements.md`, the
post-per-batch-subagents state. `clebsch-1864-anwendung-abelschen-functionen` pp. 223–243, 21 pages,
five batches, transcribed 2026-09-01.

| metric | value |
|---|---|
| tokens/page, transcription | **509k** |
| tokens/page, transcription + verification | **~1.0M** |
| turns per page, transcription (`t`) | **5.7** |
| turns per page, verification | **~4.9** |
| magnified regions per page | **1.7** (36 across 21 pages) |
| fixed cost per subagent (`B+P`) | 62.7k |
| marginal cost per page (`m`) | 7.25k |
| batch round-trips, transcription | 5, serial |
| batch round-trips, verification | serial, one per batch |
| proofread | once, **after** the verifiers |

The dominant term is `t·(B+P)` — turns times the fixed payload re-sent every turn — at ~212k of the
509k at N=5. This change targets `t` (design D1) and the serial verification round-trips (D2, D3).

**Target:** `t` near 3.3 for transcription, verification round-trips collapsing from one-per-batch
to one, and each page's scan read once rather than twice.

## Measurement method is unchanged (task 1.3)

Verified against `pipeline/measure_session.py` as it stands today:

- `turn_context()` sums `input_tokens + cache_read_input_tokens + cache_creation_input_tokens`.
- `report()` computes `grand = sum(totals.values())` over `in`, `out`, `cw`, `cr`.

So the reported total is **fresh input + output + cache writes + cache reads** — raw context volume,
not cost-weighted. That is the same quantity the 4.2M/page and 509k/page figures were computed from,
so the comparison stays like-for-like.

**Caveat, carried forward unchanged:** subagent transcripts are not persisted, so per-turn context
inside a subagent is not observable. Per-page cumulative figures are modelled as
`turns × mean context` with `mean = (B+P + end)/2`; only the endpoints (`reported tokens`, `tool
calls`) are measured. Any new figure below inherits that caveat.

## A second orchestrator data point, measured 2026-09-12 (unplanned)

`castelnuovo-enriques-1897-surfaces-algebriques` pp. 241–316 was transcribed on 2026-09-07 in a
separate session under the **pre-change** skill. Its transcript is measurable, so it is recorded
here as a second reading of the architecture this change modifies.

`python pipeline/measure_session.py f815a075-0f0f-406e-a62e-2168d7520554 --pages 76`:

| metric | value |
|---|---|
| turns | 353 |
| mean context/turn | 203k |
| peak context | 350k |
| total tokens | 72.1M |
| **images read** | **4 (5k tokens)** |
| full-context rewrites | 6 (1.7% of turns) |
| orchestration per page | 948k |

Two things it settles:

- **The central claim of the per-batch-subagent design holds at 76-page scale.** Four images entered
  the orchestrator across the whole work — the top half of p241, read to take the title off the
  print — against 5.7k pages' worth of scans handled by subagents.
- **The orchestrator is still not cheap**, and this is now measured on a clean single-work run rather
  than inferred from a session that was doing three things at once. 948k/page of orchestration, with
  images at 5.7% of residency and `result: Bash` at 26.4%. The archived change said removing scans
  from the orchestrator did not by itself make the orchestrator small; at 76 pages that is
  quantified. **This is not a term `transcribe-turn-cost` addresses** — D1 through D5 all act on
  subagents — and it is the obvious candidate for whatever comes next.

*Caveat:* subagent transcripts are still not persisted, so this is orchestration only. It is not
comparable to the 509k/page figure, which is subagent cost.

## Implementation measurements

`pipeline/magnify.py` and its tests: 33 tests, all passing.
`python -m pytest pipeline/tests -q` → **243 passed** (2026-09-12).
`python pipeline/validate.py` → **17 works pass the copyright gate**.

*History, because it was reported once as a failure:* on 2026-09-07 the suite showed 242 passed / 1
failed, `test_validate.py::test_real_corpus_passes_gate`, because
`corpus/castelnuovo-enriques-1897-surfaces-algebriques/` was then a half-started work with no
`provenance.yaml`. That was never caused by this change, and it cleared when the separate session
transcribing that work finished it.

`verification.model` in `provenance.yaml` was checked against the live gate by adding it to
`corpus/betti-1871-spazi-numero-qualunque-dimensioni/provenance.yaml` and running
`pipeline/validate.py`: no complaint. `check_provenance()` places no allowed-key restriction on the
`verification` block. The probe edit was reverted — the field asserts which tier verified that work,
and that is not known.

## The measurement target (task 1.1), qualified 2026-09-12

**Picard 1885**, *Sur les intégrales de différentielles totales algébriques de première espèce*,
Journal de mathématiques pures et appliquées, pp. 281–346. Measurement range **pp. 281–300**, five
batches. Source: a NUMDAM facsimile PDF, 3308×4678 bilevel TIFF per page, A4 (aspect 1:1.41).

`python pipeline/prepare_pages.py --pages 281-346`, all 66 pages:

| | Clebsch pp. 223–243 (baseline) | castelnuovo (rejected) | **Picard 281–346** |
|---|---|---|---|
| text width after the cap | 1180px | 895–1064px | 977–**1015 median**–1277px |
| pages under the 1000px threshold | 0 | 72 of 76 (95%) | **9 of 66 (14%)** |
| text-block detection failures | — | 12 short + 17 narrow | **0** |
| source resolution | 1400×1859 | — | **3308×4678** |
| method this forces | one image/page | half-page crops | **one image/page** |

**Why it qualifies where castelnuovo did not.** At 14% warned the run stays one image per page, so
`t` is measured against the same method the 509k/page and `t = 5.7` figures came from. castelnuovo
at 95% warned was forced into half-page crops — two images and an extra turn per page — which is the
confound that disqualified it.

**The caveat, stated up front.** At a 1015px median Picard is ~14% narrower than Clebsch, so it will
probably want more than Clebsch's 1.7 magnified regions per page. That is a property of the scan,
not of the method, and it makes this a *harder* test of D1. So the primary result must be computed
**internally** — measured `t` against the `t` the same run would have had at 2 turns per region
under per-region cropping — with the Clebsch comparison reported second and caveated. Against that,
the source is 2.4× Clebsch's linear resolution, so each crop buys back far more.

## Run measurements — Picard pp. 281–300, 2026-09-12

### The headline finding is about the metric, not the result

**`t = 5.7` was never a turn count.** The archived change computed it as `tool calls + 1`, which
assumes one tool call per turn. D1 breaks that assumption by design: its whole point is issuing
independent calls together in one message. Measured directly, the two diverge by up to 3× on the
same batch. Every comparison below therefore reports both, and the Clebsch figure is treated as a
tool-call count, which is what it is.

### Transcription, five batches of four pages

| batch | pages | reported tokens | tool calls | **turns** | magnified regions |
|---|---|---|---|---|---|
| 1 | 281–284 | 115.7k | 26 | **12** | 12 |
| 2 | 285–288 | 106.7k | 24 | 5 | 12 |
| 3 | 289–292 | 116.1k | 24 | **4** | 12 |
| 4 | 293–296 | 103.9k | 24 | **4** | 12 |
| 5 | 297–300 | 112.5k | 24 | **4** | 12 |
| **total** | **20** | **554.9k** | **122** | **29** | **60** |

Per page: **27.7k reported tokens**, 6.1 tool calls, **1.45 turns**, **3.0 magnified regions**.
Excluding batch 1, which is the outlier: **1.06 turns/page**.

### The saving, computed internally

This is the primary result, because it does not depend on the Clebsch comparison. Under per-region
cropping — one compute-and-save turn plus one read turn per region, which is what the pre-change
skill produced — the run's 60 regions would have cost **120 turns** for magnification alone.
Measured, they cost **12**: batches 2–5 spent two turns each (one chained Bash, one multi-crop read)
for 48 regions, and batch 1 spent four for 12.

> **108 turns saved across 20 pages — 5.4 turns per page.**

### Against Clebsch, on the metric Clebsch was measured with

| | Clebsch pp. 223–243 | Picard pp. 281–300 |
|---|---|---|
| tool calls per page | 5.7 | 6.1 |
| magnified regions per page | 1.7 | **3.0** |
| reported tokens per page | ~26.5k | 27.7k |

Picard costs **the same per page while doing 76% more magnification**. That is the change working:
the extra escalation the narrower scan demanded was absorbed at no cost. On tool calls alone Picard
looks 7% worse, which is exactly why the metric had to be fixed.

### Batching discipline dominates, and it is a prompt property

| batch | turns | difference |
|---|---|---|
| 1 | 12 | wrote its four fragments in four separate messages; two greps in their own messages |
| 2 | 5 | chained the magnify calls; read all crops in one message |
| 3–5 | 4 | as 2, plus all four `Write` calls in one message |

Same helper, same scan, same page count — **3× apart**. Batch 1 had `magnify.py` and still cost 12
turns. D1 supplies the capability; the prompt decides whether it is used. The skill told subagents
to batch *crop reads* and said nothing about anything else, which is now fixed in Phase 3 with this
table as the argument.

### Verification, five concurrent subagents (D2, D3)

| batch | tool calls | turns |
|---|---|---|
| 281–284 | 24 | 9 |
| 285–288 | 32 | 8 |
| 289–292 | 30 | 10 |
| 293–296 | 40 | 14 |
| 297–300 | 30 | 10 |
| **total** | **156** | **51** |

Dispatched concurrently in one message: **5 serial round-trips became 1**. Verification is
noticeably less batched than transcription (51 turns against 29 for the same pages) because its work
is genuinely iterative — a routed question leads to a crop, which leads to another question.

### D3 (proofread first) — what the routing actually bought

The proofread produced **24 `needs scan` findings across 13 pages**, handed to the verifier holding
each page. Had it run after the verifiers, every one would have needed a further subagent re-reading
scans just put down.

More useful than the count is the hit rate. Of the scan-dependent findings, verifiers **confirmed the
transcription** on p. 283 (`CHAPITRE I` genuinely absent), p. 285 (the circularity and the tag),
p. 288 (`questions`, `homogenes`), p. 289 (`nº 1` — the blob is 1:2.9, far too narrow for this
face's `2`), p. 291 (`z = c`, and `passer par` not `parallèle à`), pp. 293–295 (punctuation, the
letter `P`, the wide `x`); and **overturned it** on four: p. 284's inner sign and missing terminal
period, p. 296's `nº 5` → `nº 3`, p. 300's period → comma.

**A proofread inference is not evidence about the print.** On these pages it was wrong about as
often as it was right, which is precisely the D3 argument for routing its findings to the pass that
can see the page rather than acting on them directly.

### Quality outcome

- `houselint`: clean on every batch as it landed, and on the assembled file.
- Mechanical checks: 20 contiguous `\origpage`, 103 matched display pairs, even `$` parity, balanced
  braces, no hyphen before a page break.
- `pipeline/validate.py`: 18 works pass the gate. `pytest`: 250 passed.
- **Uncertainty flags: 0** — two were raised in transcription and both were *resolved* by the
  verification pass. The zero records doubts settled, not doubts never raised; provenance says so
  explicitly.

### Two defects the run found in this change's own work

1. **The cap was per invocation, not per page.** Batch 1 took "3 + 1 follow-up" regions on p. 281 —
   inside the cap twice, past it in total — and silently overwrote its own first crop, because
   output names restart at `r1` each call. Both holes closed by counting crops already on disk;
   5 regression tests added (38 total in `test_magnify.py`).
2. **My own stitching put a blank line before every `\origpage`**, so all twelve mid-sentence page
   joins rendered as spurious new paragraphs. Caught by the proofread, which tested it against the
   compiled PDF and against `abel-1841` (88 of 89 markers without it). Fixed in Phase 4.

### Orchestrator

Images read by the orchestrating session: **0**. The design's central claim held for a third work.
