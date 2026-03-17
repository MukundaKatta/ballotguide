"""Tests for pydantic models."""

from ballotguide.models import (
    BallotMeasure,
    Candidate,
    CandidateComparison,
    FiscalImpact,
    PolicyArea,
    PolicyPosition,
    Stance,
    VoterGuide,
)


def test_policy_position_creation():
    pos = PolicyPosition(
        area=PolicyArea.ECONOMY,
        stance=Stance.SUPPORTS,
        summary="Supports raising the minimum wage.",
    )
    assert pos.area == PolicyArea.ECONOMY
    assert pos.stance == Stance.SUPPORTS
    assert "minimum wage" in pos.summary


def test_candidate_defaults():
    c = Candidate(name="Test Person", office="Mayor")
    assert c.name == "Test Person"
    assert c.party == ""
    assert c.incumbent is False
    assert c.positions == []
    assert c.voting_record == []
    assert c.endorsements == []


def test_candidate_with_positions():
    c = Candidate(
        name="Test Person",
        office="Mayor",
        positions=[
            PolicyPosition(
                area=PolicyArea.HEALTHCARE,
                stance=Stance.MIXED,
                summary="Supports expanding coverage; opposes single-payer.",
            )
        ],
    )
    assert len(c.positions) == 1
    assert c.positions[0].area == PolicyArea.HEALTHCARE


def test_ballot_measure():
    m = BallotMeasure(
        identifier="Prop 99",
        title="Test Measure",
        summary="A measure for testing.",
        pros=["Pro 1", "Pro 2"],
        cons=["Con 1"],
    )
    assert m.identifier == "Prop 99"
    assert len(m.pros) == 2
    assert len(m.cons) == 1


def test_fiscal_impact():
    fi = FiscalImpact(
        estimated_cost="$1 billion",
        revenue_effect="None",
        funding_source="General fund",
        summary="Costs one billion dollars.",
    )
    assert "billion" in fi.estimated_cost


def test_voter_guide_disclaimer():
    vg = VoterGuide(
        election_name="Test Election",
        election_date="2024-11-05",
        jurisdiction="Test City",
    )
    assert "non-partisan" in vg.disclaimer


def test_policy_area_enum_has_16_areas():
    assert len(PolicyArea) >= 16


def test_candidate_comparison():
    comp = CandidateComparison(
        office="Mayor",
        candidates=["A", "B"],
        issues=[PolicyArea.ECONOMY],
        comparison_rows=[{"issue": "economy", "A": "Supports X", "B": "Opposes X"}],
    )
    assert len(comp.comparison_rows) == 1
