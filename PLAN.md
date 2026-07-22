# ReadTheMasters — Project Plan

A website that publishes **AI transcriptions (LaTeX)** and **AI translations (LaTeX)** of old
mathematics and physics texts, with the original source always cited, and only for texts that
comply with copyright rules worldwide.

---

## 1. Product definition

For every published *work* the site offers:

| Layer | Content | Example |
|---|---|---|
| Source | Link to the scan of the original edition (Archive.org, Gallica, e-rara, GDZ, …) | Riemann, *Über die Hypothesen…*, Göttingen 1868 scan |
| Transcription | Faithful LaTeX transcription of the original (original language) | German LaTeX text with formulas |
| Translation(s) | AI translation into English (later: other languages), also in LaTeX | English LaTeX text, math preserved |
| Metadata | Author(s) (birth/death, Wikidata id), publication date, venue/journal, discipline + tags, language, edition, copyright assessment, AI model + date, review status | YAML file (drives browse/filter — §9a) |

Guiding principles:

1. **Copyright gate before publication** — enforced automatically (CI), not by memory.
2. **Everything versioned in git** — texts are plain-text LaTeX + YAML, reviewed via pull requests.
3. **Spec-driven development** — features are proposed/specified/archived with OpenSpec.
4. **Provenance always visible** — scan source, AI model, prompt version, and human review status
   are part of the published record.
5. **The project pays for no AI compute** — every AI step (transcription, translation,
   verification) runs on a contributor's own API key or chat subscription. The project's own
   budget covers the domain name and nothing else; maintainers contributing texts do so under the
   same bring-your-own-AI rules as everyone else.

### 1.1 Goals & non-goals

**Goals**
- Preserve landmark public-domain mathematics & physics texts as clean, reusable LaTeX — faithful
  transcriptions and readable translations.
- Make copyright compliance **auditable** — every published text carries a sourced,
  machine-checkable assessment.
- Build an **open corpus (CC0)** usable as a dataset, not just a website.
- Run **community-powered at ~zero project cost** (bring-your-own-AI, static hosting).

**Non-goals** (explicit scope boundaries — change only via an OpenSpec proposal)
- **Not a scan/facsimile archive** — we link to libraries and embed only small figure crops
  (§4.5); we don't rehost full scans.
- **Not a general OCR/transcription service** — the pipeline serves this corpus, not arbitrary
  uploads.
- **Not a modernization** — we transcribe faithfully and don't reinterpret or update the
  mathematics (§4.4).
- **Not a host for in-copyright works** — the gate (§2) is absolute.
- **Not (initially) a dynamic web app** — no accounts, comments, or server-side features until an
  accepted proposal says otherwise.

---

## 2. Copyright compliance model

This is the load-bearing design decision, so it gets its own section. *(Not legal advice —
a practical engineering policy that errs on the safe side.)*

### 2.1 Why both dates matter

- Most of the world (EU, UK, Brazil, Japan for newer works, …): public domain **70 years after the
  author's death** ("pma 70").
- **United States**: what matters is the **publication date** — works published ≥95 years ago are
  public domain (in 2026: everything published before 1931), *regardless* of when the author died.
  Conversely, a work by an author long dead can still be US-copyrighted if first published late.
- Outliers: Mexico is pma 100, Spain pma 80 for pre-1987 deaths, a few countries pma 50.

Example of the trap: **Einstein (d. 1955)** entered the public domain in pma-70 countries on
1 Jan 2026 — but his 1935 EPR paper stays US-copyrighted until 2031 (1935 + 95 + 1). Storing only
one date is not enough. Hence: **store author death date AND first-publication date**, evaluate
both rules.

### 2.2 Publication policy (the "gate")

A work may be published on the site only if **all** of the following hold:

| Rule | Check |
|---|---|
| `pma_70` | every author died ≥ 70 full calendar years ago (or work is anonymous and published ≥ 70 years ago) |
| `us_publication` | first published ≥ 96 years ago (safe formulation of the US 95-year rule with the Jan-1 rollover) |
| `edition_rights` | the *specific scanned edition* is either the original/early edition, or its editorial additions (critical apparatus, new commentary, new typesetting claims) are excluded from transcription. Germany/Italy protect critical editions ~20–25 years; UK typographical arrangement 25 years. Transcribe from original editions where possible. |
| `translation_source` | translations are made **only from our own transcription of the PD original**, never from an existing modern (copyrighted) human translation |

Optional strict mode (config flag): `pma_100` to also cover Mexico. Default: off, documented.

### 2.3 Data consequences

- `Author.death_date` may be `null` only with `anonymous: true` or `death_date_unknown: true` +
  justification; unknown death date blocks publication unless publication is old enough that
  pma-70 is satisfied for any plausible lifespan (e.g. published ≥ 170 years ago).
