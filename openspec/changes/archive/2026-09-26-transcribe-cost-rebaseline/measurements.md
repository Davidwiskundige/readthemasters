# Measurements

## What we found before anything was built (2026-09-25, exploration session on Opus 5.5)

### Claude Code's `Read` caps images at 2000px long edge

Probe images read, then decoded from the session transcript to see what reached the model:

| file sent | what the model received | tokens (cache-write delta) |
|---|---|---|
| 1800×2576 PNG | **1398×2000 JPEG** | ~3.7k |
| 2400×3400 PNG | **1412×2000 JPEG** | ~3.8k |
| 1100×1568 PNG | 1100×1568 PNG, untouched | ~2.3k |

A long-edge cap, not a megapixel cap (8.2MP input landed at 2.8MP). Cost stays `w·h/750`. Images
over the cap are re-encoded as **JPEG** — on bilevel scans that means ringing at glyph edges, so
anything this pipeline sends should be pre-sized to ≤2000px. The model itself accepts 2576px on Opus
4.7+; Claude Code does not deliver it. `prepare_pages.py`, `magnify.py` and `measure_session.py`
still hardcode 1568.

For Picard's text block (median 1015px wide at 1568): ~1295px wide at 2000, for ~+1.4k image tokens
per page.

### Transcripts log output at stream start, not at the end

Probe B produced 6000 lines (63.4KB) in one message. Logged `output_tokens` for it: **4**. The next
turn's context grew by **42.7k**. Every row of a message carries the same snapshot, so taking the
last row does not help. `measure_session.py` has undercounted output in every figure recorded to
date; reconstruction from context growth is the only available source.

### Subagent transcripts are persisted

`~/.claude/projects/<project>/<session>/subagents/agent-*.jsonl` (+ `.meta.json` with the
description), with per-turn usage. The standing caveat "subagent transcripts are not persisted, so
per-page figures are modelled from endpoints" no longer holds, including retroactively for runs
since at least 2026-09-07.

### The plan meter weights usage by API price, not raw volume

`get_usage` exposes only whole percent of the 5-hour and weekly windows (Pro plan). Two windows,
nothing else running on the account:

| window | contents | raw tokens | API-price equivalent | 5-hour meter |
|---|---|---|---|---|
| output probes | two output subagents (~46k real output) + parent turns | ~2.6M | ~$2.1 | 5 → 10 (+5) |
| cache-read probe | 62 turns, 2.97M cache reads, 16k writes, near-zero output + parent turns | ~3.7M | ~$0.9 | 10 → 12 (+2) |

Raw-volume weighting calibrated on the first window predicts ~+7 for the second; price weighting
predicts ~+2; "cache reads free" predicts <1. Observed +2. **Price weighting, moderate confidence**:
one pair, ±1 rounding at each reading, parent-session turns in both windows. Implied scale: about
**$43 of API-price usage per Pro 5-hour window**.

### Picard pp. 281–300 re-scored with the prototype (SUPERSEDED — see "Instrument" and "Re-score" below)

> **These figures are wrong and kept only as the record of what motivated this change.** The
> prototype counted `<synthetic>` placeholder rows as turns (their zero usage broke the context
> series), and used 3.5 chars/token where corpus LaTeX runs at 1.9. Corrected: output ~330k not
> ~479k, thinking ~222k not ~420k, output 47% of cost at Opus 5.5 prices not 56%. The 130k
> "outlier" batch was the synthetic-row artifact.

(session `4912ad8e`, Opus 5, effort `high` per provenance)

Throwaway script (scratchpad `rescore.py`, the prototype for tasks 1.1–1.3). Output reconstructed
as context growth minus tool results; the reconstruction reproduced probe B's known 42.7k as 42.8k.

