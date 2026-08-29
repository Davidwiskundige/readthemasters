#!/usr/bin/env python3
"""ReadTheMasters corpus validator — the copyright gate.

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
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import texcompare  # noqa: E402  (stdlib-only — keeps the gate AI-free)
import houselint  # noqa: E402  (stdlib-only — mechanical HOUSESTYLE.md checks)

# Copyright terms (years).
PMA_TERM = 70          # life + 70 (most of the world)
US_TERM = 95           # US: 95 years after publication
PMA_STRICT_TERM = 100  # optional strict mode (e.g. Mexico)

STATUS_LADDER = ["ai-draft", "skimmed", "verified"]
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


def add_changelog_entry(provenance: dict, summary: str, date: str | None = None) -> dict:
    """Seed a starter `{date, summary}` changelog entry, append-if-absent (by summary).

    Used by the transcription/translation pipelines and skills so a new artifact records its own
    first revision (PLAN.md §9 #4). Idempotent: re-running does not duplicate the entry, and any
    existing entries are preserved. Keeps `changelog` as the first key for readability.
    """
    date = date or datetime.date.today().isoformat()
    log = provenance.get("changelog")
    if not isinstance(log, list):
        log = []
    if not any(isinstance(e, dict) and e.get("summary") == summary for e in log):
        log = [*log, {"date": date, "summary": summary}]
    return {"changelog": log, **{k: v for k, v in provenance.items() if k != "changelog"}}


def _is_iso_date(value) -> bool:
    """True for an ISO calendar date — a `datetime.date` (YAML often parses one) or 'YYYY-MM-DD'."""
    if isinstance(value, datetime.date):
        return True
    if not isinstance(value, str):
        return False
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False


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
# Venue vocabulary (a venues entry may be a bare string or a metadata object)
# --------------------------------------------------------------------------- #
VENUE_KINDS = {"periodical", "book", "manuscript"}


def venue_label(vocab: dict, key) -> str | None:
    """Display label for a venue key: an object entry's `name`, else the bare string.

    A `corpus/vocab.yaml` venues entry may be either a bare string (the full title) or an object
    carrying journal metadata (name/aka/kind/founded/…/archives). Everything that reads a venue
    label — the catalog, citations, `venue_full`, the journal pages — resolves it through here, so
    both forms work identically.
    """
    entry = (vocab.get("venues") or {}).get(key)
    if isinstance(entry, dict):
        return entry.get("name")
    return entry


def check_venue_vocab(vocab: dict, issues: Issues) -> None:
    """Validate the structure of any object-form venues entries (corpus-format spec).

    Bare-string entries are always valid. An object entry MUST carry `name`, its `kind` (if set)
    MUST be one of periodical/book/manuscript, and every `archives[].url` MUST be an absolute
    http(s) URL. Called once per corpus run, not per work.
    """
    for key, entry in (vocab.get("venues") or {}).items():
        if not isinstance(entry, dict):
            continue  # bare string — the full title, valid as-is
        where = f"vocab.yaml venues.{key}"
        if not entry.get("name"):
            issues.error(where, "object venue entry must have a 'name'")
        kind = entry.get("kind")
        if kind is not None and kind not in VENUE_KINDS:
            issues.error(where, f"kind '{kind}' not in {sorted(VENUE_KINDS)}")
        for i, arc in enumerate(entry.get("archives") or []):
            url = (arc or {}).get("url") if isinstance(arc, dict) else None
            if not (isinstance(url, str) and url.startswith(("http://", "https://"))):
                issues.error(where, f"archives[{i}].url must be an absolute http(s) URL")


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

    # Optional changelog (source of the work page's revision history): a list of {date, summary}.
    changelog = provenance.get("changelog")
    if changelog is not None:
        if not isinstance(changelog, list):
            issues.error(w, "changelog must be a list of {date, summary} entries")
        else:
            for i, entry in enumerate(changelog):
                if not isinstance(entry, dict):
                    issues.error(w, f"changelog[{i}] must be a mapping with date and summary")
                    continue
                if not _is_iso_date(entry.get("date")):
                    issues.error(w, f"changelog[{i}] date '{entry.get('date')}' is not ISO YYYY-MM-DD")
                if not (isinstance(entry.get("summary"), str) and entry["summary"].strip()):
                    issues.error(w, f"changelog[{i}] needs a non-empty summary")


def check_translation_math(work_dir: Path, issues: Issues) -> None:
    """Every translations/<lang>.tex must reproduce the original's math/markers verbatim (§4.2)."""
    original = work_dir / "original.tex"
    trans_dir = work_dir / "translations"
    if not original.exists() or not trans_dir.is_dir():
        return
    orig_text = original.read_text(encoding="utf-8")
    for tpath in sorted(trans_dir.glob("*.tex")):
        report = texcompare.preservation_report(orig_text, tpath.read_text(encoding="utf-8"))
        if not report["ok"]:
            issues.error(f"{work_dir.name}/translations/{tpath.name}",
                         "math/structure not preserved from original.tex:\n"
                         + texcompare.format_report(report))


NOTE_MARKER = re.compile(r"\[note (\d+)\]")
CITE_MARKER = re.compile(r"\[(\d+)\]")


def check_significance(work: dict, work_id: str, issues: Issues) -> None:
    """The editorial `significance` note and the two marker lists it addresses.

    The site renders the field as plain prose in which `[n]` addresses `significance_sources[n-1]`
    (a citation popover) and `[note n]` addresses `significance_notes[n-1]` (a labelled aside
    popover, for an excursus that would otherwise swamp the paragraph). A marker with nothing
    behind it renders as the literal `[3]` on the page and an entry nothing points at never renders
    at all — both are silent, so they are checked here rather than found by eye.
    """
    w = f"{work_id}/work.yaml"
    text = work.get("significance")
    if text is not None and not isinstance(text, str):
        issues.error(w, "significance must be a string")
        return

    def entries(field: str) -> list:
        value = work.get(field) or []
        if not isinstance(value, list):
            issues.error(w, f"{field} must be a list")
            return []
        return value

    sources = entries("significance_sources")
    notes = entries("significance_notes")

    for i, src in enumerate(sources):
        if not (isinstance(src, dict) and isinstance(src.get("citation"), str) and src["citation"].strip()):
            issues.error(w, f"significance_sources[{i}] needs a non-empty citation")
    for i, note in enumerate(notes):
        if not isinstance(note, dict):
            issues.error(w, f"significance_notes[{i}] must be a mapping with label and text")
            continue
        label = note.get("label")
        if not (isinstance(label, str) and label.strip()):
            issues.error(w, f"significance_notes[{i}] needs a non-empty label "
                            "(it is the visible text of the inline marker)")
        elif len(label) > 40:
            issues.warn(w, f"significance_notes[{i}] label is {len(label)} characters; it renders "
                           "as an inline chip inside the running prose — keep it short")
        if not (isinstance(note.get("text"), str) and note["text"].strip()):
            issues.error(w, f"significance_notes[{i}] needs a non-empty text")

    if (sources or notes) and not text:
        issues.error(w, "significance_sources/significance_notes with no significance to mark up")
    if not text:
        return

    used_notes = {int(n) for n in NOTE_MARKER.findall(text)}
    # Note markers are stripped first so the "1" inside "[note 1]" is not read as a citation.
    used_sources = {int(n) for n in CITE_MARKER.findall(NOTE_MARKER.sub("", text))}
    for kind, used, have in (("note", used_notes, notes), ("citation", used_sources, sources)):
        marker = f"[note {{n}}]" if kind == "note" else "[{n}]"
        field = "significance_notes" if kind == "note" else "significance_sources"
        for n in sorted(used):
            if not 1 <= n <= len(have):
                issues.error(w, f"significance {kind} marker {marker.format(n=n)} has no "
                                f"{field}[{n - 1}] (the marker would print as literal text)")
        for i in range(len(have)):
            if i + 1 not in used:
                issues.warn(w, f"{field}[{i}] is never referenced from the significance text "
                               f"(add a {marker.format(n=i + 1)} marker, or drop the entry)")

def check_house_style(work_dir: Path, work: dict, issues: Issues) -> None:
    """Mechanical presentation-layer house-style rules (corpus/HOUSESTYLE.md).

    Runs the stdlib-only linter over the transcription, every translation, the `significance`
    note in work.yaml and each of its `significance_notes` asides so a house-style regression (currently R2/R16 — an inline large operator must
    use `\\displaystyle`) cannot be merged. The `significance` field carries inline math that the
    site renders through KaTeX just like the `.tex` panels, so it needs the same gate. Judgement
    calls are never linted here; see houselint.py.
    """
    texs = []
    original = work_dir / "original.tex"
    if original.exists():
        texs.append(original)
    trans_dir = work_dir / "translations"
    if trans_dir.is_dir():
        texs.extend(sorted(trans_dir.glob("*.tex")))
    for tpath in texs:
        violations = houselint.lint(tpath.read_text(encoding="utf-8"))
        if violations:
            rel = tpath.relative_to(work_dir.parent).as_posix()
            issues.error(rel, "house-style violations (corpus/HOUSESTYLE.md):\n"
                         + houselint.format_violations(violations))

    significance = work.get("significance")
    if isinstance(significance, str):
        violations = houselint.lint(significance)
        if violations:
            issues.error(f"{work_dir.name}/work.yaml", "house-style violations in significance "
                         "(corpus/HOUSESTYLE.md):\n" + houselint.format_violations(violations))
    # Significance asides carry the same inline math, rendered by the same KaTeX pass.
    for i, note in enumerate(work.get("significance_notes") or []):
        text = note.get("text") if isinstance(note, dict) else None
        if not isinstance(text, str):
            continue
        violations = houselint.lint(text)
        if violations:
            issues.error(f"{work_dir.name}/work.yaml",
                         f"house-style violations in significance_notes[{i}] "
                         "(corpus/HOUSESTYLE.md):\n" + houselint.format_violations(violations))


def check_relations(works_by_id: dict[str, dict], vocab: dict, issues: Issues) -> None:
    """Validate the corpus-wide dependency graph declared in each work's `relations:` list.

    Edges are authored on the newer work pointing backward to an earlier one, so the whole thing
    must form a DAG. Runs at corpus level because dangling-target, chronology, and cycle checks all
    need every work's id and year. Per-work-local checks (kind vocab, one-recommended, self-loop)
    are folded in here too, keyed by "<id>/work.yaml" like the other messages.
    """
    kinds = vocab.get("relation_kinds") or {}
    years = {wid: (w.get("publication") or {}).get("year") for wid, w in works_by_id.items()}
    adjacency: dict[str, list[str]] = {}

    for wid, work in works_by_id.items():
        w = f"{wid}/work.yaml"
        rels = work.get("relations")
        adjacency[wid] = []
        if rels is None:
            continue
        if not isinstance(rels, list):
            issues.error(w, "relations must be a list of edges")
            continue
        recommended_count = 0
        for i, edge in enumerate(rels):
            if not isinstance(edge, dict):
                issues.error(w, f"relations[{i}] must be a mapping with at least 'to' and 'kind'")
                continue
            to = edge.get("to")
            kind = edge.get("kind")
            if not to:
                issues.error(w, f"relations[{i}] missing 'to'")
            elif to == wid:
                issues.error(w, f"relations[{i}] points to itself ('{to}')")
            elif to not in works_by_id:
                issues.error(w, f"relations[{i}] 'to: {to}' is not an existing corpus work")
            else:
                adjacency[wid].append(to)
                y_from, y_to = years.get(wid), years.get(to)
                if isinstance(y_from, int) and isinstance(y_to, int) and y_to > y_from:
                    issues.error(w, f"relations[{i}] 'to: {to}' ({y_to}) is newer than this work "
                                    f"({y_from}); edges must point backward in time")
            if kind not in kinds:
                issues.error(w, f"relations[{i}] kind '{kind}' not in vocab.relation_kinds")
            rec = edge.get("recommended")
            if rec not in (None, False, True, "primary"):
                issues.error(w, f"relations[{i}] recommended must be true or 'primary', got {rec!r}")
            if rec in (True, "primary"):
                recommended_count += 1
        if recommended_count > 1:
            issues.error(w, f"has {recommended_count} recommended relations; at most one is allowed")

    # Cycle detection over the (backward) edges — DFS colouring; report the first cycle found.
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {wid: WHITE for wid in adjacency}

    def visit(node: str, stack: list[str]) -> bool:
        colour[node] = GREY
        stack.append(node)
        for nxt in adjacency.get(node, []):
            if colour.get(nxt) == GREY:
                cyc = stack[stack.index(nxt):] + [nxt]
                issues.error("corpus", "relations form a cycle: " + " -> ".join(cyc))
                return True
            if colour.get(nxt) == WHITE and visit(nxt, stack):
                return True
        stack.pop()
        colour[node] = BLACK
        return False

    for wid in adjacency:
        if colour[wid] == WHITE and visit(wid, []):
            break


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
    check_translation_math(work_dir, issues)
    check_significance(work, work_id, issues)
    check_house_style(work_dir, work, issues)

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
    check_venue_vocab(vocab, issues)

    work_dirs = sorted(
        d for d in corpus_dir.iterdir()
        if d.is_dir() and (d / "work.yaml").exists()
    )

    seen_ids: dict[str, str] = {}
    # Cross-work author consistency: one wikidata_id must carry the same birth/death years
    # everywhere it appears, or the aggregated author page would show conflicting dates.
    author_dates: dict[str, tuple[str, dict]] = {}
    # Keyed by directory name — the dependency graph is validated across the whole corpus below.
    works_by_id: dict[str, dict] = {}
    for wd in work_dirs:
        validate_work(wd, vocab, now_year, strict_pma_100, issues, write=write)
        # Cross-work: unique ids.
        if (wd / "work.yaml").exists():
            work = load_yaml(wd / "work.yaml") or {}
            works_by_id[wd.name] = work
            wid = work.get("id")
            if wid in seen_ids:
                issues.error(wd.name, f"duplicate id '{wid}' (also in {seen_ids[wid]})")
            elif wid:
                seen_ids[wid] = wd.name

            for a in work.get("authors") or []:
                qid = a.get("wikidata_id")
                if not qid:
                    continue
                dates = {"birth_year": a.get("birth_year"), "death_year": a.get("death_year")}
                if qid in author_dates:
                    first_dir, first_dates = author_dates[qid]
                    if first_dates != dates:
                        issues.warn(wd.name, f"author {qid} has {dates} but {first_dates} in "
                                             f"{first_dir}; birth/death years should agree")
                else:
                    author_dates[qid] = (wd.name, dates)

    check_relations(works_by_id, vocab, issues)
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
