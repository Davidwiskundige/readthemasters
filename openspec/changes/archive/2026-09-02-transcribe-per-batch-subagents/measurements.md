# Measurements

Reproduce any row with `python pipeline/measure_session.py`.

## Pre-change baseline (task 1.1)

The figure this change is measured against. `clebsch-1864-anwendung-abelschen-functionen`,
pp. 189–206, transcribed 2026-08-29 in a single chat session under the current skill:

| metric | value |
|---|---|
| pages transcribed | 18 |
| API turns | 347 |
| mean context per turn | 220k |
| total tokens | 76M |
| **tokens per page** | **4.2M** |
| page images resident | 111 (198k tokens) |
| page scans' share of context-residency | 62.6% |
| turns re-writing the whole context | 33 (9.5%) |

Two other works, measured the same way, for scale:

| work | pages | turns | mean ctx | total | tokens/page |
|---|---|---|---|---|---|
| `abel-1841-fonctions-transcendantes` | 91 | 1241 | 482k | 600M | 5.8M |
| `riemann-1857-abelsche-functionen` | 42 | 735 | 362k | 267M | 5.4M |

Abel peaked at 920k context and compacted once, at turn 1071 — discarding its early pages, so the
whole-work cross-page memory this design gives up was already partly gone in the longest run.

## Subagent cost model (measured 2026-08-31)

Two clean isolated runs on untranscribed Clebsch pages, both passing `houselint` on every fragment:

| run | pages | reported tokens | tool calls |
|---|---|---|---|
| N=4 | 207–210 | 91.7k | 14 |
| N=12 | 211–222 | 149.7k | 41 |

Fitting `tokens(N) = (B+P) + m·N`:

| parameter | value |
|---|---|
| fixed per subagent, `B+P` | 62.7k |
| marginal per page, `m` | 7.25k |
| turns per page, `t` | ≈3.4 |

N=4's 14 tool calls are exactly `3N + 2` — two crop reads and a write per page, after two
style-file reads.

**Where the cost lives, at N=5:**

| term | tokens/page | depends on N? |
|---|---|---|
| `t·(B+P)` | 212k | **no** |
| `t·m·N/2` | 61k | yes |
| `s·(B+P)/N` | 6k | yes |

**Scenarios** (revised after the crop helper was measured — see below):

| scenario | N* | tokens/page | vs 4.2M |
|---|---|---|---|
| as measured (two half-crops, full HOUSESTYLE) | 1.6 | 254k | 16.5× |
| one crop, no escalation (*optimistic ceiling*) | 2.4 | 153k | 27.5× |
| **one crop + escalation on 25% of pages** | 2.2 | 170k | **24.6×** |
| **  + trimmed style payload** | 2.1 | 149k | **28.2×** |
| one crop + escalation on 50% of pages | 2.1 | 188k | 22.3× |
|   + trimmed style payload | 1.9 | 164k | 25.6× |

## Crop helper, measured (task 2.1)

`pipeline/prepare_pages.py` over Clebsch pp. 207–214: **2,375 tokens/page**, crop boxes at 88–95% of
the page. That is 44% below the 4,274 of two half-crops, and it saves one turn per page.

It also **falsified the original rationale for D5**. The 1568px cap applies to the long edge, which
on a portrait page is the height:

| | source | after the cap | text width |
|---|---|---|---|
| full page `p207.jpg` | 1400×1859 | 1180×1568 | 1180px |
| half crop `c207a.jpg` | 1500×1062 | *not downscaled* | 1500px |

So cropping margins cannot buy half-page resolution — the margins are only ~10% and the height binds
regardless. One image per page costs ~21% of the text width, bought back per page by capped
magnification (D5a). Abel 1841's 91 pages were transcribed at 1147×1568, which is this resolution.

*Caveat:* per-turn context was not observable — subagent transcripts are not persisted. `tokens(N)`
and turn counts are measured; per-page cumulative figures are modelled from those endpoints. Two
points cannot separate setup turns `s` from per-page turns `t`, so the optimum lands in N=1.6–3.2
depending on that split. Default N=4 is within ~3% of optimum across the range.

## Work-dependence

Only `m` is work-dependent, and it splits into images (set by crop strategy, not the work) and
LaTeX output. Output per page across all 13 transcribed works:

| | tokens/page |
|---|---|
| lowest (`abel-1841`) | 526 |
| highest (`riemann-1857`) | 992 |
| spread | 1.9× |

Since `N* ∝ 1/√m`, that spread moves the optimum by well under √1.9. **One default serves the whole
corpus.** The two measured runs came in at 2,473 and 2,327 chars/page — within 0.4% of the
corpus-derived estimate for Clebsch, confirming the estimation method.

## Glossary efficacy (design D2)

| run | `\Sigma` | `\sum` |
|---|---|---|
| pp. 207–210, no glossary | 0 | 19 |
| p. 223, with glossary | 19 | 0 |

