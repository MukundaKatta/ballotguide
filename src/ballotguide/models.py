"""Pydantic models for BallotGuide."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PolicyArea(str, Enum):
    """Policy areas tracked by the voter guide."""

    ECONOMY = "economy"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    IMMIGRATION = "immigration"
    CLIMATE = "climate"
    CRIMINAL_JUSTICE = "criminal_justice"
    HOUSING = "housing"
    TAXATION = "taxation"
    FOREIGN_POLICY = "foreign_policy"
    GUN_POLICY = "gun_policy"
    INFRASTRUCTURE = "infrastructure"
    LABOR = "labor"
    TECHNOLOGY = "technology"
    AGRICULTURE = "agriculture"
    VETERANS = "veterans"
    CIVIL_RIGHTS = "civil_rights"


class Stance(str, Enum):
    """A candidate's stance on an issue, described neutrally."""

    SUPPORTS = "supports"
    OPPOSES = "opposes"
    MIXED = "mixed"
    NO_POSITION = "no_position"


class PolicyPosition(BaseModel):
    """A candidate's position on a specific policy area."""

    area: PolicyArea
    stance: Stance
    summary: str = Field(
        ..., description="Neutral, factual description of the position"
    )
    source: str = Field(
        default="", description="Source or citation for this position"
    )


class VotingRecord(BaseModel):
    """A single entry in a candidate's voting record."""

    bill_name: str
    vote: str = Field(..., description="'yes', 'no', or 'abstain'")
    date: str
    description: str


class Endorsement(BaseModel):
    """An endorsement received by a candidate."""

    endorser: str
    organization_type: str = Field(
        default="", description="Type of organization, e.g. 'labor union', 'business group'"
    )


class Candidate(BaseModel):
    """Represents a candidate on the ballot."""

    name: str
    office: str
    party: str = Field(default="", description="Party affiliation, if any")
    incumbent: bool = False
    positions: list[PolicyPosition] = Field(default_factory=list)
    voting_record: list[VotingRecord] = Field(default_factory=list)
    endorsements: list[Endorsement] = Field(default_factory=list)
    biography: str = ""
    website: str = ""


class FiscalImpact(BaseModel):
    """Projected fiscal impact of a ballot measure."""

    estimated_cost: str = ""
    revenue_effect: str = ""
    funding_source: str = ""
    summary: str = ""


class BallotMeasure(BaseModel):
    """Represents a ballot measure or proposition."""

    identifier: str = Field(..., description="e.g. 'Proposition 1', 'Measure A'")
    title: str
    summary: str
    full_text_url: str = ""
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    fiscal_impact: Optional[FiscalImpact] = None
    supporters: list[str] = Field(default_factory=list)
    opponents: list[str] = Field(default_factory=list)


class CandidateComparison(BaseModel):
    """Side-by-side comparison of candidates on issues."""

    office: str
    candidates: list[str]
    issues: list[PolicyArea]
    comparison_rows: list[dict[str, str]] = Field(
        default_factory=list,
        description="Each dict maps candidate name to their stance summary for an issue",
    )


class VoterGuide(BaseModel):
    """Complete voter guide for a given election."""

    election_name: str
    election_date: str
    jurisdiction: str
    candidates: list[Candidate] = Field(default_factory=list)
    measures: list[BallotMeasure] = Field(default_factory=list)
    comparisons: list[CandidateComparison] = Field(default_factory=list)
    disclaimer: str = Field(
        default=(
            "This voter guide is strictly non-partisan. It does not endorse "
            "or oppose any candidate or measure. Information is presented for "
            "educational purposes only. Voters are encouraged to conduct their "
            "own research."
        )
    )
