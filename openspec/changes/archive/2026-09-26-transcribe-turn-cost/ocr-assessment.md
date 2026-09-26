# Should an OCR-first pipeline replace the vision-LLM reader?

*Assessed 2026-09-05. This is the alternatives record behind `proposal.md`: before optimizing the
current reader we asked whether to replace it.*

## The question

Replace the per-page vision-LLM read with a conventional OCR stack — a text engine for prose, a
math-to-LaTeX engine for formulas — and call an LLM only on passages the OCR marks ambiguous.
Motivation: cost and wall-clock, not quality. The current pipeline's output quality is not in
dispute.

## Verdict

**No. Keep the vision-LLM reader.** The savings are real in principle but unreachable in practice on
this corpus, and the failure mode they would buy is the one class of error for which we have no
automated detector.

## What was surveyed

| Tool | Role | Where it fails here |
|---|---|---|
| Tesseract / Kraken / Calamari (+ historical models) | prose OCR | no math; but genuinely good — see "Where OCR does earn a place" |
| Mathpix | commercial math OCR, ~$0.005/page | arXiv-normalized output; best-in-class BLEU, wrong objective |
| pix2tex (LaTeX-OCR) | isolated equation → LaTeX | block equations only; hallucinates on text; needs a separate formula detector |
| texify, Pix2Text | open math OCR | same normalization problem, lower accuracy than Mathpix |
| Nougat | full-page academic PDF → markup | trained on arXiv; historical pages are far out of distribution; known repetition/hallucination |
| olmOCR 2, dots.ocr, MinerU, PaddleOCR-VL | open-weight document VLMs, self-hosted | strong on modern layouts; no notation-faithfulness objective; still a VLM, so it is the current design with a weaker model |

Note the last row: the open-weight VLMs are not an alternative *architecture*. They are the same
architecture with a model that has not been instructed on our house style. Swapping to them is a
quality decision, not an efficiency one.

## Why the idea cannot be dismissed on token share alone

If OCR carried the bulk of pages and the LLM saw only the ambiguous ones, the saving would be
70–80% of transcription cost — not a rounding error. The prepared page image is only ~2.4k tokens
against ~509k/page of measured context volume, but that comparison is beside the point: the proposal
removes the *LLM pass*, not the image. So the argument has to be about feasibility.

## A1. Ambiguity is not detectable without the scan, and this corpus is ambiguous nearly every page

The routing premise — "OCR the easy 80%, escalate the hard 20%" — requires a calibrated signal for
which passages are hard. There isn't one:

- Measured on Clebsch pp. 223–243: **36 magnification crops across 21 pages, 1.7 per page**, i.e.
  escalation on nearly every page. There is no easy 80% on scans of this quality.
- On Göttinger Nachrichten 1869 both batches hit the 3-crops-per-page cap on nearly every page, and
  **all 25 crops went to subscripts, exponents and small punctuation**. The prose was fine
  throughout. OCR is strongest exactly where we need no help.
- OCR confidence is uncalibrated out of distribution, and 17th–19th c. mathematical typesetting is
  the out-of-distribution tail. A math OCR model is not *uncertain* when it silently modernizes; it
  is confident and wrong.

What the crops actually settled, and whether math OCR would settle them:

| Crop settled | Math OCR? |
|---|---|
| continuation-dot counts (5 corrections, pp. 224–227) | **No** — emits `\cdots`, does not count |
| nested `\frac` vs `\dfrac` sizing (28 spans) | **No** — always `\frac` |
| `y_1`/`y_2` misprint (p. 227) | probably |
| roman `d` against `∂` (p. 225) | probably |
| two inequality sorts (pp. 229–230) | probably |

About half, at best — and the half it misses is the half that needs counting, sizing, and judgment.

## A2. Normalization is the disqualifier, and nothing we run would catch it

Every math-to-LaTeX model is trained on arXiv-era LaTeX. Its objective *is* to emit the modern
rendering of what it sees. Non-negotiable rule 2 is the exact opposite: `zz` not `z^2`, the Sigma
letter not `\sum`, tight baseline dots not `\cdot`, `arc.` preserved, printer's errors kept under
R4.

The measurements say this class is invisible to our mechanical checks:

- `houselint` returned **0 violations** on a version carrying 28 flattened nested fractions, and
  **0** on a version carrying two page-break hyphenation bugs plus nine R15/R17 violations.
- All eight distinct A/B decisions were settled by the scan or by a written ruling — **none** by the
  diff or the linter.

So OCR-first would inject a systematic, confident, silent notation drift into the one place we
detect nothing automatically. The cost lands on human review, which is the project's scarce
resource. Everything the status ladder means by `skimmed` and `verified` gets more expensive, not
less.

## A3. The economics do not motivate it

- Mathpix at ~$0.005/page is ~$1.50 for a 300-page book against $6–12 for an Opus batch run: a
  **$5–10 saving per book**, and only if the LLM pass disappeared entirely, which A1 says it cannot.
- Under principle 5 the project's AI spend is €0 either way; the saving would accrue to individual
  Tier-3 contributors at roughly the price of a coffee per book.
- On the Tier-2 path — the one actually in use — the dollar saving is **exactly zero**. The currency
  there is rate limits and wall-clock, and those are set by turns, not by pixels. See `proposal.md`.
- Against that: a paid third-party API key, a `$19.99` activation, and a non-Anthropic dependency in
  a pipeline whose whole point is that a contributor can run it with what they already have.

## Where OCR does earn a place (noted, not adopted here)

One use is free, local, and carries no faithfulness risk, because it **produces nothing**.

Historical prose OCR is good: pretrained models reach 95–98% character accuracy on 19th-c. Fraktur,
and Calamari ensembles go below 1% CER. Run a text-only engine over the full-resolution scan, strip
math from `original.tex`, and diff the two as a mechanical check in the text-only proofread phase. That is a deterministic,
zero-token detector for dropped lines, skipped paragraphs and transposed words — a defect class that
is invisible to `houselint` and currently costs an LLM subagent to find (the proofread found a word split
across a page break and six mid-sentence paragraph breaks that way).

Deliberately out of scope for `transcribe-turn-cost`, which is about turns. Recorded here so the
option is not re-derived from scratch.

## What would change the verdict

- A math OCR model trained to transcribe *as printed* rather than as modern LaTeX. This needs
  ground truth that, as far as we can tell, does not exist for historical mathematical typesetting.
- A mechanical detector for notation drift strong enough that A2's silence is no longer silent.
  `houselint` is a sampler, not a gate, and the measurements say so twice.
- A corpus shift toward clean modern typography, where the ambiguity rate collapses and A1's
  premise stops holding.

## Sources

- Mathpix API pricing — https://mathpix.com/pricing/api
- pix2tex (LaTeX-OCR) — https://github.com/lukas-blecher/LaTeX-OCR
- texify — https://github.com/VikParuchuri/texify
- olmOCR 2, *Unit Test Rewards for Document OCR* — https://arxiv.org/pdf/2510.19817
- OCR of 19th-c. classical commentaries — https://ar5iv.labs.arxiv.org/html/2110.06817
- Ground truth for OCR on German Fraktur and Early Modern Latin —
  https://www.researchgate.net/publication/366245443_Ground_Truth_for_training_OCR_engines_on_historical_documents_in_German_Fraktur_and_Early_Modern_Latin
- In-repo evidence: `openspec/changes/archive/2026-09-02-transcribe-per-batch-subagents/measurements.md`
