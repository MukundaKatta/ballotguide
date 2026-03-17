"""Tests for bias detection."""

from ballotguide.analyzer.bias import BiasDetector


def test_neutral_text():
    detector = BiasDetector()
    assert detector.is_neutral("The candidate supports increasing education funding.")


def test_detect_partisan_label():
    detector = BiasDetector()
    flags = detector.scan("This left-wing proposal would change the tax code.")
    assert len(flags) >= 1
    assert any("partisan" in f.reason.lower() or "label" in f.reason.lower() for f in flags)


def test_detect_loaded_language():
    detector = BiasDetector()
    flags = detector.scan("This reckless policy would destroy jobs.")
    assert len(flags) >= 2


def test_detect_positive_bias():
    detector = BiasDetector()
    flags = detector.scan("This bold, visionary leader proposed a groundbreaking plan.")
    assert len(flags) >= 2


def test_severity_levels():
    detector = BiasDetector()
    flags = detector.scan("The radical socialist agenda is dangerous.")
    severities = {f.severity for f in flags}
    assert "high" in severities


def test_suggestions_provided():
    detector = BiasDetector()
    flags = detector.scan("This extreme position is outrageous.")
    for flag in flags:
        assert flag.suggestion, f"No suggestion for flag: {flag.text}"


def test_neutralize_returns_flags():
    detector = BiasDetector()
    text, flags = detector.neutralize("A common-sense approach.")
    assert len(flags) >= 1
    assert text == "A common-sense approach."


def test_custom_patterns():
    detector = BiasDetector(extra_patterns=[
        (r"\bfantastic\b", "Overly positive", "Use neutral language"),
    ])
    flags = detector.scan("This is a fantastic proposal.")
    assert len(flags) >= 1


def test_case_insensitive():
    detector = BiasDetector()
    flags = detector.scan("This RADICAL plan is EXTREME.")
    assert len(flags) >= 2


def test_sample_candidate_summaries_are_neutral():
    """Verify that sample candidate position summaries pass bias detection."""
    from ballotguide.guide.candidates import CandidateDatabase

    detector = BiasDetector()
    db = CandidateDatabase()
    for candidate in db.all_candidates:
        for pos in candidate.positions:
            flags = detector.scan(pos.summary)
            assert not flags, (
                f"Biased language in {candidate.name}'s {pos.area.value} position: "
                f"{[f.text for f in flags]}"
            )
