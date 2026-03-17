"""Tests for report generation."""

from io import StringIO

from rich.console import Console

from ballotguide.guide.candidates import CandidateDatabase
from ballotguide.guide.comparator import CandidateComparator
from ballotguide.guide.measures import BallotMeasureAnalyzer
from ballotguide.models import VoterGuide
from ballotguide.report import ReportGenerator


def _make_report() -> tuple[ReportGenerator, StringIO]:
    buf = StringIO()
    console = Console(file=buf, force_terminal=False, width=120)
    return ReportGenerator(console), buf


def test_print_disclaimer():
    report, buf = _make_report()
    report.print_disclaimer()
    output = buf.getvalue()
    assert "non-partisan" in output.lower()


def test_print_candidate():
    report, buf = _make_report()
    db = CandidateDatabase()
    candidate = db.get_candidate("Maria Santos")
    report.print_candidate(candidate)
    output = buf.getvalue()
    assert "Maria Santos" in output
    assert "Education" in output


def test_print_measure():
    report, buf = _make_report()
    analyzer = BallotMeasureAnalyzer()
    measure = analyzer.get_measure("Proposition 1")
    report.print_measure(measure)
    output = buf.getvalue()
    assert "Proposition 1" in output
    assert "Fiscal Impact" in output


def test_print_comparison():
    report, buf = _make_report()
    db = CandidateDatabase()
    comparator = CandidateComparator(db)
    comparison = comparator.compare_by_office("senate")
    report.print_comparison(comparison)
    output = buf.getvalue()
    assert "Maria Santos" in output
    assert "James Thornton" in output


def test_print_full_guide():
    report, buf = _make_report()
    db = CandidateDatabase()
    analyzer = BallotMeasureAnalyzer()

    guide = VoterGuide(
        election_name="Test Election",
        election_date="2024-11-05",
        jurisdiction="Test State",
        candidates=db.all_candidates,
        measures=analyzer.all_measures,
    )
    report.print_full_guide(guide)
    output = buf.getvalue()
    assert "Test Election" in output
    assert "Disclaimer" in output
