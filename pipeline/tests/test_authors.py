"""Tests for author aggregation in build_site_data.py (PLAN.md §9 backlog #4)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_site_data as bsd  # noqa: E402


def works_fixture():
    """Two Fagnano works (same QID) + one Leibniz work, in the shape build() emits."""
    return [
        {"id": "fag-1", "title": "Schediasma I", "year": 1718, "url": "/works/fag-1/",
         "status": "ai-draft", "venue_full": "Giornale, vol. 29",
         "authors": [{"name": "Giulio Carlo de' Toschi di Fagnano",
                      "wikidata_id": "Q1528006", "birth_year": 1682, "death_year": 1766}]},
        {"id": "fag-2", "title": "Schediasma II", "year": 1718, "url": "/works/fag-2/",
         "status": "skimmed", "venue_full": "Giornale, vol. 30",
         "authors": [{"name": "Giulio Carlo de' Toschi di Fagnano",
                      "wikidata_id": "Q1528006", "birth_year": 1682, "death_year": 1766}]},
        {"id": "leib-1", "title": "De linea isochrona", "year": 1689, "url": "/works/leib-1/",
         "status": "ai-draft", "venue_full": "Acta Eruditorum, April",
         "authors": [{"name": "Gottfried Wilhelm Leibniz",
                      "wikidata_id": "Q9047", "birth_year": 1646, "death_year": 1716}]},
    ]


def test_slugify_folds_diacritics_and_punctuation():
    assert bsd.slugify("Giulio Carlo de' Toschi di Fagnano") == "giulio-carlo-de-toschi-di-fagnano"
    assert bsd.slugify("Émile Léonard Mathieu") == "emile-leonard-mathieu"
    assert bsd.slugify("") == "author"


def test_same_qid_merges_across_works():
    authors = bsd.build_authors(works_fixture())
    assert len(authors) == 2
    fagnano = next(a for a in authors if a["wikidata_id"] == "Q1528006")
    assert [w["id"] for w in fagnano["works"]] == ["fag-1", "fag-2"]
    assert fagnano["work_count"] == 2


def test_authors_sorted_by_name():
    authors = bsd.build_authors(works_fixture())
    assert [a["slug"] for a in authors] == [
        "giulio-carlo-de-toschi-di-fagnano", "gottfried-wilhelm-leibniz"]


def test_slug_attached_to_each_work_author():
    works = works_fixture()
    bsd.build_authors(works)
    assert works[0]["authors"][0]["slug"] == "giulio-carlo-de-toschi-di-fagnano"
    assert works[2]["authors"][0]["slug"] == "gottfried-wilhelm-leibniz"


def test_namesakes_with_distinct_qids_get_distinct_slugs():
    # Two different people who happen to share a name are kept apart by their QIDs (PLAN §9a);
    # the second gets a "-2" suffix so the URLs stay unique.
    works = [
        {"id": "w1", "title": "A", "year": 1900, "url": "/works/w1/", "status": "ai-draft",
         "authors": [{"name": "John Smith", "wikidata_id": "Q1", "death_year": 1850}]},
        {"id": "w2", "title": "B", "year": 1901, "url": "/works/w2/", "status": "ai-draft",
         "authors": [{"name": "John Smith", "wikidata_id": "Q2", "death_year": 1860}]},
    ]
    authors = bsd.build_authors(works)
    assert len(authors) == 2
    assert sorted(a["slug"] for a in authors) == ["john-smith", "john-smith-2"]


def test_namesakes_without_qid_merge():
    # No id to disambiguate => the honest fallback is one page (they cannot be told apart).
    works = [
        {"id": "w1", "title": "A", "year": 1900, "url": "/works/w1/", "status": "ai-draft",
         "authors": [{"name": "John Smith", "death_year": 1850}]},
        {"id": "w2", "title": "B", "year": 1901, "url": "/works/w2/", "status": "ai-draft",
         "authors": [{"name": "John Smith", "death_year": 1850}]},
    ]
    authors = bsd.build_authors(works)
    assert len(authors) == 1
    assert authors[0]["work_count"] == 2


def test_resolve_portrait_copies_and_returns_url(tmp_path):
    # Source image committed under corpus/authors/<slug>/; build copies it into the site.
    corpus = tmp_path / "corpus"
    (corpus / "authors" / "leibniz").mkdir(parents=True)
    (corpus / "authors" / "leibniz" / "portrait.jpg").write_bytes(b"\xff\xd8\xff\xe0JPEG")
    public_authors = tmp_path / "site" / "public" / "authors"

    p = bsd.resolve_portrait(corpus, public_authors, "leibniz",
                             {"file": "portrait.jpg", "credit": "Portrait by B. C. Francke",
                              "alt": "Portrait of Leibniz",
                              "source": "https://commons.wikimedia.org/wiki/File:X.jpg"})
    assert p["url"] == "/authors/leibniz/portrait.jpg"
    assert p["credit"] == "Portrait by B. C. Francke"
    assert p["source"] == "https://commons.wikimedia.org/wiki/File:X.jpg"  # passthrough
    assert (public_authors / "leibniz" / "portrait.jpg").read_bytes() == b"\xff\xd8\xff\xe0JPEG"


def test_resolve_portrait_missing_file_yields_no_url(tmp_path):
    p = bsd.resolve_portrait(tmp_path, None, "nobody", {"file": "ghost.jpg"})
    assert p["url"] is None


def test_resolve_portrait_none_when_absent():
    assert bsd.resolve_portrait(Path("."), None, "x", None) is None
    assert bsd.resolve_portrait(Path("."), None, "x", {"credit": "no file key"}) is None


def test_mactutor_url_from_id_and_full_url():
    assert bsd.mactutor_url("Leibniz") == \
        "https://mathshistory.st-andrews.ac.uk/Biographies/Leibniz/"
    assert bsd.mactutor_url("/Fagnano_Giulio/") == \
        "https://mathshistory.st-andrews.ac.uk/Biographies/Fagnano_Giulio/"
    assert bsd.mactutor_url("https://example.org/bio") == "https://example.org/bio"
    assert bsd.mactutor_url(None) is None


def test_mactutor_url_flows_into_author_record():
    works = works_fixture()
    works[2]["authors"][0]["mactutor"] = "Leibniz"
    authors = bsd.build_authors(works)
    leib = next(a for a in authors if a["wikidata_id"] == "Q9047")
    assert leib["mactutor_url"] == "https://mathshistory.st-andrews.ac.uk/Biographies/Leibniz/"
    fagnano = next(a for a in authors if a["wikidata_id"] == "Q1528006")
    assert fagnano["mactutor_url"] is None


def test_anonymous_author_flag_preserved():
    works = [
        {"id": "w1", "title": "A", "year": 1700, "url": "/works/w1/", "status": "ai-draft",
         "authors": [{"name": "Anonymous", "anonymous": True}]},
    ]
    authors = bsd.build_authors(works)
    assert authors[0]["anonymous"] is True
