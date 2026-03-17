"""Tests for candidate comparator."""

from ballotguide.guide.candidates import CandidateDatabase
from ballotguide.guide.comparator import CandidateComparator
from ballotguide.models import PolicyArea


def test_compare_by_office():
    db = CandidateDatabase()
    comp = CandidateComparator(db)
    result = comp.compare_by_office("senate")
    assert result is not None
    assert len(result.candidates) == 2
    assert len(result.comparison_rows) >= 1


def test_compare_by_office_not_found():
    db = CandidateDatabase()
    comp = CandidateComparator(db)
    assert comp.compare_by_office("president") is None


def test_compare_specific_issues():
    db = CandidateDatabase()
    comp = CandidateComparator(db)
    result = comp.compare_by_office("senate", issues=[PolicyArea.ECONOMY, PolicyArea.EDUCATION])
    assert result is not None
    assert len(result.issues) == 2
    assert len(result.comparison_rows) == 2


def test_compare_candidates_by_name():
    db = CandidateDatabase()
    comp = CandidateComparator(db)
    result = comp.compare_candidates(["Maria Santos", "James Thornton"])
    assert result is not None
    assert len(result.candidates) == 2


def test_compare_candidates_insufficient():
    db = CandidateDatabase()
    comp = CandidateComparator(db)
    result = comp.compare_candidates(["Maria Santos"])
    assert result is None


def test_comparison_rows_contain_all_candidates():
    db = CandidateDatabase()
    comp = CandidateComparator(db)
    result = comp.compare_by_office("senate")
    assert result is not None
    for row in result.comparison_rows:
        for name in result.candidates:
            assert name in row, f"Candidate {name} missing from comparison row"
