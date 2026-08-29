"""Tests for the copyright gate and corpus validator."""
import copy
import sys
from pathlib import Path

# Make pipeline/validate.py importable regardless of pytest's rootdir.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import validate  # noqa: E402

REPO = Path(__file__).resolve().parents[2]
NOW = 2026


# --- A minimal public-domain work + provenance, mutated per test ------------- #
def pd_work():
    return {
        "id": "test-work",
        "title": "Test",
        "authors": [{"name": "A. Author", "death_year": 1900}],
        "publication": {"year": 1905, "venue": "crelle"},
        "edition": {"year": 1905, "is_transcribed_edition": True,
                    "rights_cleared": True, "rights_note": "original edition"},
        "discipline": "mathematics",
        "tags": ["analysis"],
        "language": "de",
        "type": "paper",
        "source": {"scan_url": "http://x", "scan_id": "x:1"},
        "sources": {"death_date": "wikidata:Q1",
                    "publication_date": "catalog:1", "edition": "catalog:1"},
    }


def pd_prov():
    return {"transcription": {"status": "ai-draft", "model": "claude-opus-4-8",
                              "prompt_version": "transcribe-v1"}}


def verdict(work, prov=None, now=NOW, strict=False):
    a = validate.evaluate_copyright(work, prov or pd_prov(), now, strict)
    return a["public_domain"], {k: v["verdict"] for k, v in a["evaluated"].items()}


# --- Copyright rule tests ---------------------------------------------------- #
def test_public_domain_work_passes():
    pd, rules = verdict(pd_work())
    assert pd is True
    assert all(v == "pass" for v in rules.values())


def test_recent_death_fails_pma70():
    w = pd_work()
    w["authors"][0]["death_year"] = 1990  # 1990 + 71 = 2061 > 2026
    pd, rules = verdict(w)
    assert pd is False
    assert rules["pma_70"] == "fail"


def test_pma70_boundary():
    w = pd_work()
    w["authors"][0]["death_year"] = 1955           # +71 = 2026 -> PD exactly now
    assert verdict(w)[1]["pma_70"] == "pass"
    w["authors"][0]["death_year"] = 1956           # +71 = 2027 -> not yet
    assert verdict(w)[1]["pma_70"] == "fail"


def test_recent_publication_fails_us_rule():
    # Author long dead, but published recently -> US rule blocks (the Einstein trap).
    w = pd_work()
    w["authors"][0]["death_year"] = 1850
    w["publication"]["year"] = 1980  # 1980 + 96 = 2076 > 2026
    pd, rules = verdict(w)
    assert pd is False
    assert rules["us_publication"] == "fail"
    assert rules["pma_70"] == "pass"


def test_us_publication_boundary():
    w = pd_work()
    w["authors"][0]["death_year"] = 1850
    w["publication"]["year"] = 1930  # +96 = 2026 -> PD now
    assert verdict(w)[1]["us_publication"] == "pass"
    w["publication"]["year"] = 1931  # +96 = 2027 -> not yet (published >= 1931)
    assert verdict(w)[1]["us_publication"] == "fail"


def test_edition_rights_must_be_cleared():
    w = pd_work()
    w["edition"]["rights_cleared"] = False
    pd, rules = verdict(w)
    assert pd is False
    assert rules["edition_rights"] == "fail"


def test_edition_rights_needs_note():
    w = pd_work()
    w["edition"]["rights_note"] = ""
    assert verdict(w)[1]["edition_rights"] == "fail"


def test_external_translation_fails():
    prov = pd_prov()
    prov["translations"] = {"en": {"status": "ai-draft", "model": "m",
                                   "prompt_version": "v", "source": "external"}}
    pd, rules = verdict(pd_work(), prov)
    assert pd is False
    assert rules["translation_source"] == "fail"


def test_external_open_translation_with_license_passes():
    prov = pd_prov()
    prov["translations"] = {"en": {"status": "ai-draft", "model": "m", "prompt_version": "v",
                                   "source": "external-open", "license": "public-domain"}}
    assert verdict(pd_work(), prov)[1]["translation_source"] == "pass"


def test_external_open_translation_without_license_fails():
    prov = pd_prov()
    prov["translations"] = {"en": {"status": "ai-draft", "model": "m", "prompt_version": "v",
                                   "source": "external-open"}}  # no license named
    assert verdict(pd_work(), prov)[1]["translation_source"] == "fail"