- Every work stores a machine-written `copyright_assessment` block (which rules were evaluated,
  with what dates, verdict, timestamp) so decisions are auditable.
- Death dates are cross-checked against **Wikidata** (authors get a Wikidata/VIAF ID in metadata);
  a small script can verify our dates against Wikidata in CI.

### 2.4 Status of our own output

AI-generated transcriptions/translations have doubtful copyrightability (US Copyright Office:
purely AI output is not protectable). To keep the corpus unambiguous and reusable, release all
site content under **CC0** (or CC-BY if attribution is wanted). This is also the ethical match for
a public-domain project.

### 2.5 Sourcing & auditability of copyright facts

The gate is only as trustworthy as its inputs, so the copyright-critical facts must be **sourced**,
not merely asserted. `work.yaml` records a citation for each:

| Fact | Source recorded | CI behavior |
|---|---|---|
| Author death date | Wikidata QID (already cross-checked) | auto-verified vs Wikidata; warn on mismatch |
| First-publication date | library catalog record, bibliography, or DOI | **required** — an unsourced publication date fails the gate |
| Edition identity | the specific scan's catalog entry | **required** — ties the assessment to the exact edition transcribed |

For **borderline works** (first publication near a threshold year), a human reviewer confirms the
cited source actually supports the claimed year before approval. The `copyright_assessment` block
thus reads as a self-contained, checkable argument: which rules, which dates, which sources,
verdict, timestamp.

---

## 3. Architecture

**Recommendation: static site + "corpus as git repository".** No database, no server to maintain,
free hosting, and git versioning of the texts falls out naturally.

```
readthemasters/            (one git repo, GitHub)
├── openspec/              # OpenSpec: project.md, specs/, changes/, archive/
├── corpus/
│   └── fagnano-1718-lemniscata/
│       ├── work.yaml          # metadata: author(s), dates, edition, source URL, copyright block
│       ├── original.tex       # transcription (original language)
│       ├── translations/
│       │   └── en.tex
│       └── provenance.yaml    # model, prompt version, batch ids, review status per file
├── pipeline/              # Python scripts: transcribe, translate, validate, wikidata-check
├── site/                  # Astro site (builds catalog + work pages from corpus/)
└── .github/workflows/     # CI: copyright gate, LaTeX compile check, site deploy
```

Component choices:

| Concern | Choice | Why |
|---|---|---|
| Site generator | **Astro** | content-driven static sites, fast, easy YAML/content collections |
| Math rendering | **KaTeX** (build-time render) | fast, no client JS needed for math |
| PDF artifacts | **Tectonic** in GitHub Actions | reproducible LaTeX → PDF per text, downloadable |
| Search | **Pagefind** | static search index, zero infra |
| Hosting | **Cloudflare Pages** (or GitHub Pages) | free, custom domain, global CDN |
| Scans | **Link, don't rehost** (Archive.org etc.) | zero storage cost, provenance stays with the library |
| AI pipeline | Python + Anthropic SDK, **Batch API** — run by contributors on their own keys (§7) | project pays no AI costs; Batch's 50% discount benefits contributors |
| Review UI | GitHub pull requests | diff review of .tex is exactly what PRs are good at |

If the site later needs dynamic features (user accounts, comments, correction submissions from
non-git users), add them then — e.g. Supabase/Neon free tier or a small VPS — as an OpenSpec
change proposal. Don't build it up front.

### 3.1 The copyright gate in CI

A `pipeline/validate.py` runs on every PR:

1. Schema-validate every `work.yaml` (required fields, ISO dates).
2. Evaluate `pma_70` + `us_publication` (+ `pma_100` if enabled); **fail the build** on violation.
3. Cross-check author death dates against Wikidata (warn on mismatch).
4. Compile every changed `.tex` with Tectonic (catch broken LaTeX).
5. Validate the per-artifact `status` field against the quality ladder of §4.3 (`ai-draft` →
   `spot-checked` → `proofread` → `validated`) and check consistency (e.g. a `validated` status
   requires two distinct reviewers in provenance). The site build shows the matching badge; a
   config value sets the minimum status that gets published at all (default: `ai-draft`).

Nothing reaches the live site without passing the gate — the compliance rule is code, not policy.

### 3.2 Canonical work identity & editions

**Every work has a canonical ID**, preferring a stable external identifier: Wikidata QID if one
exists, else a DOI, else a deterministic slug (`author-year-shorttitle`). Stored as `id` in
`work.yaml` and used as the directory name and permanent URL.

- **Duplicate prevention:** CI enforces unique IDs; matching on the Wikidata QID catches "same
  work, different scan." The contributor guide's first step is an "is this already in the corpus?"
  search, backed by the claims file (§10).