Same work, same model, same isolation. The glossary also produced 0 `\cdot`, obeying that rule
exactly — but set 11 *spaced* dots where pp. 189–206 set 63 *tight* ones, because the entry said
only that spacing "is normalized". Precision transmits; vagueness licenses a fresh divergence.

## Post-change, measured (tasks 5.8 and 6.2)

**Run: Clebsch pp. 223–243, 21 pages, five batches, 2026-09-01.** The first real use of the loop.
Every figure in the "measured" columns is reported by the harness; the cumulative column is
**modelled** as `turns × mean context`, with `mean = (B+P + end)/2` and `B+P = 62.7k` carried over
from the fit above — subagent transcripts are still not persisted, so per-turn context remains
unobservable. `turns = tool calls + 1`.

| batch | pages | reported tokens | tool calls | crops | modelled cumulative | per page |
|---|---|---|---|---|---|---|
| 223–226 | 4 | 105.8k | 23 | 7 | 2.02M | 505k |
| 227–230 | 4 | 122.2k | 20 | 7 | 1.94M | 485k |
| 231–234 | 4 | 107.6k | 22 | 6 | 1.96M | 490k |
| 235–238 | 4 | 99.5k | 20 | 5 | 1.70M | 426k |
| 239–243 | 5 | 107.5k | 35 | 11 | 3.06M | 613k |
| **transcription total** | **21** | | **120** | **36** | **10.7M** | **509k** |
| verification 223–232 | 10 | 144.8k | 48 | 15 | 5.08M | 508k |

**The comparison is like-for-like.** `measure_session.py` counts fresh input + cache reads + cache
writes + output — raw context volume, not cost-weighted — so `turns × mean context` is the same
quantity as the 4.2M/page baseline, which also included its verification pass.

| | tokens/page | vs 4.2M baseline |
|---|---|---|
| transcription only | 509k | **8.3×** |
| transcription + verification | ~1.0M | **4.1×** |
| design's projection (D5) | 149–170k | 20–28× |

**The design's projection is not met, and the reason is turns.** D5 assumed one image read plus one
write per page — `t = 2`. Measured `t = 5.7` for transcription and ~4.9 for verification. Two causes,
both real and neither an implementation defect:

- **Magnification costs more than D5a budgeted.** The design forecast escalation on 25–50% of pages;
  measured, batches magnified **36 regions across 21 pages — 1.7 per page**, escalating on nearly
  every page. Each crop is a compute-and-save plus a read, so it roughly doubles a page's turns.
  The escalation is not waste: it settled the `y_1`/`y_2` misprint on p. 227, the roman `d` against
  `∂` on p. 225, the two inequality sorts on pp. 229–230, and it is why 21 pages carry only one
  `\uncertain{}`. But **D5's claim that one image per page makes a page "one Read plus one Write"
  is false whenever the scan is doubtful, which on this work is most pages.**
- **Verification costs about what transcription costs.** D4 called the second read "cheap precisely
  because neither read persists". Residency is indeed not the problem, but the pass is a second full
  reading of every page at 4.9 turns/page — 5.08M for ten pages. It is worth running (it found eight
  real corrections, below), but it should be budgeted as a second transcription, not as a rounding
  error.

**Orchestrating session** (`measure_session.py edaf63a8`, 247 turns):

| metric | value |
|---|---|
| **images read** | **0 (0k tokens)** |
| mean context/turn | 192k |
| peak context | 312k |
| total tokens | 47.8M |
| full-context rewrites | 3 (1.2% of turns) |

The zero is the design's central claim, and it holds mechanically: no scan image entered the
orchestrating session, and `git status` confirmed no subagent touched the repository. But the
orchestrator is **not** cheap — its context still reached a 192k mean against the baseline's 220k,
and the residency breakdown says the filler is now `result: Bash` (59%) and Agent prompts/reports
(21%), not images. Removing scans from the orchestrator did not by itself make the orchestrator
small. *Caveat: this session also ran the whole group-5 A/B, the crop-helper change and the spec
work, so its 47.8M cannot be divided by 21 pages to get a per-page orchestration cost.*

**Where this leaves the design.** The architecture works and is a real improvement — 8.3× on
transcription, with page cost flat across batches (426k–613k, no upward drift from batch 1 to batch
5, which is the property the change exists to buy). It is not the 20–28× D5 projected, and D5's
"one crop, no escalation" ceiling row should be read as unreachable on a scan of this quality
rather than as an optimistic estimate.

## A/B quality check (group 5), measured

**Sample: Clebsch pp. 189–196, 8 of the 18 baseline pages, two isolated batches of 4.**

| batch | pages | reported tokens | tool calls | crops |
|---|---|---|---|---|
| 189–192 | 4 | 89.8k | 22 | 7 |
| 193–196 | 4 | 96.7k | 27 | 8 |
| adjudication (task 5.6) | 3 pages re-read | 97.9k | 38 | 9 |

The 89.8k at N=4 reproduces the earlier clean run's 91.7k at N=4 to within 2%, confirming the cost
model's endpoint.