| component | tokens | Opus 5 prices | share | re-priced at Opus 5.5 | share |
|---|---|---|---|---|---|
| cache reads | 11.02M | $5.51 | 23% | $2.20 | 13% |
| cache writes (5-minute TTL) | 1.06M | $6.59 | 27% | $5.30 | 31% |
| output (reconstructed) | ~479k | $11.98 | 50% | $9.58 | 56% |
| &nbsp;&nbsp;of which visible (≈3.5 chars/token) | ~60k | | | | |
| &nbsp;&nbsp;of which thinking | ~420k | | | | |
| **total** | 12.55M raw | **$24.09** — $1.20/page | | **$17.07** — $0.85/page | |

By pass: transcription $11.76, verification $7.56, **proofread $4.77** (one text-only subagent, 33
turns, ~82k output).

Picard pp. 301–346 (`50b4018c`, 27 subagents): output 55%, cache writes 27%, cache reads 18%, $69.30
at Opus 5 prices ($50.34 re-priced). Same shape.

**Caveats.** The visible/thinking split rests on an uncalibrated chars-per-token ratio; thinking is
somewhere around 80–90% of output. Batch 289–292 reconstructs to 130k output in 6 turns — a long
reasoning session or an estimation miss on its crops; worth ~10% of the total either way. These are
Opus 5 tokens re-priced, not Opus 5.5 behaviour.

### Effort

Picard's `provenance.yaml` records `effort: high`. This app's sessions now run with
`CLAUDE_EFFORT=medium`, the Opus 5.5 API default. A new baseline therefore differs from Picard in
model **and** effort; only a new run separates them.

## Instrument (tasks 1.1–1.6, 2026-09-26)

`pipeline/measure_session.py` now prints, for a session and for each subagent under
`<session>/subagents/`, cache reads / writes (by TTL) / fresh input / reconstructed output, priced
per model, with shares, per-page figures and the raw-volume total. `--price-as MODEL` re-prices a
run's tokens; `--only TEXT` filters subagents by description (for sessions that did several works).

Three transcript defects are corrected, not just the one we went in for:

| defect | effect on every earlier figure | fix |
|---|---|---|
| one row per content block, each repeating `usage` | turns and token totals inflated 2–3× wherever rows were summed | a turn is a distinct message id |
| `output_tokens` is a stream-start snapshot in current Claude Code (older versions logged the final count on some turns) | output undercounted, up to 10,000× on a long reply | reconstruct: next turn's context growth minus what was fed in; use a logged count when it is ≥ half the estimate |
| `<synthetic>` placeholder rows (after interrupts) carry zero usage | break the context series; growth attributed to a non-call | skipped |

**Calibration of chars/token (task 1.5).** Two independent measurements agree:

- A subagent copied 11,996 chars of Picard LaTeX verbatim (byte-identical, checked with `cmp`): the
  write turn grew the context by 6,753 tokens including a 240-char tool result → **~1.9 chars/token**
  (12,804 JSON chars). The fragment-write turns of the Picard run give a lower bound of 1.83.
- On the **285 turns** (Picard, both sessions) whose logged count looks final, the reconstruction
  matches the log within **3.7–3.8% in aggregate, median +1.5–2.5%** at 1.9. At the old 4 it
  overestimated by 35–56%; at 3, by 24–36%.

`CHARS_PER_TOKEN = 1.9`. English-prose tool results run nearer 4, so they are overcounted as fed-in,
which biases output slightly low; the 285-turn check bounds the net effect.

Tests: 24 in `test_measure_session.py` (reconstruction against a known answer, logged-final vs
snapshot, TTL pricing, de-duplication, synthetic rows, unpriced models, subagent discovery).
`python -m pytest pipeline/tests -q` → **290 passed, 1 skipped**; `python pipeline/validate.py` →
**30 works pass the gate**.

## Re-score (tasks 2.1–2.2, 2026-09-26)

Reproduce with `python pipeline/measure_session.py <session>.jsonl --pages N [--price-as
claude-opus-5-5] [--only TEXT]`, sessions under the main checkout's transcript directory. All five
runs were Opus 5; the right-hand block re-prices the same tokens at Opus 5.5 — structure, not 5.5
behaviour.