- **Editions/variants:** a work is the abstract text; a specific scanned printing is an `edition`
  block (year, publisher, source identifiers, and whether it is the edition we transcribed).
  Multiple editions may be recorded; we transcribe from the earliest clean public-domain edition
  and mark it — which is also what `edition_rights` in §2 evaluates.

### 3.3 PDFs — compile at deploy time, don't commit

Downloadable PDFs are built **once per deploy in CI with Tectonic**, not on every visit and not
stored in git:

- *Compile on every visit* — rejected: the site is static (no server), and full LaTeX in the
  browser needs a heavy (~tens of MB) WASM TeX engine that is slow to load. On-page math is
  already handled by KaTeX; the PDF is a separate downloadable artifact.
- *Commit prebuilt PDFs* — rejected: binary blobs bloat a text corpus, churn on every edit, and
  drift from source when the `.tex` changes but the PDF doesn't.
- *Compile at deploy with Tectonic* — **chosen**: each `.tex` → PDF during the site build,
  published under `/pdf/<id>/`, regenerated only for changed works (cached) and never committed.
  A work MAY optionally ship a pre-made PDF as an override for the rare case Tectonic can't
  reproduce it. Source stays clean; PDFs never drift.

---

## 4. AI pipeline design

The pipeline lives in the repo, but **it is executed by contributors on their own AI accounts**
(API key, Claude Code subscription, or chat app — see §7 and §10). The project runs only the free
non-AI checks in CI. The steps below describe what a contributor's run does.

### 4.1 Transcription (scan → LaTeX)

1. **Acquire scan** — download page images (or PDF) from the source library; record identifiers.
2. **Page-level transcription** — one Batch API request per page (image + instructions →
   LaTeX fragment). Include the previous page's tail for continuity. Model: **Claude Opus 4.8**
   for hard material (blackletter/Fraktur, dense 18th–19th c. math, poor scans); **Claude
   Sonnet 5** for clean modern typography at lower cost.
3. **Stitch + normalize** — script concatenates fragments; one cleanup pass (model) fixes
   hyphenation breaks, heading structure, macro consistency.
4. **Verification pass** — a second pass (cheap model, e.g. Haiku/Sonnet) compares the rendered
   transcription against the scan page-by-page and flags discrepancies. For pipeline runs
   (tiers 2–3) this is part of the contributor's run and its output ships with the submission;
   for chat submissions (tier 1) a reviewer runs it with their own AI. Either way, not on the
   project's bill.
5. **Human review** — PR with the `.tex`; reviewer spot-checks against the scan; approval flips
   `review.status`.

### 4.2 Translation (LaTeX → LaTeX)

- Chunk by section/paragraph; translate text while preserving math, labels, and environments
  verbatim (explicit instruction + validation that math tokens survived unchanged).
- Glossary file per work/era (e.g. 19th-c. German math terminology) fed into the prompt for
  consistency; the glossary itself lives in git and improves over time.
- Same Batch API + PR review flow. Translation notes (`\footnote{}` translator remarks) allowed
  but tagged.

### 4.3 Quality status & provenance

Every artifact (each transcription, each translation) carries a **quality status** — a ladder
modeled on Wikisource's proofreading levels, so visitors always know how much to trust a text:

| Status | Meaning | Badge on site |
|---|---|---|
| `ai-draft` | Machine output; automated checks only (LaTeX compiles, AI verification pass ran) | grey — "AI draft, not yet human-checked" |
| `skimmed` | A human gave it a superficial once-over — a sample of pages, or just the math, plus everything the verification pass flagged, but not a full word-for-word pass | bronze — "Skimmed" |
| `verified` | Full, rigorous human pass against the scan (transcription) / against the original text (translation) | gold — "Verified" |

Publishing policy: `ai-draft` texts **are** published (content velocity, and honesty beats
hiding), but with a prominent badge and a banner inviting corrections. A site-wide config can
raise the minimum publishable status later if quality becomes a concern.

`provenance.yaml` records per artifact:

```yaml
transcription:
  status: skimmed               # ai-draft | skimmed | verified
  model: claude-opus-4-8        # model that produced the current text
  effort: xhigh                 # thinking/effort level, optional; low|medium|high|xhigh|max,
                                #   "adaptive", "extended" (chat toggle), or null if unknown
  prompt_version: transcribe-v3 # pipeline prompt/spec version
  batch_ids: [msgbatch_...]
  produced: 2026-07-20
  verification: {model: claude-sonnet-5, flagged_pages: [12, 31], date: 2026-07-21}
  reviewers: [{name: DvdL, level: skimmed, date: 2026-07-25}]
translations:
  en:
    status: ai-draft
    model: claude-opus-4-8
    effort: adaptive
    ...
```