def test_unknown_death_recent_publication_blocks():
    w = pd_work()
    w["authors"][0].pop("death_year")
    w["authors"][0]["death_year"] = None
    w["publication"]["year"] = 1950  # 1950 + 170 = 2120 > 2026
    assert verdict(w)[1]["pma_70"] == "fail"


def test_unknown_death_very_old_publication_passes():
    w = pd_work()
    w["authors"][0]["death_year"] = None
    w["publication"]["year"] = 1800  # 1800 + 170 = 1970 <= 2026
    assert verdict(w)[1]["pma_70"] == "pass"


def test_anonymous_uses_publication_plus_70():
    w = pd_work()
    w["authors"] = [{"name": "Anonymous", "anonymous": True}]
    w["publication"]["year"] = 1900  # +71 = 1971 <= 2026
    assert verdict(w)[1]["pma_70"] == "pass"


def test_multiple_authors_all_must_clear():
    w = pd_work()
    w["authors"] = [{"name": "Old", "death_year": 1900},
                    {"name": "Recent", "death_year": 1990}]
    assert verdict(w)[1]["pma_70"] == "fail"


def test_strict_pma_100():
    w = pd_work()
    w["authors"][0]["death_year"] = 1940  # +71 = 2011 (pma70 pass) but +101 = 2041 (pma100 fail)
    assert verdict(w, strict=False)[0] is True
    pd, rules = verdict(w, strict=True)
    assert pd is False
    assert rules["pma_100"] == "fail"


# --- Schema / vocab / provenance tests --------------------------------------- #
def test_bad_vocab_value_errors():
    w = pd_work()
    w["discipline"] = "chemistry"  # not in vocab
    iss = validate.Issues()
    vocab = validate.load_yaml(REPO / "corpus" / "vocab.yaml")
    validate.check_schema_and_vocab(w, vocab, "test-work", iss)
    assert any("discipline" in e for e in iss.errors)


def test_unsourced_publication_date_errors():
    w = pd_work()
    w["sources"]["publication_date"] = ""
    iss = validate.Issues()
    vocab = validate.load_yaml(REPO / "corpus" / "vocab.yaml")
    validate.check_schema_and_vocab(w, vocab, "test-work", iss)
    assert any("publication_date" in e for e in iss.errors)


def test_bad_effort_value_errors():
    prov = {"transcription": {"status": "ai-draft", "model": "m",
                              "prompt_version": "v", "effort": "turbo"}}
    iss = validate.Issues()
    validate.check_provenance(prov, "test-work", iss)
    assert any("effort" in e for e in iss.errors)


# --- Significance note / marker tests ---------------------------------------- #
def sig_issues(**fields):
    """Run check_significance over a work carrying only the significance fields under test."""
    iss = validate.Issues()
    validate.check_significance(fields, "test-work", iss)
    return iss


def test_significance_markers_resolve():
    iss = sig_issues(
        significance="Roch fixed the excess.[1] [note 1]",
        significance_sources=[{"citation": "MacTutor, Gustav Roch", "url": "https://x"}],
        significance_notes=[{"label": "In modern notation", "text": "The Riemann-Roch formula."}])
    assert iss.errors == [] and iss.warnings == []


def test_unresolved_note_marker_errors():
    iss = sig_issues(significance="An aside. [note 2]",
                     significance_notes=[{"label": "L", "text": "T"}])
    assert any("[note 2]" in e for e in iss.errors)


def test_unresolved_citation_marker_errors():
    iss = sig_issues(significance="A claim.[3]",
                     significance_sources=[{"citation": "One source"}])
    assert any("[3]" in e for e in iss.errors)


def test_note_marker_is_not_read_as_a_citation_marker():
    # "[note 1]" contains "1"; only the note list must be consulted for it.
    iss = sig_issues(significance="An aside. [note 1]",
                     significance_notes=[{"label": "L", "text": "T"}])
    assert iss.errors == []


def test_unreferenced_note_warns():
    iss = sig_issues(significance="No markers here.",
                     significance_notes=[{"label": "L", "text": "T"}])
    assert iss.errors == []
    assert any("never referenced" in x for x in iss.warnings)


def test_note_without_label_or_text_errors():
    iss = sig_issues(significance="An aside. [note 1] Another. [note 2]",
                     significance_notes=[{"text": "no label"}, {"label": "no text"}])
    assert any("label" in e for e in iss.errors)
    assert any("text" in e for e in iss.errors)


