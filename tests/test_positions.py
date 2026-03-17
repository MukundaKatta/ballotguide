"""Tests for position tracker."""

from ballotguide.analyzer.positions import PositionTracker
from ballotguide.guide.candidates import CandidateDatabase
from ballotguide.models import PolicyArea


def test_coverage_report():
    db = CandidateDatabase()
    tracker = PositionTracker(db.all_candidates)
    report = tracker.coverage_report("Maria Santos")
    assert isinstance(report, dict)
    assert PolicyArea.EDUCATION in report
    assert report[PolicyArea.EDUCATION] is True


def test_coverage_gaps():
    db = CandidateDatabase()
    tracker = PositionTracker(db.all_candidates)
    gaps = tracker.coverage_gaps("Maria Santos")
    # Santos has 8 positions, so at least 8 gaps out of 16
    assert len(gaps) >= 8


def test_positions_by_area():
    db = CandidateDatabase()
    tracker = PositionTracker(db.all_candidates)
    positions = tracker.positions_by_area(PolicyArea.ECONOMY)
    assert "Maria Santos" in positions
    assert positions["Maria Santos"] is not None


def test_stance_summary():
    db = CandidateDatabase()
    tracker = PositionTracker(db.all_candidates)
    summary = tracker.stance_summary()
    assert "Maria Santos" in summary
    assert PolicyArea.EDUCATION in summary["Maria Santos"]


def test_find_agreement():
    db = CandidateDatabase()
    tracker = PositionTracker(db.all_candidates)
    agreement = tracker.find_agreement("Maria Santos", "James Thornton")
    # Both support education (though different approaches) - stance is SUPPORTS
    assert PolicyArea.EDUCATION in agreement


def test_find_disagreement():
    db = CandidateDatabase()
    tracker = PositionTracker(db.all_candidates)
    disagreement = tracker.find_disagreement("Maria Santos", "James Thornton")
    # They disagree on taxation stance
    assert PolicyArea.TAXATION in disagreement


def test_all_policy_areas():
    assert len(PositionTracker.ALL_POLICY_AREAS) >= 16


def test_get_position():
    db = CandidateDatabase()
    tracker = PositionTracker(db.all_candidates)
    pos = tracker.get_position("Maria Santos", PolicyArea.CLIMATE)
    assert pos is not None
    assert pos.area == PolicyArea.CLIMATE
