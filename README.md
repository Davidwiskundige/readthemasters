# ReadTheMastersAI

A website that publishes **AI transcriptions (LaTeX)** and **AI translations (LaTeX)** of old
mathematics and physics texts — with the original source always cited, and **only** for texts that
are in the public domain worldwide.

- **Faithful transcriptions** of landmark works into clean LaTeX (original language).
- **Readable translations** (starting with English), made only from our own public-domain
  transcriptions.
- **Auditable copyright** — every published text carries a machine-checkable, sourced assessment
  using both the author's death date (life + 70) and the first-publication date (US 95-year rule).
- **Open corpus (CC0)** — usable as a dataset, not just a website.
- **Community-powered at ~zero project cost** — contributors run the pipeline on their own AI
  accounts (see [CONTRIBUTING.md](CONTRIBUTING.md)); the project pays only for a domain name.

See [PLAN.md](PLAN.md) for the full design.

## Repository layout

```
corpus/            The texts. One folder per work: work.yaml + original.tex + translations/
  vocab.yaml       Controlled vocabulary for metadata facets (disciplines, venues, types, langs)
  preamble/        Shared LaTeX house style (readmasters.sty)
pipeline/          Python: validation (the copyright gate), catalog build, Wikidata check
  validate.py        Copyright gate + schema + vocabulary + status/provenance checks
  build_catalog.py   Emits catalog.json for the site's browse/filter
  tests/             Test suite for the validator
prompts/           Pinned copy-paste prompts contributors use in their own AI app
openspec/          Spec-driven development: project conventions, change proposals, archive
site/              Astro static site (catalog, work pages, browse/filter, legal pages)
.github/           CI (copyright gate + LaTeX compile) and the contribution issue form
```

## Quick start (maintainers)

```bash
# 1. Install the validator's one dependency
pip install -r pipeline/requirements.txt

# 2. Validate the whole corpus (this is the copyright gate — it must pass to publish)
python pipeline/validate.py

# 3. Build the catalog index the site consumes
python pipeline/build_catalog.py

# 4. Run the tests
python -m pytest pipeline/tests -q
```

## Licensing

- **Code** (everything under `pipeline/`, `site/`, `.github/`): MIT — see [LICENSE](LICENSE).
- **Corpus content** (everything under `corpus/`): CC0 1.0 — see [LICENSE-CONTENT](LICENSE-CONTENT).

Contributions are accepted under these licenses via a Developer Certificate of Origin sign-off;
see [CONTRIBUTING.md](CONTRIBUTING.md).

> Public-domain assessments here are made in good faith and are **not legal advice**. If you
> believe a work is published in error, see the [Copyright & takedown page](site/src/pages/copyright.md)
> for the takedown process.