| run | session | pages | $/page Opus 5 | **$/page at 5.5** | reads | writes | output | thinking (est.) |
|---|---|---|---|---|---|---|---|---|
| Picard 281–300 | `4912ad8e` | 20 | 1.02 | **0.70** | 16% | 38% | 47% | ~2/3 of output |
| Picard 301–346 | `50b4018c` | 46 | 1.16 | **0.81** | 14% | 39% | 47% | ~3/4 |
| Clebsch 223–243 (transcribe + verify only) | `edaf63a8 --only "Clebsch pp.2"` | 21 | 0.89 | **0.60** | 20% | 34% | 46% | ~2/3 |
| castelnuovo 241–316 | `f815a075` | 76 | 1.22 | **0.76** | 29% | 36% | 35% | ~2/3 |
| Betti 140–158 | `4f364d40` | 19 | 2.32 | **1.40** | 32% | 28% | 39% | ~2/3 |

Shares are of the Opus 5.5 re-priced cost. The shares hold across five works and three shapes of
run; per-page cost varies 2.3×, and the expensive runs are the ones with long subagents (below).

**What the writes are.** The obvious suspects are small:

| run | subagent setup written (first turn) | images written |
|---|---|---|
| Picard 281–300 | 6% of cost | 7% |
| Picard 301–346 | 6% | 5% |
| Clebsch 223–243 | 5% | 6% |
| castelnuovo | 5% | 12% (half-page crops) |
| Betti | 7% | 6% |

Most of each subagent's ~45k setup is *read* from a sibling's cache, not rewritten. The rest of the
writes is output being cached on the next turn (output is paid twice: once as output, once as a
write) and text tool results.

**Where the reads are.** Concentrated in a few long subagents, not spread over batches:

| run | largest read consumers |
|---|---|
| Picard 281–300 | proofread 33 turns — **36%** of reads; one verifier 15 turns 12% |
| Picard 301–346 | proofread 51 turns — **28%** |
| Clebsch 223–243 | verifiers 49 and 26 turns — 35% and 19% |
| castelnuovo | whole-text proofreads 76 and 39 turns — 14% and 6% |
| Betti | two transcribers at 41 and 39 turns — 9% and 8% |

## The proofread (task 2.3)

Picard 281–300's proofread: **$2.64 of $14.08 at 5.5 prices (19% of the run)**, 33 turns. It was
real work — its findings were used — but about 25 of the 33 turns built tooling rather than read
the text: a mechanical-check script (`\origpage` continuity, `$` parity, display pairs), a
glossary-conformance script, a KaTeX render test, and exploring `houselint`, `site/src/lib/tex.js`
and other works to learn the conventions those scripts check. Every proofread rebuilds this from
nothing. Picard 301–346's proofread ran 51 turns.

## Experiment order (task 2.4)

| lever | share of cost at 5.5 | verdict |
|---|---|---|
| **thinking (effort)** | 23–34% (castelnuovo lowest, Picard 301–346 highest) | **first experiment**: largest single term, one setting |
| **proofread tooling** | ~19% of a run in one pass, mostly re-derivation | **no page experiment needed** — measurable by re-running a proofread on already-assembled text with a shipped checker; candidate for the follow-up change |
| long-subagent turns (verify, proofread) | most of the 14–32% reads | follows from the two above |
| image resolution | images 5–12% of cost | **design D5's condition is not met** — not run here. 2000px would add ~1.65× image tokens, i.e. +3–8% cost, against fewer crop turns; that is a quality/turns question, not a cost one |
| batch size `N` | setup 5–7% | **not reinstated.** Price weighting makes a new subagent's setup a write (25× a read), so if anything larger `N` is favoured — but at 5–7% there is little to win either way |

## Effort A/B on Opus 5.5 (tasks 3.1–3.6, 2026-09-26)

### Setup

