#!/usr/bin/env python3
"""Compile each work's LaTeX to PDF with Tectonic (deploy-time, not committed).

For every public-domain work at/above the minimum status, compile original.tex and each
translations/<lang>.tex into site/public/pdf/<id>/<name>.pdf. Astro copies public/ into the
build output, so the PDFs are served at /pdf/<id>/<name>.pdf. Nothing here is committed to git
(site/public/pdf is git-ignored); PDFs are regenerated on every deploy.

Requires the `tectonic` binary on PATH (https://tectonic-typesetting.github.io/). Works that
already ship a pre-made PDF override (corpus/<id>/pdf/<name>.pdf) are copied instead of compiled.

Usage:
    python pipeline/build_pdfs.py [--corpus corpus] [--out site/public/pdf]
        [--min-status ai-draft] [--now-year YYYY] [--only ID]
"""
from __future__ import annotations

import argparse
import datetime
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from build_catalog import max_status  # type: ignore
from validate import STATUS_LADDER, evaluate_copyright, load_yaml  # type: ignore


def have_tectonic() -> bool:
    return shutil.which("tectonic") is not None


def compile_one(tex: Path, out_pdf: Path) -> bool:
    """Compile a single .tex to out_pdf. Returns True on success."""
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        # --keep-logs off; -Z search-path lets \usepackage{readmasters} resolve the shared preamble.
        cmd = ["tectonic", "-X", "compile", str(tex), "--outdir", tmp,
               "-Z", "search-path=" + str(tex.parent),
               "-Z", "search-path=corpus/preamble"]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            sys.stderr.write(f"tectonic failed for {tex}:\n{proc.stderr[-1500:]}\n")
            return False
        produced = Path(tmp) / (tex.stem + ".pdf")
        if not produced.exists():
            sys.stderr.write(f"no PDF produced for {tex}\n")
            return False
        shutil.copyfile(produced, out_pdf)
        return True


def build(corpus_dir: Path, out_root: Path, now_year: int, min_status: str,
          only: str | None) -> int:
    min_rank = STATUS_LADDER.index(min_status)
    built = 0
    for wd in sorted(corpus_dir.iterdir()):
        wp = wd / "work.yaml"
        if not wd.is_dir() or not wp.exists():
            continue
        work = load_yaml(wp) or {}
        if only and work.get("id") != only:
            continue
        prov = load_yaml(wd / "provenance.yaml") if (wd / "provenance.yaml").exists() else {}
        if not evaluate_copyright(work, prov, now_year)["public_domain"]:
            continue
        if STATUS_LADDER.index(max_status(prov)) < min_rank:
            continue

        wid = work["id"]
        targets = [("original", wd / "original.tex")]
        for lang in (prov.get("translations") or {}):
            targets.append((lang, wd / "translations" / f"{lang}.tex"))

        for name, tex in targets:
            if not tex.exists():
                continue
            out_pdf = out_root / wid / f"{name}.pdf"
            override = wd / "pdf" / f"{name}.pdf"
            if override.exists():
                out_pdf.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(override, out_pdf)
                print(f"copied override {override} -> {out_pdf}")
                built += 1
            elif compile_one(tex, out_pdf):
                print(f"compiled {tex} -> {out_pdf}")
                built += 1
    return built


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Compile corpus PDFs with Tectonic.")
    p.add_argument("--corpus", default="corpus")
    p.add_argument("--out", default="site/public/pdf")
    p.add_argument("--min-status", default="ai-draft", choices=STATUS_LADDER)
    p.add_argument("--now-year", type=int, default=datetime.date.today().year)
    p.add_argument("--only", help="compile only this work id")
    args = p.parse_args(argv)

    if not have_tectonic():
        sys.stderr.write("WARN: tectonic not found on PATH; skipping PDF build. "
                         "The site still builds, just without PDF downloads.\n")
        return 0

    n = build(Path(args.corpus), Path(args.out), args.now_year, args.min_status, args.only)
    print(f"Built {n} PDF(s) into {args.out}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
