#!/usr/bin/env python3
"""ReadTheMastersAI corpus validator — the copyright gate.

Validates every work under corpus/ against the schema, the controlled vocabulary, the
copyright rules (PLAN.md §2), sourced-facts requirements (§2.5), and status/provenance
consistency. Exits non-zero on any violation, so CI blocks publication of anything that
does not pass.

Usage:
    python pipeline/validate.py [--corpus DIR] [--strict-pma-100] [--now-year YYYY]
                                [--write] [--min-status STATUS]

--write recomputes and rewrites each work.yaml's copyright_assessment block (maintainer
convenience; reformats the file). Without it, the stored assessment must match the
recomputation or the gate fails (prevents stale or forged assessments).
"""
from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

import yaml

# Copyright terms (years).
PMA_TERM = 70          # life + 70 (most of the world)
US_TERM = 95           # US: 95 years after publication
PMA_STRICT_TERM = 100  # optional strict mode (e.g. Mexico)

STATUS_LADDER = ["ai-draft", "spot-checked", "proofread", "validated"]
EFFORT_VALUES = {
    "low", "medium", "high", "xhigh", "max",   # API effort levels
    "adaptive", "extended", "standard",         # provider-agnostic / chat
}


class Issues:
    """Collects errors (block publication) and warnings (informational)."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")

    @property
    def ok(self) -> bool:
        return not self.errors


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# --------------------------------------------------------------------------- #
# Copyright rules
# --------------------------------------------------------------------------- #
def _rule(verdict: bool, inputs: dict) -> dict:
    return {"verdict": "pass" if verdict else "fail", "inputs": inputs}


def evaluate_copyright(work: dict, provenance: dict, now_year: int,
                       strict_pma_100: bool = False) -> dict:
    """Compute the copyright assessment from the work's (sourced) facts.

    Returns a dict shaped like the stored `copyright_assessment` block.
    """
    authors = work.get("authors", []) or []
    pub_year = (work.get("publication") or {}).get("year")
    edition = work.get("edition") or {}

    # pma_70 — every author must clear life + 70 (Jan-1 rollover => +1).
    death_years = []
    pma_ok = True
    for a in authors:
        dy = a.get("death_year")
        death_years.append(dy)
        if a.get("anonymous"):
            # Anonymous: PD 70 years after publication.
            author_ok = pub_year is not None and now_year >= pub_year + PMA_TERM + 1
        elif dy is not None:
            author_ok = now_year >= dy + PMA_TERM + 1
        else:
            # Unknown death date, not anonymous: only clears if the work is old
            # enough that any plausible lifespan (<=100y past publication) is covered.
            author_ok = pub_year is not None and now_year >= pub_year + PMA_TERM + 100
        pma_ok = pma_ok and author_ok

    # us_publication — 95 years after first publication (Jan-1 rollover => +1).
    us_ok = pub_year is not None and now_year >= pub_year + US_TERM + 1

    # edition_rights.
    edition_ok = bool(edition.get("rights_cleared")) and bool(edition.get("rights_note"))

    # translation_source — a hosted translation must derive from our transcription, or be imported
    # from a public-domain/openly-licensed translation (source: external-open + a license). A
    # still-copyrighted translation (source: external) is a violation.
    external = 0
    for _lang, rec in ((provenance or {}).get("translations") or {}).items():
        rec = rec or {}
        src = rec.get("source")
        if src in (None, "transcription"):
            continue
        if src == "external-open" and rec.get("license"):
            continue
        external += 1  # "external" (copyrighted), or "external-open" without a named license
    trans_ok = external == 0

    evaluated = {
        "pma_70": _rule(pma_ok, {"death_years": death_years, "term": PMA_TERM}),
        "us_publication": _rule(us_ok, {"publication_year": pub_year, "term": US_TERM}),
        "edition_rights": _rule(edition_ok, {"rights_cleared": bool(edition.get("rights_cleared"))}),
        "translation_source": _rule(trans_ok, {"external_translations": external}),
    }
    public_domain = pma_ok and us_ok and edition_ok and trans_ok

    if strict_pma_100:
        strict_ok = all(
            (a.get("death_year") is not None and now_year >= a["death_year"] + PMA_STRICT_TERM + 1)
            for a in authors
        )
        evaluated["pma_100"] = _rule(strict_ok, {"term": PMA_STRICT_TERM})
        public_domain = public_domain and strict_ok

    return {
        "public_domain": public_domain,
        "evaluated": evaluated,
        "evaluated_at": datetime.date.today().isoformat(),
    }


# --------------------------------------------------------------------------- #
# Schema + vocabulary + provenance checks
# --------------------------------------------------------------------------- #
def check_schema_and_vocab(work: dict, vocab: dict, work_id: str, issues: Issues) -> None:
    w = f"{work_id}/work.yaml"

    for field in ("id", "title", "authors", "publication", "edition",
                  "discipline", "language", "type", "source", "sources"):
        if field not in work or work[field] in (None, "", []):
            issues.error(w, f"missing required field '{field}'")

    if work.get("id") != work_id:
        issues.error(w, f"id '{work.get('id')}' must equal directory name '{work_id}'")

    for i, a in enumerate(work.get("authors") or []):
        if not a.get("name"):
            issues.error(w, f"authors[{i}] missing name")
        if "death_year" not in a and not a.get("anonymous"):
            issues.error(w, f"authors[{i}] needs death_year or anonymous:true")

    pub = work.get("publication") or {}
    if not isinstance(pub.get("year"), int):
        issues.error(w, "publication.year must be an integer")
    if pub.get("venue") not in (vocab.get("venues") or {}):
        issues.error(w, f"publication.venue '{pub.get('venue')}' not in vocab.venues")

    disc = work.get("discipline")
    disc_list = disc if isinstance(disc, list) else [disc]
    if not disc_list:
        issues.error(w, "discipline is required")
    for dd in disc_list:
        if dd not in (vocab.get("disciplines") or {}):
            issues.error(w, f"discipline '{dd}' not in vocab.disciplines")
    for tag in work.get("tags") or []:
        if tag not in (vocab.get("tags") or {}):
            issues.error(w, f"tag '{tag}' not in vocab.tags")
    if work.get("language") not in (vocab.get("languages") or {}):
        issues.error(w, f"language '{work.get('language')}' not in vocab.languages")
    if work.get("type") not in (vocab.get("types") or {}):
        issues.error(w, f"type '{work.get('type')}' not in vocab.types")

    # Sourced facts (§2.5).
    sources = work.get("sources") or {}
    if not sources.get("publication_date"):
        issues.error(w, "sources.publication_date is required (an unsourced publication date fails the gate)")
    if not sources.get("edition"):
        issues.error(w, "sources.edition is required")
    if not sources.get("death_date"):
        issues.warn(w, "sources.death_date missing (blocks the Wikidata cross-check)")


def check_provenance(provenance: dict, work_id: str, issues: Issues) -> None:
    w = f"{work_id}/provenance.yaml"
    if not provenance:
        issues.error(w, "provenance.yaml is empty or missing")
        return

    artifacts = []
    if "transcription" in provenance:
        artifacts.append(("transcription", provenance["transcription"]))
    for lang, rec in (provenance.get("translations") or {}).items():
        artifacts.append((f"translations.{lang}", rec))

    if not artifacts:
        issues.error(w, "no artifacts (need a transcription and/or translations)")

    for name, rec in artifacts:
        rec = rec or {}
        status = rec.get("status")
        if status not in STATUS_LADDER:
            issues.error(w, f"{name}: status '{status}' not in {STATUS_LADDER}")
        if not rec.get("model"):
            issues.error(w, f"{name}: model is required")
        if not rec.get("prompt_version"):
            issues.error(w, f"{name}: prompt_version is required")
        effort = rec.get("effort")
        if effort is not None and effort not in EFFORT_VALUES:
            issues.error(w, f"{name}: effort '{effort}' not in {sorted(EFFORT_VALUES)} (or null)")
        if status == "validated":
            reviewers = rec.get("reviewers") or []
            distinct = {r.get("name") for r in reviewers}
            if len(distinct) < 2:
                issues.error(w, f"{name}: status 'validated' requires >= 2 distinct reviewers")


def rule_verdicts(assessment: dict) -> dict:
    """Extract {rule: verdict, 'public_domain': bool} for comparison."""
    out = {"public_domain": assessment.get("public_domain")}
    for rule, body in (assessment.get("evaluated") or {}).items():
        out[rule] = (body or {}).get("verdict")
    return out


# --------------------------------------------------------------------------- #
# Per-work + corpus driver
# --------------------------------------------------------------------------- #
def validate_work(work_dir: Path, vocab: dict, now_year: int,
                  strict_pma_100: bool, issues: Issues, write: bool = False) -> None:
    work_id = work_dir.name
    work_path = work_dir / "work.yaml"
    prov_path = work_dir / "provenance.yaml"

    if not work_path.exists():
        issues.error(work_id, "missing work.yaml")
        return
    work = load_yaml(work_path) or {}
    provenance = load_yaml(prov_path) if prov_path.exists() else {}

    check_schema_and_vocab(work, vocab, work_id, issues)
    check_provenance(provenance, work_id, issues)

    computed = evaluate_copyright(work, provenance, now_year, strict_pma_100)

    if write:
        work["copyright_assessment"] = computed
        with work_path.open("w", encoding="utf-8") as fh:
            yaml.safe_dump(work, fh, allow_unicode=True, sort_keys=False)
    else:
        stored = work.get("copyright_assessment")
        if stored is None:
            issues.error(f"{work_id}/work.yaml",
                         "missing copyright_assessment (run with --write, then review)")
        elif rule_verdicts(stored) != rule_verdicts(computed):
            issues.error(f"{work_id}/work.yaml",
                         f"copyright_assessment is stale/incorrect: stored {rule_verdicts(stored)} "
                         f"!= computed {rule_verdicts(computed)}")

    if not computed["public_domain"]:
        failed = [r for r, b in computed["evaluated"].items() if b["verdict"] == "fail"]
        issues.error(work_id, f"NOT public domain — failing rules: {', '.join(failed)}. "
                              f"This work cannot be published.")


def validate_corpus(corpus_dir: Path, now_year: int, strict_pma_100: bool = False,
                    write: bool = False) -> Issues:
    issues = Issues()
    vocab_path = corpus_dir / "vocab.yaml"
    if not vocab_path.exists():
        issues.error("corpus", "vocab.yaml missing")
        return issues
    vocab = load_yaml(vocab_path) or {}

    work_dirs = sorted(
        d for d in corpus_dir.iterdir()
        if d.is_dir() and (d / "work.yaml").exists()
    )

    seen_ids: dict[str, str] = {}
    for wd in work_dirs:
        validate_work(wd, vocab, now_year, strict_pma_100, issues, write=write)
        # Cross-work: unique ids.
        if (wd / "work.yaml").exists():
            wid = (load_yaml(wd / "work.yaml") or {}).get("id")
            if wid in seen_ids:
                issues.error(wd.name, f"duplicate id '{wid}' (also in {seen_ids[wid]})")
            elif wid:
                seen_ids[wid] = wd.name

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the corpus (the copyright gate).")
    parser.add_argument("--corpus", default="corpus", help="corpus directory (default: corpus)")
    parser.add_argument("--strict-pma-100", action="store_true",
                        help="also require life + 100 (e.g. Mexico)")
    parser.add_argument("--now-year", type=int, default=datetime.date.today().year,
                        help="override the current year (for reproducible checks/tests)")
    parser.add_argument("--write", action="store_true",
                        help="recompute and rewrite each work.yaml copyright_assessment")
    args = parser.parse_args(argv)

    corpus_dir = Path(args.corpus)
    if not corpus_dir.exists():
        print(f"error: corpus directory '{corpus_dir}' does not exist", file=sys.stderr)
        return 2

    issues = validate_corpus(corpus_dir, args.now_year, args.strict_pma_100, args.write)

    for w in issues.warnings:
        print(f"WARN  {w}")
    for e in issues.errors:
        print(f"ERROR {e}")

    n_works = sum(1 for d in corpus_dir.iterdir() if d.is_dir() and (d / "work.yaml").exists())
    if issues.ok:
        print(f"\nOK — {n_works} work(s) pass the copyright gate.")
        return 0
    print(f"\nFAILED — {len(issues.errors)} error(s) across {n_works} work(s). "
          f"Nothing publishes until these are fixed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
