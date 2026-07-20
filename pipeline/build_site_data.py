#!/usr/bin/env python3
"""Bundle everything the static site needs into one JSON file.

Writes site/src/data/works.json: for every public-domain work at/above the minimum status,
the full metadata plus the transcription/translation LaTeX text and provenance summary. The
Astro site builds the catalog (browse/filter) and the per-work pages from this single file,
so the site build has no other dependency on the corpus layout.

Usage:
    python pipeline/build_site_data.py [--corpus corpus]
        [--out site/src/data/works.json] [--min-status ai-draft] [--now-year YYYY]
"""
from __future__ import annotations

import argparse
import datetime
import json
import shutil
from pathlib import Path

from build_catalog import max_status  # type: ignore
from validate import STATUS_LADDER, evaluate_copyright, load_yaml  # type: ignore


def read_text(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.exists() else None


def write_tex_copy(tex_root: Path | None, work_id: str, name: str, text: str | None) -> str | None:
    """Copy a source .tex into the site's public/ so it can be downloaded, return its URL.

    The corpus .tex is the faithful, compilable artifact; we expose it for download (curl-able,
    right-clickable) rather than only rendering a simplified HTML view. Emitted at build time,
    never committed (site/public/tex is git-ignored).
    """
    if tex_root is None or text is None:
        return None
    dest = tex_root / work_id / f"{name}.tex"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return f"/tex/{work_id}/{name}.tex"


def pdf_url(pdf_root: Path, work_id: str, name: str) -> str | None:
    """Return the public URL for a compiled PDF if it exists, else None.

    PDFs are built by pipeline/build_pdfs.py into site/public/pdf/<id>/<name>.pdf during the
    CI deploy (never committed). If they aren't built (e.g. local dev without Tectonic), the
    work page simply omits the download link.
    """
    if pdf_root and (pdf_root / work_id / f"{name}.pdf").exists():
        return f"/pdf/{work_id}/{name}.pdf"
    return None


def copy_figures(fig_root: Path | None, work_dir: Path, work_id: str) -> None:
    """Copy a work's figure crops into the site's public/ so they can be served."""
    src = work_dir / "figures"
    if fig_root is None or not src.is_dir():
        return
    dest = fig_root / work_id
    dest.mkdir(parents=True, exist_ok=True)
    for img in src.iterdir():
        if img.is_file():
            shutil.copyfile(img, dest / img.name)


def build(corpus_dir: Path, now_year: int, min_status: str,
          pdf_root: Path | None = None, tex_root: Path | None = None,
          fig_root: Path | None = None) -> dict:
    vocab = load_yaml(corpus_dir / "vocab.yaml") or {}
    min_rank = STATUS_LADDER.index(min_status)
    works = []

    # Make the shared preamble downloadable alongside sources, so a downloaded .tex compiles.
    if tex_root is not None:
        preamble = corpus_dir / "preamble" / "readmasters.sty"
        if preamble.exists():
            tex_root.mkdir(parents=True, exist_ok=True)
            (tex_root / "readmasters.sty").write_text(
                preamble.read_text(encoding="utf-8"), encoding="utf-8")

    for wd in sorted(corpus_dir.iterdir()):
        wp = wd / "work.yaml"
        if not wd.is_dir() or not wp.exists():
            continue
        work = load_yaml(wp) or {}
        prov = load_yaml(wd / "provenance.yaml") if (wd / "provenance.yaml").exists() else {}
        if not evaluate_copyright(work, prov, now_year)["public_domain"]:
            continue
        status = max_status(prov)
        if STATUS_LADDER.index(status) < min_rank:
            continue

        copy_figures(fig_root, wd, work["id"])
        pub = work.get("publication") or {}
        translations = {}
        for lang in sorted((prov.get("translations") or {}).keys()):
            t_tex = read_text(wd / "translations" / f"{lang}.tex")
            translations[lang] = {
                "label": (vocab.get("languages") or {}).get(lang, lang),
                "tex": t_tex,
                "tex_url": write_tex_copy(tex_root, work["id"], lang, t_tex),
                "provenance": prov["translations"][lang],
                "pdf": pdf_url(pdf_root, work["id"], lang),
            }

        works.append({
            "id": work["id"],
            "title": work.get("title"),
            "title_en": work.get("title_en"),
            "authors": work.get("authors") or [],
            "year": pub.get("year"),
            "venue": pub.get("venue"),
            "venue_label": (vocab.get("venues") or {}).get(pub.get("venue")),
            "volume": pub.get("volume"),
            "pages": pub.get("pages"),
            "publication_full": pub.get("title_full"),
            "significance": work.get("significance"),
            "significance_sources": work.get("significance_sources") or [],
            "discipline": work.get("discipline"),
            "discipline_label": (vocab.get("disciplines") or {}).get(work.get("discipline")),
            "tags": work.get("tags") or [],
            "tag_labels": [(vocab.get("tags") or {}).get(t, t) for t in (work.get("tags") or [])],
            "language": work.get("language"),
            "language_label": (vocab.get("languages") or {}).get(work.get("language")),
            "type": work.get("type"),
            "type_label": (vocab.get("types") or {}).get(work.get("type")),
            "source": work.get("source") or {},
            "sources": work.get("sources") or {},
            "edition": work.get("edition") or {},
            "copyright_assessment": work.get("copyright_assessment"),
            "status": status,
            "original_tex": (orig_tex := read_text(wd / "original.tex")),
            "original_tex_url": write_tex_copy(tex_root, work["id"], "original", orig_tex),
            "original_pdf": pdf_url(pdf_root, work["id"], "original"),
            "transcription_provenance": prov.get("transcription"),
            "translations": translations,
            "translation_langs": sorted(translations.keys()),
            "external_translations": work.get("external_translations") or [],
            "url": f"/works/{work['id']}/",
        })

    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "vocab": vocab,
        "count": len(works),
        "works": works,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Bundle site data JSON.")
    p.add_argument("--corpus", default="corpus")
    p.add_argument("--out", default="site/src/data/works.json")
    p.add_argument("--min-status", default="ai-draft", choices=STATUS_LADDER)
    p.add_argument("--now-year", type=int, default=datetime.date.today().year)
    args = p.parse_args(argv)

    out = Path(args.out)
    # PDFs and .tex copies live under <site>/public/, two levels above src/data/works.json.
    site_public = out.parents[2] / "public" if len(out.parents) >= 3 else None
    pdf_root = site_public / "pdf" if site_public else None
    tex_root = site_public / "tex" if site_public else None
    fig_root = site_public / "figures" if site_public else None
    data = build(Path(args.corpus), args.now_year, args.min_status, pdf_root, tex_root, fig_root)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out}: {data['count']} work(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
