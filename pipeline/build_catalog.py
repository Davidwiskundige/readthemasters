#!/usr/bin/env python3
"""Build catalog.json — the browse/filter index the site consumes.

Reads every work.yaml + provenance.yaml, resolves vocabulary labels, and emits a single
JSON file the static site filters client-side (PLAN.md §9a). Only works that pass the
copyright gate and meet the minimum status are included.

Usage:
    python pipeline/build_catalog.py [--corpus corpus] [--out catalog.json]
                                     [--min-status ai-draft] [--now-year YYYY]
"""
from __future__ import annotations

import argparse
import datetime
import json
from pathlib import Path

import yaml

from validate import STATUS_LADDER, evaluate_copyright, load_yaml  # type: ignore


def max_status(provenance: dict) -> str:
    """Highest status across all artifacts (ladder order)."""
    ranks = []
    if provenance.get("transcription"):
        ranks.append(provenance["transcription"].get("status"))
    for rec in (provenance.get("translations") or {}).values():
        ranks.append((rec or {}).get("status"))
    ranks = [s for s in ranks if s in STATUS_LADDER]
    if not ranks:
        return "ai-draft"
    return max(ranks, key=STATUS_LADDER.index)


def build(corpus_dir: Path, now_year: int, min_status: str) -> dict:
    vocab = load_yaml(corpus_dir / "vocab.yaml") or {}
    min_rank = STATUS_LADDER.index(min_status)
    works = []

    for wd in sorted(corpus_dir.iterdir()):
        wp = wd / "work.yaml"
        if not wd.is_dir() or not wp.exists():
            continue
        work = load_yaml(wp) or {}
        prov = load_yaml(wd / "provenance.yaml") if (wd / "provenance.yaml").exists() else {}

        assessment = evaluate_copyright(work, prov, now_year)
        if not assessment["public_domain"]:
            continue  # never index a non-PD work

        status = max_status(prov)
        if STATUS_LADDER.index(status) < min_rank:
            continue

        pub = work.get("publication") or {}
        translations = sorted((prov.get("translations") or {}).keys())
        works.append({
            "id": work["id"],
            "title": work.get("title"),
            "title_en": work.get("title_en"),
            "authors": [
                {"name": a.get("name"), "wikidata_id": a.get("wikidata_id"),
                 "death_year": a.get("death_year")}
                for a in (work.get("authors") or [])
            ],
            "year": pub.get("year"),
            "venue": pub.get("venue"),
            "venue_label": (vocab.get("venues") or {}).get(pub.get("venue")),
            "discipline": work.get("discipline"),
            "discipline_label": (vocab.get("disciplines") or {}).get(work.get("discipline")),
            "tags": work.get("tags") or [],
            "tag_labels": [(vocab.get("tags") or {}).get(t, t) for t in (work.get("tags") or [])],
            "language": work.get("language"),
            "language_label": (vocab.get("languages") or {}).get(work.get("language")),
            "type": work.get("type"),
            "type_label": (vocab.get("types") or {}).get(work.get("type")),
            "translations": translations,
            "status": status,
            "url": f"/works/{work['id']}/",
        })

    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "count": len(works),
        "works": works,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Build catalog.json for the site.")
    p.add_argument("--corpus", default="corpus")
    p.add_argument("--out", default="catalog.json")
    p.add_argument("--min-status", default="ai-draft", choices=STATUS_LADDER)
    p.add_argument("--now-year", type=int, default=datetime.date.today().year)
    args = p.parse_args(argv)

    catalog = build(Path(args.corpus), args.now_year, args.min_status)
    Path(args.out).write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.out}: {catalog['count']} work(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
