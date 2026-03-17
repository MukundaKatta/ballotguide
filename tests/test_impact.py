"""Tests for impact estimator."""

from ballotguide.analyzer.impact import ImpactDirection, ImpactEstimator, ImpactLevel
from ballotguide.models import PolicyArea, PolicyPosition, Stance


def test_estimate_spending_position():
    estimator = ImpactEstimator()
    pos = PolicyPosition(
        area=PolicyArea.EDUCATION,
        stance=Stance.SUPPORTS,
        summary="Supports increased funding for public schools.",
    )
    result = estimator.estimate(pos)
    assert result.area == PolicyArea.EDUCATION
    assert result.fiscal_direction == ImpactDirection.INCREASE
    assert len(result.caveats) >= 1


def test_estimate_cutting_position():
    estimator = ImpactEstimator()
    pos = PolicyPosition(
        area=PolicyArea.TAXATION,
        stance=Stance.SUPPORTS,
        summary="Supports cutting the income tax rate.",
    )
    result = estimator.estimate(pos)
    assert result.fiscal_direction == ImpactDirection.DECREASE


def test_estimate_mixed_position():
    estimator = ImpactEstimator()
    pos = PolicyPosition(
        area=PolicyArea.ECONOMY,
        stance=Stance.MIXED,
        summary="Supports expanding job training while reducing subsidies.",
    )
    result = estimator.estimate(pos)
    assert result.fiscal_direction == ImpactDirection.MIXED


def test_estimate_has_narrative():
    estimator = ImpactEstimator()
    pos = PolicyPosition(
        area=PolicyArea.HEALTHCARE,
        stance=Stance.SUPPORTS,
        summary="Supports expanding Medicaid coverage.",
    )
    result = estimator.estimate(pos)
    assert len(result.narrative) > 0
    assert "uncertainty" in result.narrative.lower()


def test_estimate_multiple():
    estimator = ImpactEstimator()
    positions = [
        PolicyPosition(area=PolicyArea.ECONOMY, stance=Stance.SUPPORTS, summary="Supports investment."),
        PolicyPosition(area=PolicyArea.EDUCATION, stance=Stance.SUPPORTS, summary="Supports funding."),
    ]
    results = estimator.estimate_multiple(positions)
    assert len(results) == 2


def test_affected_populations():
    estimator = ImpactEstimator()
    pos = PolicyPosition(
        area=PolicyArea.HEALTHCARE,
        stance=Stance.SUPPORTS,
        summary="Supports expanding coverage.",
    )
    result = estimator.estimate(pos)
    assert "patients" in result.affected_populations
