"""Tests for candidate database."""

from ballotguide.guide.candidates import CandidateDatabase
from ballotguide.models import Candidate, PolicyArea, PolicyPosition, Stance


def test_default_database_has_candidates():
    db = CandidateDatabase()
    assert len(db.all_candidates) >= 4


def test_get_candidate_by_name():
    db = CandidateDatabase()
    c = db.get_candidate("Maria Santos")
    assert c is not None
    assert c.name == "Maria Santos"


def test_get_candidate_not_found():
    db = CandidateDatabase()
    assert db.get_candidate("Nonexistent Person") is None


def test_search_case_insensitive():
    db = CandidateDatabase()
    results = db.search("santos")
    assert len(results) == 1
    assert results[0].name == "Maria Santos"


def test_by_office():
    db = CandidateDatabase()
    results = db.by_office("senate")
    assert len(results) == 2


def test_get_positions():
    db = CandidateDatabase()
    positions = db.get_positions("Maria Santos")
    assert len(positions) >= 5


def test_get_positions_filtered_by_area():
    db = CandidateDatabase()
    positions = db.get_positions("Maria Santos", PolicyArea.EDUCATION)
    assert len(positions) == 1
    assert positions[0].area == PolicyArea.EDUCATION


def test_get_voting_record():
    db = CandidateDatabase()
    record = db.get_voting_record("Maria Santos")
    assert len(record) >= 2


def test_get_endorsements():
    db = CandidateDatabase()
    endorsements = db.get_endorsements("James Thornton")
    assert len(endorsements) >= 1


def test_add_candidate():
    db = CandidateDatabase()
    new = Candidate(name="New Candidate", office="School Board")
    db.add_candidate(new)
    assert db.get_candidate("New Candidate") is not None


def test_list_offices():
    db = CandidateDatabase()
    offices = db.list_offices()
    assert len(offices) >= 2


def test_sample_candidates_are_non_partisan():
    """Verify sample candidates do not have party affiliations set."""
    db = CandidateDatabase()
    for c in db.all_candidates:
        assert c.party == "", f"Candidate {c.name} has party '{c.party}' set"