def test_long_note_label_warns():
    iss = sig_issues(significance="An aside. [note 1]",
                     significance_notes=[{"label": "x" * 41, "text": "T"}])
    assert iss.errors == []
    assert any("keep it short" in x for x in iss.warnings)


def test_notes_without_significance_error():
    iss = sig_issues(significance_notes=[{"label": "L", "text": "T"}])
    assert any("no significance" in e for e in iss.errors)


def test_work_without_significance_is_fine():
    iss = sig_issues()
    assert iss.errors == [] and iss.warnings == []


# --- Relations / dependency graph tests -------------------------------------- #
VOCAB = {"relation_kinds": {"cites": "Cites", "builds-on": "Builds on"}}


def rel_work(wid, year, relations=None):
    w = {"id": wid, "publication": {"year": year}}
    if relations is not None:
        w["relations"] = relations
    return w


def rel_errors(works, vocab=VOCAB):
    iss = validate.Issues()
    validate.check_relations({w["id"]: w for w in works}, vocab, iss)
    return iss.errors


def test_valid_backward_graph_passes():
    works = [
        rel_work("a", 1689),
        rel_work("b", 1694, [{"to": "a", "kind": "builds-on", "recommended": True}]),
        rel_work("c", 1718, [{"to": "b", "kind": "builds-on", "recommended": "primary"},
                             {"to": "a", "kind": "cites"}]),
    ]
    assert rel_errors(works) == []


def test_dangling_target_errors():
    works = [rel_work("b", 1694, [{"to": "nope", "kind": "cites"}])]
    assert any("not an existing corpus work" in e for e in rel_errors(works))


def test_self_edge_errors():
    works = [rel_work("b", 1694, [{"to": "b", "kind": "cites"}])]
    assert any("points to itself" in e for e in rel_errors(works))


def test_forward_in_time_edge_errors():
    works = [rel_work("a", 1689, [{"to": "b", "kind": "builds-on"}]), rel_work("b", 1694)]
    assert any("newer than this work" in e for e in rel_errors(works))


def test_same_year_edge_allowed():
    works = [rel_work("a", 1718), rel_work("b", 1718, [{"to": "a", "kind": "builds-on"}])]
    assert rel_errors(works) == []


def test_bad_kind_errors():
    works = [rel_work("a", 1689), rel_work("b", 1694, [{"to": "a", "kind": "inspired-by"}])]
    assert any("relation_kinds" in e for e in rel_errors(works))


def test_two_recommended_errors():
    works = [rel_work("a", 1689), rel_work("b", 1690),
             rel_work("c", 1694, [{"to": "a", "kind": "builds-on", "recommended": True},
                                  {"to": "b", "kind": "builds-on", "recommended": "primary"}])]
    assert any("at most one" in e for e in rel_errors(works))


def test_bad_recommended_value_errors():
    works = [rel_work("a", 1689),
             rel_work("b", 1694, [{"to": "a", "kind": "builds-on", "recommended": "yes"}])]
    assert any("recommended must be" in e for e in rel_errors(works))


def test_cycle_detected():
    # Same-year 2-cycle: a->b and b->a both satisfy year(to) <= year(self) but form a cycle.
    works = [rel_work("a", 1700, [{"to": "b", "kind": "cites"}]),
             rel_work("b", 1700, [{"to": "a", "kind": "cites"}])]
    assert any("cycle" in e for e in rel_errors(works))


# --- Integration: the real corpus passes ------------------------------------- #
def test_real_corpus_passes_gate():
    issues = validate.validate_corpus(REPO / "corpus", now_year=NOW)
    assert issues.ok, "corpus should pass:\n" + "\n".join(issues.errors)


def test_stale_assessment_detected(tmp_path):
    # Copy a corpus work, corrupt its stored assessment, expect an error.
    import shutil
    src = REPO / "corpus"
    dst = tmp_path / "corpus"
    shutil.copytree(src, dst)
    wp = dst / "leibniz-1689-isochrona" / "work.yaml"
    work = validate.load_yaml(wp)
    work["copyright_assessment"]["public_domain"] = False
    work["copyright_assessment"]["evaluated"]["pma_70"]["verdict"] = "fail"
    import yaml
    wp.write_text(yaml.safe_dump(work, allow_unicode=True, sort_keys=False), encoding="utf-8")
    issues = validate.validate_corpus(dst, now_year=NOW)
    assert not issues.ok
    assert any("stale" in e or "incorrect" in e for e in issues.errors)
