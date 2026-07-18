#!/usr/bin/env python3
"""Warn-only cross-check of author death years against Wikidata.

Run in CI as an informational step (never blocks the build). For each author with a
`wikidata_id` (Q…), fetch the death date from Wikidata and warn on a mismatch with the
death_year recorded in work.yaml. Requires network; uses only the standard library.

Usage:
    python pipeline/wikidata_check.py [--corpus corpus]
Exit code is always 0 (warnings go to stdout); pass --strict to exit 1 on any mismatch.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

import yaml

WD_ENTITY = "https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
DEATH_PROP = "P570"


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def wikidata_death_year(qid: str, timeout: float = 15.0) -> int | None:
    url = WD_ENTITY.format(qid=qid)
    with urllib.request.urlopen(url, timeout=timeout) as resp:  # noqa: S310 (trusted host)
        data = json.load(resp)
    claims = data.get("entities", {}).get(qid, {}).get("claims", {})
    for claim in claims.get(DEATH_PROP, []):
        try:
            t = claim["mainsnak"]["datavalue"]["value"]["time"]  # e.g. "+1866-07-20T00:00:00Z"
            return int(t.lstrip("+")[:4])
        except (KeyError, ValueError):
            continue
    return None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Cross-check death years against Wikidata (warn-only).")
    p.add_argument("--corpus", default="corpus")
    p.add_argument("--strict", action="store_true", help="exit 1 on any mismatch")
    args = p.parse_args(argv)

    corpus = Path(args.corpus)
    mismatches = 0
    for wp in sorted(corpus.glob("*/work.yaml")):
        work = load_yaml(wp) or {}
        for a in work.get("authors") or []:
            qid, recorded = a.get("wikidata_id"), a.get("death_year")
            if not qid or recorded is None:
                continue
            try:
                wd = wikidata_death_year(qid)
            except Exception as exc:  # network hiccup — never fatal
                print(f"WARN  {work.get('id')}: could not query {qid} ({exc})")
                continue
            if wd is not None and wd != recorded:
                mismatches += 1
                print(f"WARN  {work.get('id')}: {a.get('name')} death_year={recorded} "
                      f"but Wikidata {qid}={wd}")
            else:
                print(f"OK    {work.get('id')}: {a.get('name')} death_year={recorded} matches {qid}")

    print(f"\n{mismatches} mismatch(es).")
    return 1 if (args.strict and mismatches) else 0


if __name__ == "__main__":
    sys.exit(main())
