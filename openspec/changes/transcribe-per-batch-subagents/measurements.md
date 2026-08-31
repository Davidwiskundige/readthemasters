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

## Post-change (to be filled by tasks 5.8 and 6.2)

| metric | target | measured |
|---|---|---|
| tokens/page | ≤200k | — |
| vs 4.2M baseline | ≥20× | — |
| turns per page | 2 | — |
| observed `B+P` | ~62.7k | — |