`effort` is **provider-agnostic and optional**. For API/pipeline runs (tiers 2–3) it records the
exact setting (`low`–`max`, or `adaptive`). For chat contributions (tier 1) it holds whatever the
contributor can report — `"extended"` if they used a thinking toggle, `"standard"` otherwise, or
`null` — the issue form offers these as a dropdown so no one has to know API terminology. It is
metadata for reproducibility and quality analysis, **not** a gate: the status ladder decides
trust, not the effort level.

The site renders this as an attribution line per artifact, e.g.
*"Transcribed by Claude Opus 4.8 (July 2026) · Skimmed by DvdL"* — and re-runs with a newer
model are ordinary git commits, so the full history stays auditable. Status is per-artifact, not
per-work: a verified transcription can coexist with an ai-draft translation.

---

## 4.4 LaTeX house style & fidelity policy

**Standardize the markup; stay faithful to the content.** These are separate axes, and the answer
to "conventions or original?" is "conventions for *how* we encode, fidelity for *what* we encode."

| Layer | Policy |
|---|---|
| **Markup & structure** (macros, environments, file layout, encoding) | **House style, enforced.** Invisible to the reader; the translation pipeline, KaTeX/Tectonic rendering, faceting, and clean PR diffs all depend on it being uniform. |
| **Notation & content** (author's words, symbols, formula structure) | **Faithful to the original — never silently modernized.** Where notation diverges confusingly from modern usage, explain it via the optional facing-notation annotation layer (backlog #14), don't overwrite it. |
| **Typography & orthography** (Fraktur, long-s, ligatures, original line/hyphenation breaks) | **Normalized to readable modern rendering** — this is a transcription, not a facsimile. *Exception:* preserve page boundaries as `\origpage{n}` markers (metadata for the side-by-side reader and citation anchors), not as visual layout. |

### Shared preamble & apparatus

`corpus/preamble/` provides a small shared package (or document class) that every text uses, so
the corpus is uniform and renderable by both engines:

- **Structure** — standard sectioning and theorem-like environments (named by us, mapped onto the
  original's structure).
- **Scholarly apparatus macros** — `\origpage{n}` (page boundary), `\uncertain{...}` (doubtful
  reading), `\illegible` (unrecoverable), `\ednote{...}` (editorial note), and a diagram
  placeholder that links to a region of the scan (we do not attempt to redraw figures — we point
  to the original). These make transcription *honesty* machine-readable.
- **Curated math macros** for recurring archaic notation — defined **once** in the shared preamble
  so the author's notation is preserved consistently rather than reinvented per contributor. Add
  sparingly; prefer standard commands.

### Rendering constraint

Math must render in **both** KaTeX (web) and Tectonic (PDF). The house style therefore stays
within a KaTeX-supported LaTeX subset for math, and any custom math macro defined in the preamble
is mirrored in a KaTeX macro map. CI compiles every `.tex` against the shared preamble (Tectonic)
and rejects non-whitelisted packages, keeping the corpus portable.

### How the convention is applied

The pinned pipeline/chat prompts (§10) **encode the house style** — structure, apparatus macros,
"transcribe faithfully, don't modernize notation, normalize typography" — so contributor output is
uniform regardless of which model or app produced it. The house style itself is specified in the
`corpus-format` proposal (§5); changes to it are versioned like any other spec.

## 4.5 Figures & diagrams

Historical math and physics is full of diagrams, and LLMs can't reliably redraw them. **Default
policy: crop the figure region straight from the scan and embed it inline** — it is the *actual
original figure*, so it's exact and faithful with no redrawing. Because the scan is public domain
(guaranteed by the gate), the crop is public domain too.

- This is a deliberate, narrow exception to "link, don't rehost" (§3): we still never rehost full
  scans, but we **do** host small figure crops, because they're integral to the text and
  unambiguously PD. Storage is trivial (a few KB per figure).
- The diagram-placeholder macro from §4.4 resolves to the embedded crop, with a caption and
  **alt text** for accessibility, and provenance recording the source page and region.
- **Optional enhancement (backlog):** a redrawn vector version (TikZ/SVG) for print quality and
  screen-reader access, flagged `redrawn: true` and kept *alongside* — never replacing — the
  original crop.

## 4.6 Referencing existing open translations

A public-domain or openly-licensed translation often already exists (e.g. W. K. Clifford's 1873
English rendering of Riemann's 1868 lecture). We **reference** these rather than duplicate them:
`work.yaml` carries an `external_translations` list (language, translator, year, license, venue,
url), and the work page shows an "Existing translations elsewhere" section. This is pure metadata —
a link is always allowed, whatever the translation's copyright — and is separate from our own
`translations/<lang>.tex`.

Optionally, a translation that is *itself* public-domain or openly-licensed may be **imported** as
a hosted artifact, with provenance `source: external-open` and its `license` recorded (the gate
requires the license). A still-copyrighted translation may only be linked, never hosted, and our
own translations are still made only from our transcription (the `translation_source` rule, §2.2).

---

## 5. Spec-driven workflow (OpenSpec)

- `openspec init` in the repo; `openspec/project.md` holds conventions (stack, corpus format,
  copyright policy pointer, review rules).
- Every feature = one change proposal: `/opsx:propose` → `proposal.md` + delta specs + `tasks.md`
  → implement → `/opsx:verify` → `/opsx:archive`. `openspec/specs/` stays the source of truth for
  what the system *is*; `openspec/changes/archive/` is the decision history.
- First proposals, in order:
  1. `corpus-format` — work.yaml schema (incl. faceting fields + `vocab.yaml`, canonical IDs &
     edition blocks §3.2, copyright-fact sources §2.5), directory layout, provenance format,
     **LaTeX house style + shared preamble (§4.4)**
  2. `copyright-gate` — the rules of §2 as a spec + validator
  3. `site-catalog` — catalog + work pages, KaTeX rendering, **browse & filter facets (§9a)**
  4. `transcription-pipeline` — §4.1
  5. `translation-pipeline` — §4.2
  6. `search-and-pdf` — Pagefind + Tectonic artifacts

Content additions (new texts) are *not* OpenSpec changes — they're ordinary PRs gated by CI.

---

## 6. Phased roadmap

| Phase | Deliverable | Effort (part-time) |
|---|---|---|
| 0. Foundations | git init, openspec init, project.md, repo skeleton | 1 evening |
| 1. Corpus + gate | work.yaml schema, validator, Wikidata check, one text added *manually* as fixture | 1–2 weeks |
| 2. Site MVP | Astro site: catalog with browse/filter facets (§9a), work page (scan link + LaTeX + translation side by side), legal pages (§11.3), deploy to Cloudflare Pages with domain | 2 weeks |
| 3. Transcription pipeline | Batch scripts + stitching + verification + PR flow; first fully AI-transcribed work | 2 weeks |
| 4. Translation pipeline | Translation scripts + glossary mechanism; first translated work live | 1–2 weeks |
| 5. Polish & scale | Pagefind search, PDF downloads, contributor guide, steady cadence of new texts | ongoing |

Good pilot candidates (safe under both rules, mathematically iconic, decent scans):
Euler (d. 1783), Gauss *Disquisitiones* (1801, d. 1855), Riemann (d. 1866), Maxwell (d. 1879),
Boltzmann (d. 1906), Poincaré (d. 1912), Noether *Invariante Variationsprobleme* (1918, d. 1935),
Hilbert pre-1931 papers (d. 1943 — pma-70 satisfied since 2014, pre-1931 publications clear the
US rule too).

---

## 7. Cost prediction

### 7.1 Fixed costs (infrastructure)

| Item | Cost |
|---|---|
| Domain name | ~€10–15 / year |
| Hosting (Cloudflare Pages / GitHub Pages free tier) | €0 |
| CI (GitHub Actions free tier, public repo = unlimited) | €0 |
| Database / storage (none needed; scans linked not hosted) | €0 |
| **Total fixed** | **~€10–15 / year** |

### 7.2 AI costs — carried by contributors, not the project

**Policy (principle 5): the project's AI spend is €0.** The table below is *reference
information for contributors* deciding what a run will cost them — and for the contributor guide,
which should show it so nobody is surprised. Contributors on chat subscriptions (tier 1/2) pay
nothing extra at all beyond the subscription they already have.

Current API pricing (per million tokens): **Opus 4.8** $5 in / $25 out; **Sonnet 5** $3 / $15
(intro $2 / $10 through Aug 2026); **Batch API: −50%** on everything. Per scanned page, roughly
2–3.5k input tokens (page image + instructions) and 1–2k output tokens (LaTeX):

| Task, model | Per page (batch) | 300-page book (batch) |
|---|---|---|
| Transcription, Opus 4.8 | ~$0.02–0.04 | ~$6–12 |
| Transcription, Sonnet 5 | ~$0.01–0.02 | ~$3–6 |
| Verification pass (optional) | +~60–100% of the above | +$3–10 |
| Translation, Opus 4.8 | ~$0.01–0.03 | ~$4–8 |
| Translation, Sonnet 5 | ~$0.006–0.015 | ~$2–5 |

**Rule of thumb for a contributor: €5–25 per book** for transcription + verification + one
translation via the Batch API (lower end Sonnet, upper end Opus on difficult material). Short
papers (10–40 pages): well under €1–3 each — the sweet spot for casual contributions.

### 7.3 Project totals, year one

| Item | Cost to the project |
|---|---|
| Domain | ~€10–15 / year |
| Hosting, CI, storage | €0 (free tiers, public repo) |
| AI (any number of texts) | **€0 by policy** — contributor-funded |
| **Total, at any scale** | **~€10–15 / year** |

The project's cost no longer depends on how many texts get published — scale costs contributors'
goodwill, not money. Development labor remains the largest real investment (~6–8 part-time weeks
to Phase 4), but with Claude Code doing spec-driven implementation that is calendar time more
than money.

### 7.4 Bring-your-own-AI — the operating model

This is **policy, not an option**: all AI work runs on contributors' own accounts. Because the
pipeline is repo-local scripts and contributions are PRs, this needs no infrastructure at all:

| Mechanism | How | Notes |
|---|---|---|
| **BYO API key** | Contributor sets their own `ANTHROPIC_API_KEY` (or another provider's), runs `pipeline/transcribe.py`, opens a PR | Zero infra on our side; the pinned prompt version keeps output comparable |
| **BYO Claude subscription** | Repo ships a Claude Code skill (e.g. `/transcribe <work> <pages>`); contributors with Pro/Max run it as an agent task — no per-token billing for them | Great for papers/chapters; subscription rate limits make 400-page books a multi-session job; no Batch discount |
| **In-browser tool (later)** | Static page where a visitor pastes their own API key (kept in localStorage; Anthropic's API supports direct browser access) and transcribes a few pages, then exports a ready-to-submit patch | Lowers the barrier for non-git users; needs careful key-handling UX; backlog material |

Not possible: "log in with your Claude account" on our site — there is no third-party OAuth for
consumer-subscription inference, so a website cannot piggyback on visitors' Claude.ai plans.
BYO key/subscription-via-Claude-Code are the workable routes.

Consistency requirements (all already in the design): contributor runs must use the repo's pinned
prompt version, must emit `provenance.yaml` (model recorded — any capable model is acceptable,
the status ladder is the quality gate, not the model brand), and everything still passes the CI
copyright gate — which is pure code, no AI, and therefore free.

**Independent QA without project spend:** the verification pass (§4.1 step 4) is part of the
contributor's own run for pipeline submissions; for chat submissions it is run by the *reviewer*
on the reviewer's AI account. Since reviewer and contributor are different people, the
independent-check property survives without the project paying for a centralized pass.

**Bootstrap:** before there is a community, the maintainer is simply contributor #1, using a
personal subscription or key under exactly the same rules — the project budget itself never
carries an AI line. If a funded pool is ever wanted (e.g. to sponsor runs for keyless
contributors), route it through GitHub Sponsors as a separate, explicit fund rather than
project money.

### 7.5 Cost tips for contributors

To be included in the contributor guide, so runs stay cheap:

- Always use the **Batch API** (50% off; transcription is never latency-critical).
- Sonnet 5's **introductory pricing ($2/$10) runs through 2026-08-31** — cheap window for a first
  bulk transcription run.
- Start pages at ~1080p-equivalent resolution; escalate to full high-res (Opus, up to 2576px long
  edge, ~3× image tokens) only for pages the verification pass flags.
- Cache the fixed instruction prompt (prompt caching, −90% on the shared prefix).
- On a chat subscription (tier 1/2): marginal cost is zero — prefer papers and chapters over full
  books to stay within rate limits.

---

## 8. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Copyright edge case slips through (late first publication, protected critical edition) | Gate in CI + both-dates policy + edition provenance recorded; takedown process documented on the site |
| AI mistranscribes formulas | Verification pass + human review PR + "report an error" link per page (opens GitHub issue) |
| Fraktur/handwriting too hard for OCR-by-LLM | Pilot on printed antiqua texts first; keep per-page confidence flags; escalate hard pages to Opus high-res |
| Scope creep (accounts, comments, dynamic features) | OpenSpec: features exist only as accepted change proposals |
| Source library link rot | Store stable identifiers (Archive.org ID, DOI, library permalink), not bare URLs |
| Few contributors early on → no new content under the BYO-AI policy | Maintainer is contributor #1 on a personal subscription; keep tier 1 friction minimal (copy-paste prompt, issue form); "good first text" labels; the policy costs nothing to keep even while the community is small |
| Unsourced or wrong first-publication date slips the gate | Gate requires a cited source for publication date + edition; human confirmation for near-threshold works (§2.5) |
| Contribution IP status unclear | DCO `Signed-off-by` on every PR + a CC0 checkbox on the chat submission form (§11.1) |
| Spam, vandalism, or low-quality dumps | All changes merge only via maintainer-approved, CI-gated PRs; contributor trust ladder; junk closed (§11.4) |
| Copyright complaint after publication | Documented takedown policy: prompt unpublish, reassess, purge from git history if needed (§11.2) |

---

## 9. Improvement backlog

Ideas beyond the core roadmap, roughly ordered by value-for-effort. Each becomes an OpenSpec
proposal when its time comes.

### Near-term (high value, modest effort)

1. **Side-by-side reader** — scan page ↔ transcription ↔ translation in synced columns
   (Wikisource-style). Requires keeping a page/paragraph alignment map during transcription,
   which the pipeline has anyway. This is the single biggest UX differentiator.
2. **Per-paragraph error reporting** — a small link on every paragraph that opens a prefilled
   GitHub issue (work, file, paragraph anchor, quoted text). Turns readers into proofreaders and
   feeds the status ladder.
3. **Citation support** — stable per-paragraph anchors + a "Cite" button emitting BibTeX/CSL for
   both the original work and our transcription (with commit hash for reproducibility).
4. **Author pages** — bio line, portrait (PD), death/birth dates with the copyright status
   derived from them, Wikidata link, list of works on the site.
5. **RSS/Atom feed + "recently published/updated"** — cheap, and the natural way for an audience
   to follow a growing corpus.
6. **Revision history on each work page** — rendered from git log: "eq. 12 corrected (2026-08)",
   status promotions, model re-runs. Builds trust; zero extra bookkeeping.

### Medium-term

7. **Accessibility & SEO for math** — render KaTeX with MathML output (screen-reader friendly),
   schema.org `CreativeWork`/`Person` metadata, OpenGraph cards, sitemap.
8. **EPUB export** alongside the Tectonic PDFs — old texts are exactly what people read on
   e-readers; pandoc in the same CI job.
9. **Bulk corpus download** — zip/JSONL export of the whole corpus (CC0). Makes the site a
   *dataset* for historians and researchers, not just a website; likely the main driver of
   inbound links.
10. **Glossary pages** — the per-era terminology glossaries from §4.2 published as browsable
    pages ("how we translate *Mannigfaltigkeit*"), doubling as translator documentation.
11. **Translation back-check** — cheap QA pass: back-translate a sample with a small model and
    flag divergences for the reviewer; feeds `skimmed` promotion.
12. **Curated collections / reading paths** — "The birth of non-Euclidean geometry", "Origins of
    statistical mechanics": ordered lists of works with one paragraph of editorial context each.

### Later / aspirational

13. **Cross-reference graph** — when work A cites work B and both are on the site, link them;
    eventually a browsable citation graph of the corpus.
14. **Facing-notation notes** — optional annotations where archaic notation differs from modern
    convention (kept strictly separate from the faithful transcription).
15. **Community "adopt a text" workflow** — contributors claim a work, run the pipeline on their
    own AI key/subscription (§7.4), review it, and get credited in provenance; contributor guide +
    CI make this safe. This is also the primary cost-reduction lever, so it deserves promotion
    into the core roadmap once the pipeline is stable.
16. **Multiple translation languages** — the corpus format already supports `translations/<lang>.tex`;
    add when demand appears.
17. **Statistics page** — works, pages, formulas transcribed, status distribution, model
    breakdown; fun and good for progress posts.

---

## 9a. Browse & filter (catalog facets)

Visitors must be able to slice the catalog, not just scroll it. Because the site is static, all
filtering is **client-side over a pre-built JSON index** (Astro emits `catalog.json` at build
time from every `work.yaml`; the browser filters it — no server, no database). This scales fine
to thousands of works.

### Facets

| Facet | Type | Source field(s) in `work.yaml` |
|---|---|---|
| **Author** | multi-select (with search) | `authors[].name` + `authors[].wikidata_id` (id disambiguates namesakes) |
| **Timeline** | range slider + histogram | `publication.year` (brushable; also feeds a timeline view) |
| **Journal / venue** | multi-select | `publication.venue` (journal, book publisher, academy proceedings, or "manuscript") |
| **Discipline** | multi-select | `discipline` (mathematics, physics; sub-tags: geometry, number theory, mechanics, thermodynamics, …) |
| **Original language** | multi-select | `language` (de, fr, la, en, it, …) |
| **Available translations** | multi-select | keys of `translations` (e.g. "has English") |
| **Quality status** | multi-select | max `status` across artifacts (ai-draft → verified) — lets readers show only verified texts |
| **Content type** | multi-select | `type` (paper, book, chapter, letter, lecture) |

Free-text search (Pagefind, §3) runs alongside the facets. Facet state lives in the URL query
string so a filtered view is shareable and bookmarkable.

### Views

- **List/grid** (default) — filtered catalog with author, title, year, venue, status badge.
- **Timeline** — works plotted on a horizontal time axis, grouped by discipline; a compelling
  landing view for a history-of-science project ("see the 1820s–1840s flowering of analysis").
- **By author** — the author pages (backlog #4) double as a pre-filtered catalog view.

### Metadata requirement

The facets are only as good as the metadata, so `work.yaml` gains structured, controlled-vocabulary
fields — `discipline`, sub-tags, `publication.venue`, `type`, `language` — validated in CI against
an allowed-values list (`corpus/vocab.yaml`) to prevent drift ("Ann. d. Physik" vs "Annalen der
Physik"). Venue and discipline normalization is part of the `corpus-format` spec (§5).

---

## 10. Contributor workflow — instructions per tier

Deliverables: a `CONTRIBUTING.md` in the repo and a friendlier **"Contribute" page on the site**,
both offering entry points sorted by effort. The lowest tiers require no coding and no API key —
any AI chat subscription (Claude app, ChatGPT, Gemini) is enough.

| Tier | Who | What they do | What they need |
|---|---|---|---|
| 0 — Report errors | Any reader | Click "report an error" on a paragraph; prefilled GitHub issue | GitHub account |
| 1 — Chat transcription | Anyone with an AI chat subscription | Copy our pinned prompt, upload scan pages in their own chat app, paste the LaTeX back to us via an issue form | AI subscription + GitHub account; **no coding** |
| 2 — Claude Code skill | Claude Pro/Max users, terminal-comfortable | `/transcribe <work> <pages>` runs the pipeline semi-automatically and opens a PR | Claude Code + git |
| 3 — Full pipeline | Technical contributors | Run `pipeline/` scripts on their own API key (Batch API), full provenance emitted, PR | API key + Python |

### Tier 1 in detail (the on-ramp that matters most)

- `prompts/transcribe-chat.md` and `prompts/translate-chat.md`: **self-contained copy-paste
  prompts**, kept in sync with the pipeline's `prompt_version`, instructing the model to output
  LaTeX in our house style (macros, structure, "transcribe faithfully, don't modernize" rules).
- Step-by-step instructions: pick an unclaimed work (or propose one — with scan link, author
  death date, publication date so the copyright gate can be pre-checked); do a few pages per
  message; eyeball that formulas render (Overleaf, or a snippet-renderer page on our site later).
- Submission via a **GitHub issue form** (structured template): work, pages covered, model/app
  used (self-reported provenance), the LaTeX output pasted or attached.
- A maintainer — or later a small CI bot — assembles submissions into the corpus format.
  Provenance records `submitted_via: chat` and the self-reported model; status starts at
  `ai-draft`; a reviewer runs the verification pass on their own AI account (§7.4) and the normal
  review flow takes it from there.
- **Credit**: contributors are named in `provenance.yaml` and on the work page. Recognition is
  the currency of volunteer projects — make it visible from day one.

### Claiming and coordination

A simple `corpus/CLAIMS.md` (or GitHub issue labels) tracks who is working on what, preventing
duplicate effort. Claims expire after e.g. 60 days of inactivity. "Good first texts" (short,
clean antiqua print, papers not books) get a label to funnel newcomers to winnable tasks.

---

## 11. Governance, legal & community

### 11.1 Licensing & contribution mechanism

- **Two licenses, cleanly separated:** site/pipeline **code** under an OSI license (MIT or
  Apache-2.0); **corpus content** under **CC0** (§2.4).
- **How CC0 is actually secured:** every contribution carries a **DCO `Signed-off-by`** asserting
  the contributor made the submission and releases it CC0 — CI enforces the sign-off on PRs. The
  tier-1 chat issue form includes an explicit "I release this under CC0" checkbox. No CLA
  paperwork.

### 11.2 Takedown & complaints

- A public **takedown policy** + contact address. On a credible claim (still in copyright in some
  jurisdiction, a protected critical edition, personality/moral rights), we **unpublish promptly**
  pending review, then reassess with the two-date gate and sourcing (§2.5). Because content is in
  git, unpublishing is removing it from the build — and, where required, purging it from history.
  Every decision is logged. Posture: good-faith, err-on-the-safe-side.

### 11.3 Legal pages & disclaimer

- **About**, **Contact**, and a **Copyright/Disclaimer** page: how we assess public-domain status,
  a clear statement that this is good-faith practice and **not legal advice**, the takedown path,
  and the CC0 status of our output. Ships in Phase 2.

### 11.4 Contribution moderation & trust

- **Nothing auto-publishes** — every change merges only via a maintainer-approved, CI-gated PR.
- **Trust ladder for people** (mirroring the quality ladder for texts): newcomers get full review;
  consistent, reliable contributors earn lighter-touch review and, eventually, triage/merge
  rights. This scales review capacity as the community grows.
- **Spam/vandalism:** PRs and issue forms are maintainer-moderated; obvious junk is closed, repeat
  abuse blocked. The attack surface is small — the site is static and every change is reviewed.

### 11.5 Privacy & analytics

- EU-run public site → **cookieless, privacy-respecting analytics** (e.g. Plausible / GoatCounter)
  or none at all: no cookie banner, no personal data, GDPR-trivial. No visitor accounts (non-goal).

### 11.6 Continuity (bus factor)

- The corpus and code live in git, so they're inherently backed up and CC0-forkable. Add an
  **off-GitHub mirror** (e.g. Codeberg or a periodic archived export) and a short "how to build /
  take over this project" document, so a single-maintainer outage is never fatal.
