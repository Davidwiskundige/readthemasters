"""Tests for the provenance changelog: revision history (PLAN.md §9 backlog #4)."""
import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_site_data as bsd  # noqa: E402
import validate  # noqa: E402


# --- build_site_data.changelog_entries -------------------------------------------------------- #

def test_changelog_entries_sorted_newest_first_and_normalized():
    prov = {"changelog": [
        {"date": "2026-07-19", "summary": "Transcription added."},
        {"date": "2026-07-21", "summary": "Translation added."},
        {"date": "2026-07-20", "summary": "Spot-checked."},
    ]}
    got = bsd.changelog_entries(prov)
    assert [e["date"] for e in got] == ["2026-07-21", "2026-07-20", "2026-07-19"]
    assert got[0] == {"date": "2026-07-21", "summary": "Translation added."}


def test_changelog_entries_absent_or_empty():
    assert bsd.changelog_entries({}) == []
    assert bsd.changelog_entries({"changelog": None}) == []
    assert bsd.changelog_entries(None) == []


def test_changelog_entries_coerces_yaml_date_object():
    # An unquoted YAML date parses to datetime.date; it must serialize to an ISO string.
    prov = {"changelog": [{"date": datetime.date(2026, 7, 20), "summary": "x"}]}
    assert bsd.changelog_entries(prov)[0]["date"] == "2026-07-20"


# --- validate.check_provenance changelog rules ------------------------------------------------ #

def _base_prov(changelog):
    return {
        "transcription": {"status": "ai-draft", "model": "m", "prompt_version": "v"},
        "changelog": changelog,
    }


def test_validate_accepts_a_good_changelog():
    issues = validate.Issues()
    validate.check_provenance(_base_prov([{"date": "2026-07-20", "summary": "ok"}]), "w", issues)
    assert issues.ok, issues.errors


def test_validate_rejects_bad_date_and_empty_summary():
    issues = validate.Issues()
    validate.check_provenance(
        _base_prov([{"date": "20 July 2026", "summary": "bad date"},
                    {"date": "2026-07-20", "summary": "  "}]), "w", issues)
    assert len(issues.errors) == 2
    assert any("not ISO" in e for e in issues.errors)
    assert any("non-empty summary" in e for e in issues.errors)


def test_validate_rejects_non_list_changelog():
    issues = validate.Issues()
    validate.check_provenance(_base_prov("nope"), "w", issues)
    assert any("must be a list" in e for e in issues.errors)


def test_validate_allows_absent_changelog():
    issues = validate.Issues()
    prov = {"transcription": {"status": "ai-draft", "model": "m", "prompt_version": "v"}}
    validate.check_provenance(prov, "w", issues)
    assert issues.ok, issues.errors
