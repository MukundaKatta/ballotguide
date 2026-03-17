"""Tests for ballot measure analyzer."""

from ballotguide.guide.measures import BallotMeasureAnalyzer


def test_default_measures():
    analyzer = BallotMeasureAnalyzer()
    assert len(analyzer.all_measures) >= 3


def test_get_measure():
    analyzer = BallotMeasureAnalyzer()
    m = analyzer.get_measure("Proposition 1")
    assert m is not None
    assert "Water" in m.title


def test_get_measure_not_found():
    analyzer = BallotMeasureAnalyzer()
    assert analyzer.get_measure("Prop 999") is None


def test_search():
    analyzer = BallotMeasureAnalyzer()
    results = analyzer.search("transit")
    assert len(results) >= 1


def test_pros_and_cons_balanced():
    """Each sample measure should have both pros and cons."""
    analyzer = BallotMeasureAnalyzer()
    for measure in analyzer.all_measures:
        assert len(measure.pros) >= 2, f"{measure.identifier} has too few pros"
        assert len(measure.cons) >= 2, f"{measure.identifier} has too few cons"


def test_fiscal_impact_present():
    analyzer = BallotMeasureAnalyzer()
    for measure in analyzer.all_measures:
        assert measure.fiscal_impact is not None, f"{measure.identifier} missing fiscal impact"


def test_summarize():
    analyzer = BallotMeasureAnalyzer()
    summary = analyzer.summarize("Proposition 1")
    assert summary["identifier"] == "Proposition 1"
    assert "pros" in summary
    assert "cons" in summary
    assert "fiscal_impact" in summary


def test_summarize_not_found():
    analyzer = BallotMeasureAnalyzer()
    assert analyzer.summarize("Nonexistent") == {}


def test_supporters_and_opponents():
    """Each sample measure should list both supporters and opponents."""
    analyzer = BallotMeasureAnalyzer()
    for measure in analyzer.all_measures:
        assert len(measure.supporters) >= 1, f"{measure.identifier} has no supporters listed"
        assert len(measure.opponents) >= 1, f"{measure.identifier} has no opponents listed"
