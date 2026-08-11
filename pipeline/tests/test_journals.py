"""Tests for venue metadata + journal aggregation (journal-pages change).

Covers the object-or-string venue vocabulary (validate.venue_label / check_venue_vocab) and the
per-journal aggregation for /journals/ (build_site_data.build_journals / venue_meta).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_site_data as bsd  # noqa: E402
import validate  # noqa: E402


# --------------------------------------------------------------------------- #
# venue_label: object -> name, bare string -> itself
# --------------------------------------------------------------------------- #
def test_venue_label_resolves_object_and_string():
    vocab = {"venues": {
        "obj": {"name": "The Full Name", "aka": "Short"},
        "bare": "A Bare Title",
    }}
    assert validate.venue_label(vocab, "obj") == "The Full Name"
    assert validate.venue_label(vocab, "bare") == "A Bare Title"
    assert validate.venue_label(vocab, "missing") is None


# --------------------------------------------------------------------------- #
# check_venue_vocab: structural validation of object-form entries
# --------------------------------------------------------------------------- #
def _errors(vocab):
    issues = validate.Issues()
    validate.check_venue_vocab(vocab, issues)
    return issues.errors


def test_bare_string_venue_is_always_valid():
    assert _errors({"venues": {"x": "A Journal"}}) == []


def test_object_venue_requires_name():
    errs = _errors({"venues": {"x": {"aka": "no name"}}})
    assert any("must have a 'name'" in e for e in errs)


def test_object_venue_kind_must_be_known():
    errs = _errors({"venues": {"x": {"name": "N", "kind": "periodicalish"}}})
    assert any("kind" in e for e in errs)
    # A valid kind passes.
    assert _errors({"venues": {"x": {"name": "N", "kind": "book"}}}) == []


def test_archive_urls_must_be_absolute_http():
    errs = _errors({"venues": {"x": {"name": "N", "archives": [{"label": "L", "url": "/relative"}]}}})
    assert any("archives[0].url" in e for e in errs)
    ok = _errors({"venues": {"x": {"name": "N",
                                   "archives": [{"label": "L", "url": "https://example.org/run"}]}}})
    assert ok == []


# --------------------------------------------------------------------------- #
# venue_meta: normalize an entry (object or bare string) to a metadata dict
# --------------------------------------------------------------------------- #
def test_venue_meta_defaults_for_bare_string():
    m = bsd.venue_meta("A Journal")
    assert m["name"] == "A Journal"
    assert m["kind"] == "periodical"   # bare strings are periodicals by default
    assert m["archives"] == []


def test_venue_meta_passes_object_fields():
    m = bsd.venue_meta({"name": "N", "aka": "K", "kind": "book", "founded": 1826,
                        "archives": [{"label": "L", "url": "https://x"}]})
    assert (m["name"], m["aka"], m["kind"], m["founded"]) == ("N", "K", "book", 1826)
    assert m["archives"] == [{"label": "L", "url": "https://x"}]


# --------------------------------------------------------------------------- #
# build_journals: aggregate the venue vocab into per-journal records
# --------------------------------------------------------------------------- #
def vocab_fixture():
    return {"venues": {
        "acta": {"name": "Acta Eruditorum", "kind": "periodical", "founded": 1682},
        "giornale": {"name": "Giornale de' letterati d'Italia", "founded": 1710},
        "empty-journal": {"name": "Zeitschrift ohne Werke", "kind": "periodical"},
        "book": {"name": "(book)", "kind": "book"},
        "manuscript": {"name": "(manuscript)", "kind": "manuscript"},
    }}


def works_fixture():
    return [
        {"id": "b1", "title": "Solutio", "year": 1690, "url": "/works/b1/", "status": "ai-draft",
         "venue": "acta", "venue_full": "Acta Eruditorum, June", "authors": [{"name": "Jacob Bernoulli"}],
         "source": {"scan_url": "https://archive.org/details/x#p1"}},
        {"id": "b2", "title": "Curvatura", "year": 1694, "url": "/works/b2/", "status": "skimmed",
         "venue": "acta", "venue_full": "Acta Eruditorum, September", "authors": [{"name": "Jacob Bernoulli"}],
         "source": {}},
        {"id": "f1", "title": "Schediasma", "year": 1718, "url": "/works/f1/", "status": "ai-draft",
         "venue": "giornale", "venue_full": "Giornale, vol. 29", "authors": [{"name": "Giulio Fagnano"}],
         "source": {"scan_url": "https://archive.org/details/g#p1"}},
    ]


def test_sentinels_excluded_and_empty_periodical_kept():
    journals = bsd.build_journals(works_fixture(), vocab_fixture())
    slugs = {j["slug"] for j in journals}
    assert "book" not in slugs and "manuscript" not in slugs
    assert "empty-journal" in slugs  # curated periodical with no works still appears
    assert next(j for j in journals if j["slug"] == "empty-journal")["work_count"] == 0


def test_works_aggregated_by_venue_and_ordered_by_year():
    journals = bsd.build_journals(works_fixture(), vocab_fixture())
    acta = next(j for j in journals if j["slug"] == "acta")
    assert acta["work_count"] == 2
    assert [w["id"] for w in acta["works"]] == ["b1", "b2"]  # 1690 before 1694
    assert acta["works"][0]["scan_url"] == "https://archive.org/details/x#p1"
    assert acta["works"][0]["by"] == "Bernoulli"  # surname only
    assert acta["works"][1]["scan_url"] is None    # missing scan_url passes through as None


def test_journals_sorted_by_name():
    journals = bsd.build_journals(works_fixture(), vocab_fixture())
    names = [j["name"] for j in journals]
    assert names == sorted(names, key=str.lower)


def test_journal_url_and_slug_from_venue_key():
    journals = bsd.build_journals(works_fixture(), vocab_fixture())
    giornale = next(j for j in journals if j["slug"] == "giornale")
    assert giornale["url"] == "/journals/giornale/"