- **Pages (3.1).** Picard 1885 pp. 321–332, re-transcribed in a sandbox (option B: a reference transcription exists — Opus 5, effort `high`, verified). No corpus work has untranscribed pages (survey of all 30 works), and `scratch/poincare-1910` is complete. NUMDAM PDF re-downloaded (2.7 MB, 67 pp.), embedded scans 3308×4678 extracted; `prepare_pages.py` warns on 1 of the 12 pages (p. 325, 988px), the same regime as the original run.
- **Effort (3.2).** Every transcript row carries `"effort": ...`; subagents inherit the session's. A session cannot change its own effort (`set_session_effort` refuses); the contributor switched it for arm L. Audited: every row of every arm-M subagent says `medium`, every arm-L row `low`.
- **Sandbox (3.3).** Scans, prepared pages, rules, `magnify.py`, and the glossary **truncated to its state before p. 321** — the corpus `notation.md` holds entries written *after* batches covering these very pages (e.g. `\tag{I}` (p. 323)), which would have leaked answers. Each arm grew its own copy from its own batch reports, as the skill prescribes. Handoff: the reference's last 15 lines of p. 320, identical for both arms. Prompts character-identical between arms but for `armM`/`armL`.
- **Audit.** Every tool call of all 12 arm subagents: no access outside the sandbox (the only hits are Claude Code's own offloaded tool-result files). Arm M reproduces the reference on pp. 321 and 332 after whitespace normalization — legitimate for two plain-prose pages given the audit, but noted.
- **Scope.** Transcription (3 sequential batches of 4) + verification (3 concurrent verifiers) per arm. The proofread is excluded from both (its cost is a tooling question, see above).

### Cost (`measure_session.py --only "Arm M" / "Arm L" --pages 12`)

| | arm M (`medium`) | arm L (`low`) | L vs M |
|---|---|---|---|
| transcription, $/page | 0.185 | 0.145 | −22% |
| verification, $/page | 0.229 | 0.128 | −44% |
| **total, $/page** | **0.41** | **0.27** | **−34%** |
| output | 78k (thinking ~38k) | 42k (thinking ~12k) | −46% |
| magnified regions, transcription | 30 | 6 | |
| turns, verification | 48 | 28 | |

For scale: the Opus 5 `high` Picard run, re-priced at Opus 5.5 and without its proofread, was ~$0.57/page. **Model + effort `medium` already cuts that ~28%**, and thinking falls from ~2/3 of output (Opus 5 `high`) to ~1/2.

### Quality — adjudicated against the scan

Differences between the verified arms (57 word-level) are mostly an alignment convention (`&=` vs a leading `&`); the reference uses M's. Every substantive difference:

| page | arm M | arm L | print / verdict |
|---|---|---|---|
| 322/323 | *d'intersection.* opens p. 323 | at the end of p. 322 | p. 323's first line reads *…mentaires d'intersection.* — **L wrong** (transcriber) |
| 323 | `$f'_{z_{0}}$` | `\$f'_{z_{0}}$` | stray backslash, math breaks — **L defect** (introduced by L's verifier) |
| 324 | `s'assurer` | `\s'assurer` | undefined macro, compile error — **L defect** (L's verifier) |
| 324 | `\ednote{...}` plain | `\ednote{Sic; read \emph{...}}` | HOUSESTYLE R18 violation, caught by houselint — **L defect** (L's verifier) |
| 329 | correct | opens with the stray tail `mentaire` of p. 328's *complé-* | **L defect** (transcriber; L's verifier missed it) |

Arm M has no substantive error that arm L avoids. **Kill criterion (design D4) is met: `low` is not adopted** for either pass as run. Note the split: three of L's five defects were introduced by its *verifier* — a pass that should only remove errors — and L's verifiers magnified a third as much and ran 40% fewer turns.

### Where both arms beat the reference

Two readings where the Opus 5 `high` reference is wrong and **both** Opus 5.5 arms are right, checked at source resolution:

- **p. 323 `f'_{z_{0}}`** — the print has a broken `z` followed by the solid dot this scan makes of every subscript 0 (compare *(x₀, y₀, z₀)* one line above). The reference has `f'_{z}`.
- **p. 329 `3P`** — the first denominator prints an old-style **3** (open, two bowls, descending), side by side with the same page's clean `2P`. A printer's error, which R4 requires reproduced with an `\ednote`; the reference silently wrote `2P`. Arm L caught it at transcription, arm M at verification.

Both are corpus corrections to make in their own PR; this change does not touch the corpus.

### Tooling finding: crops land off target

5 of 10 crops in arm M batch 1 missed, and batch 3 reported crops 40–150px above the requested region. `magnify.py` is **not** at fault: cropping the same box from the prepared image matches its output at shift 0 (mean pixel difference 1.7, against ≥ 9.5 at any other shift). The model's coordinate estimates on the prepared image are off. Costs turns and regions against the cap; a candidate for the follow-up (padding, or a coordinate grid on prepared pages).

## Arm M against the Opus 5 `high` reference, fully adjudicated (2026-09-26)

Every difference between arm M (verified) and the reference that survives normalizing conventions (`&` placement, `\dots`/`\ldots`, spacing), each settled against the scan:

| | arm M (Opus 5.5 `medium`) wrong | reference (Opus 5 `high`) wrong |
|---|---|---|
| readings | none | **2**: `f'_{z}` for `f'_{z_{0}}` (p. 323); printed `3P` silently corrected to `2P` (p. 329) |
| paragraph breaks | **2**: none at the indented *On a, d'ailleurs* (p. 325); a spurious one at the flush-left *Par suite* (p. 331) | **5**: breaks at flush-left continuations after displays (pp. 321, 322, 323, 324 ×2) |
| punctuation | **1**: `0,` where the print has `0.` (p. 326) | **1, probable**: no terminal period after `\frac{dz}{C_{1}}` (p. 322; the mark is faint) |
| glossary conformance | none | **2**: `1ʳᵉ Partie` against the work's own `Iʳᵉ` rule (pp. 329, 331) |

Arm M additionally carries R4 notes the reference lacks (*représenté* p. 324, `f'_{z}` p. 326, `(y - y)` ×2 p. 327) — same text, annotated. Caveats: the reference also had a whole-work proofread, which the arms did not; and model and effort changed together, so this does not show what Opus 5.5 at `high` would do.

## Batch size: N=12 against N=4 (2026-09-26)

Question raised at review: N=4 was chosen for cost; if batch size no longer matters for cost, does a larger batch buy quality? One further arm on the same pages, same sandbox, same starting glossary, same prompt, effort `medium`, **one transcription subagent for all 12 pages**; verification kept at three concurrent verifiers of 4 pages. Audit clean (the one hit is a false positive in handback text; the transcriber's reference to "p. 306" comes from the glossary, line 238).

**Cost.** Per transcription batch at N=4, turns are ~6 regardless of pages (the four-message shape does not scale with N) and the fixed part is ~$0.11 warm ($0.23 for a run's first batch, which writes the shared prefix). Measured:

| | N=4 (arm M) | N=12 |
|---|---|---|
| transcription | $2.22, 18 turns | **$1.56, 7 turns** (−30%) |
| verification (N=4, concurrent) | $2.75 | $2.86 |
| **total, $/page** | 0.41 | **0.37** (−10%) |

**Quality**, N=12 against N=4, every substantive difference against the scan:

| page | N=4 | N=12 | verdict |
|---|---|---|---|
| 331 | spurious paragraph at flush-left *Par suite* | none | **N=12 right** |
| 332 | printed `(n - 4)` passed without note | R4 `\ednote`: `m` expected (the work writes `(m - 4)` throughout, e.g. p. 306) | **N=12 better** — missed by N=4, `low` and the reference |
| 324 | R4 note on *représenté* | none | annotation only |
| 325 | `\emph` closes after `$\Gamma$` | before it | cosmetic |
| 326, 327, 329 | notes | same notes, different wording/placement | neutral |

Both arms share the p. 325 paragraph and p. 326 punctuation errors, and both transcribers wrote `2P` on p. 329, corrected by their verifiers. **N=12 is at least as good as N=4 and 10% cheaper.** No batch-join errors occurred at `medium` with N=4 either, so fewer joins is not yet a demonstrated gain; the two differences above are not join errors.

### A chapter-sized batch: N=28 (pp. 305–332)

Same setup, one transcriber for pp. 305–332, glossary truncated to its state before p. 305 (no reference to pp. 305–332), handoff the reference's last 15 lines of p. 304. pp. 321–332 therefore sit at positions 17–28 of its context; only they were verified (three concurrent verifiers, as for the other arms). `prepare_pages.py` warns on 4 of 31 pages. Audit clean.

**Cost.** Transcription: **6 turns** (97 tool calls, all parallel), $2.73 for 28 pages = **$0.10/page**; peak context ~220k, not the ~600k extrapolated above. Verification of pp. 321–332: $0.22/page. Total on the compared pages ≈ **$0.32/page**.

**Quality, pp. 321–332, verified, against the scan:**

| | N=4 | N=12 | N=28 |
|---|---|---|---|
| $/page | 0.41 | 0.37 | **0.32** |
| readings wrong | 0 | 0 | **1** — `3P` kept as `2P`; the verifier called the descending 3 "a 2 with ink loss" |
| paragraph breaks wrong | 2 | 1 | **8** |
| p. 332 `(n - 4)` misprint caught | no | yes | yes |

**The paragraph errors are not a depth effect.** Counting paragraphs that open directly after a display: N=28 does it 16× on pp. 305–320 (1.0/page, the start of its context) and 14× on pp. 321–332 (1.2/page); N=4 and N=12 5× on pp. 321–332 (0.4/page). The run adopted a convention on its first page and held it — the risk of a large batch is that one agent's habit reaches every page, where batch boundaries spread it. No glossary entry governs paragraphs after displays (checked), so the smaller starting glossary does not explain it either. The missed `3P` is a verifier miss (all three transcribers wrote `2P`; the N=4 and N=12 verifiers corrected it). One run per arm: variance cannot be separated from batch size.

**Tooling finding: the magnification cap is per output directory.** One N=28 verifier took 7 regions on one page by writing to `vcrops2` and `vcrops3`. `magnify.py` counts crops already on disk in the `--out` directory, so a new directory resets the cap.

**Ordinals.** N=28 wrote `1ʳᵉ` on p. 329 and `Iʳᵉ` on p. 331; its verifier corrected p. 329 to `Iʳᵉ`, as the glossary requires. The print's sort is ambiguous (the reference also has `1ʳᵉ`); the glossary rule settles it.

## Levers (task 4.2) — decided 2026-09-26

| lever | measured | decision |
|---|---|---|
| **transcription batch size** | N=12: −10% cost, equal-or-better quality vs N=4; N=28: −22% cost, worse structure | **12 pages** (or to a nearby chapter boundary) |
| verification batch size | — | **4 pages, concurrent** (unchanged; for wall-clock) |
| effort | `low` failed the kill criterion; `medium` beats the Opus 5 `high` reference on readings | **`medium`** |
| paragraph breaks after displays | the most frequent error in every run, the reference included; no pass checks it | **verifiers check each post-display break against the scan** |
| magnification cap | bypassed via a fresh `--out` | **count per page, independent of output directory** |
| crop targeting | 40–150px vertical misses, the model's coordinates not the tool | follow-up: pad crops or grid the prepared page |
| proofread tooling | ~19% of a run, mostly re-deriving checks | follow-up: ship the mechanical checks as a script |
| image resolution, batch size for cost | 5–12% and 5–7% of cost | no change |
| corpus: Picard p. 323 `f'_{z_{0}}`, p. 329 `3P` | reference wrong, checked at source | separate corpus PR |