**Contamination tripwire (5.3): passed.** No fragment was byte-identical to the committed text.
Similarity ran 0.938–0.999 and — the part that matters — **tracked math density rather than being
uniformly near-perfect**: the prose-only opening page scored 0.9993 while the formula-dense p. 191
scored 0.9383. Contamination produces uniform agreement; independent transcription produces exactly
this gradient, because prose converges and math markup does not.

**houselint (5.5): 0 violations on both sides.** Again a sampler, not a gate — see below.

**Divergences (5.4): 66 spans across 8 pages, collapsing to 8 distinct decisions** (the design
predicted "far fewer decisions than divergences"; the ratio was 8:1).

| # | decision | adjudicated by | outcome |
|---|---|---|---|
| 1 | inner fraction of a compound fraction: `\dfrac` or `\frac` | scan | **baseline right, new run wrong** |
| 2 | subscripts `x_{1}` or `x_1` | corpus convention | new run **split against itself** |
| 3 | footnote markers: R15 superscript or bare `~*)` | HOUSESTYLE R15 | new run right |
| 4 | abbreviation dot: `\ ` or `~` | HOUSESTYLE R17 | new run right |
| 5 | word split across a page break | notation.md's own rule | new run right; **baseline had 2 bugs** |
| 6 | `\Sigma` before a fraction: thin space, dot, or tight | scan | new run right |
| 7 | `ihr` vs `ihre` (p. 190) | scan | tie — same text, new run flagged it |
| 8 | `ff.` in the Prym footnote (p. 190) | scan | tie — same text, new run flagged it |

Decision 1 is the substantive one and the new architecture lost it. Both batches wrote `\frac` at
every nesting level, flattening ~28 nested fractions across pp. 193–195. The scan is unambiguous:
measured at both nesting levels across four compound fractions on two pages, the `x` glyph is
13–14px tall and the `∂` 21–22px **at both levels**, agreeing within ±1px, where a script-size
shrink would put the inner `x` at 9–10px. The cause was a gap in the rules payload, not the model:
HOUSESTYLE's `\frac`-not-`\dfrac` ruling governs the operand of a large operator and says nothing
about nesting, so "display math is already display style" was over-applied. Recorded in
`notation.md` with the forbidden reasoning named — and it held: the batch transcribing pp. 231–234
under the corrected glossary got the analogous case right.

Decision 2 is the failure mode the glossary exists for, caught in the act: batch 1 wrote `x_1`
throughout pp. 191–192 and batch 2 wrote `x_{1}` throughout pp. 193–196, **in the same run**. The
committed file had drifted the same way (pp. 189–206 braced 218 subscripts, pp. 207–222 left 166
bare). Nothing on the page decides it; only a written-down convention can.

Decision 5 found two outright bugs in the committed baseline — p. 195 ended `An-` with p. 196
opening `zahl`, and p. 198 ended `aus-` with p. 199 opening `reichend` — both violating a rule
already written in this work's own `notation.md`, both rendering a stray hyphen and space inside a
running word, and both invisible to `houselint`. The new run wrote `Anzahl` whole.

**Verdict (5.9): rollout proceeds.** Every substantive decision was adjudicated against the scan and
recorded. The new architecture is not uniformly better than the baseline — it lost decision 1 — but
the loss was a missing glossary entry, which is a repairable class, and the glossary demonstrably
repaired it. Markup-only divergence (whitespace inside math, `\qquad`/`\quad`, `$(p=1)$` versus
`($p=1$)`) did not block.

**The mechanical checks were, again, exactly as weak as the design says.** `houselint` passed both
versions at 0 violations while the baseline carried two page-break hyphenation bugs and nine
R15/R17 violations, and while the new version carried 28 flattened nested fractions. Every one of
the eight decisions was settled by the scan or by a written ruling — none by the diff or the linter.

## What the verification pass caught (task 6.1, pp. 223–232)

Run as a separate subagent per the D4 contract. It confirmed the two readings the transcribing
batches had flagged as unresolved — p. 228's last line really is printed `n^{\text{ter}}` (Clebsch's
own slip, kept per R4) and p. 227's rows 2–3 really are printed `y_2` — and found eight corrections
the transcription had got wrong:

- five continuation-dot rows with the wrong dot count (p. 224 12→10, p. 225 6→12 and 6→15 twice,
  p. 227 9→12), all measured off the scan by pixel-lattice profile;
- three inline fractions still written `\frac` on pp. 226–228, which predate the `\dfrac` glossary
  entry added mid-run.

It also raised one non-finding worth recording: letterspacing *inside* an already-italic passage
looked like dropped emphasis but is correct under R24, since both devices collapse to `\emph` and a
nested `\emph` would break `tex.js`'s `[^}]*` match. That is now a `notation.md` entry so the next
verification pass does not re-raise it.

**All 1383 math spans in the assembled pp. 189–243 render through the site's own KaTeX 0.16.47
build**, and the site's `tex.js` tests still pass (27/27).
