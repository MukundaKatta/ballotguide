"""Candidate database and lookup functionality."""

from __future__ import annotations

from ballotguide.models import (
    Candidate,
    Endorsement,
    PolicyArea,
    PolicyPosition,
    Stance,
    VotingRecord,
)


def _build_sample_candidates() -> list[Candidate]:
    """Build sample candidates for demonstration purposes.

    These are fictional candidates with realistic but fabricated positions.
    They are designed to illustrate diverse viewpoints without favoring
    any real-world party or ideology.
    """
    return [
        Candidate(
            name="Maria Santos",
            office="State Senate District 5",
            party="",
            incumbent=True,
            biography=(
                "Maria Santos has served in the State Senate since 2020. "
                "She previously worked as a public school principal for 12 years."
            ),
            website="https://example.com/santos",
            positions=[
                PolicyPosition(
                    area=PolicyArea.EDUCATION,
                    stance=Stance.SUPPORTS,
                    summary="Supports increased funding for public schools and universal pre-K.",
                    source="Campaign website, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.HEALTHCARE,
                    stance=Stance.SUPPORTS,
                    summary="Advocates expanding state Medicaid coverage and lowering prescription drug costs.",
                    source="Senate floor speech, March 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.ECONOMY,
                    stance=Stance.MIXED,
                    summary="Supports raising the minimum wage; opposes new business taxes on small firms.",
                    source="Town hall remarks, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.CLIMATE,
                    stance=Stance.SUPPORTS,
                    summary="Co-sponsored the Clean Energy Transition Act; supports renewable energy subsidies.",
                    source="Legislative record",
                ),
                PolicyPosition(
                    area=PolicyArea.IMMIGRATION,
                    stance=Stance.MIXED,
                    summary="Supports a path to legal status for long-term residents; favors increased border security funding.",
                    source="Campaign website, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.HOUSING,
                    stance=Stance.SUPPORTS,
                    summary="Authored bill to increase affordable housing construction through zoning reform.",
                    source="Senate Bill 1042",
                ),
                PolicyPosition(
                    area=PolicyArea.CRIMINAL_JUSTICE,
                    stance=Stance.SUPPORTS,
                    summary="Supports expanding diversion programs and investing in mental health crisis response.",
                    source="Committee testimony, 2023",
                ),
                PolicyPosition(
                    area=PolicyArea.TAXATION,
                    stance=Stance.MIXED,
                    summary="Voted for targeted tax credits for working families; opposed broad-based tax increases.",
                    source="Legislative voting record",
                ),
            ],
            voting_record=[
                VotingRecord(
                    bill_name="Clean Energy Transition Act",
                    vote="yes",
                    date="2023-06-15",
                    description="Mandates 80% renewable energy by 2040.",
                ),
                VotingRecord(
                    bill_name="School Funding Reform Act",
                    vote="yes",
                    date="2023-09-20",
                    description="Increases per-pupil funding by 12%.",
                ),
                VotingRecord(
                    bill_name="Business Tax Simplification Act",
                    vote="no",
                    date="2024-01-10",
                    description="Would have reduced corporate tax rate by 3%.",
                ),
            ],
            endorsements=[
                Endorsement(endorser="State Teachers Association", organization_type="labor union"),
                Endorsement(endorser="Clean Air Coalition", organization_type="environmental group"),
            ],
        ),
        Candidate(
            name="James Thornton",
            office="State Senate District 5",
            party="",
            incumbent=False,
            biography=(
                "James Thornton is a small business owner who has run a chain "
                "of hardware stores for 20 years. He serves on the county "
                "planning commission."
            ),
            website="https://example.com/thornton",
            positions=[
                PolicyPosition(
                    area=PolicyArea.EDUCATION,
                    stance=Stance.SUPPORTS,
                    summary="Supports school choice, including charter school expansion and education savings accounts.",
                    source="Campaign website, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.HEALTHCARE,
                    stance=Stance.MIXED,
                    summary="Favors market-based reforms to lower costs; opposes single-payer proposals; supports telehealth expansion.",
                    source="Candidate forum, April 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.ECONOMY,
                    stance=Stance.SUPPORTS,
                    summary="Proposes reducing regulations on small businesses and cutting state licensing fees.",
                    source="Campaign platform, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.CLIMATE,
                    stance=Stance.MIXED,
                    summary="Supports nuclear energy investment and natural gas as a bridge fuel; skeptical of renewable mandates.",
                    source="Editorial board interview, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.IMMIGRATION,
                    stance=Stance.SUPPORTS,
                    summary="Supports streamlined legal immigration for skilled workers; favors stricter enforcement of existing immigration law.",
                    source="Campaign website, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.HOUSING,
                    stance=Stance.SUPPORTS,
                    summary="Proposes reducing permitting barriers and impact fees to encourage private housing construction.",
                    source="Planning commission testimony, 2023",
                ),
                PolicyPosition(
                    area=PolicyArea.CRIMINAL_JUSTICE,
                    stance=Stance.SUPPORTS,
                    summary="Supports increased funding for law enforcement and opposes reducing mandatory minimum sentences.",
                    source="Campaign platform, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.TAXATION,
                    stance=Stance.OPPOSES,
                    summary="Opposes all new tax increases; supports a flat reduction in the state income tax rate.",
                    source="Campaign website, 2024",
                ),
            ],
            voting_record=[],
            endorsements=[
                Endorsement(endorser="Small Business Alliance", organization_type="business group"),
                Endorsement(endorser="County Sheriff's Association", organization_type="law enforcement"),
            ],
        ),
        Candidate(
            name="Linda Choi",
            office="City Council District 3",
            party="",
            incumbent=False,
            biography=(
                "Linda Choi is a civil engineer who has worked on municipal "
                "infrastructure projects for 15 years."
            ),
            website="https://example.com/choi",
            positions=[
                PolicyPosition(
                    area=PolicyArea.INFRASTRUCTURE,
                    stance=Stance.SUPPORTS,
                    summary="Proposes a comprehensive 10-year infrastructure plan including road, water, and broadband upgrades.",
                    source="Campaign platform, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.HOUSING,
                    stance=Stance.SUPPORTS,
                    summary="Supports mixed-use zoning reform and transit-oriented development.",
                    source="Campaign website, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.CLIMATE,
                    stance=Stance.SUPPORTS,
                    summary="Advocates green building standards and urban tree canopy expansion.",
                    source="Candidate forum, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.ECONOMY,
                    stance=Stance.SUPPORTS,
                    summary="Supports creating a city innovation district to attract technology companies.",
                    source="Campaign platform, 2024",
                ),
            ],
            endorsements=[
                Endorsement(endorser="Engineers for Good Government", organization_type="professional association"),
            ],
        ),
        Candidate(
            name="Robert Kim",
            office="City Council District 3",
            party="",
            incumbent=True,
            biography=(
                "Robert Kim has served on the City Council for 8 years. "
                "He is a retired firefighter and community volunteer."
            ),
            website="https://example.com/kim",
            positions=[
                PolicyPosition(
                    area=PolicyArea.INFRASTRUCTURE,
                    stance=Stance.SUPPORTS,
                    summary="Prioritizes repairing existing infrastructure before new construction; supports expanding public transit.",
                    source="Council meeting minutes, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.HOUSING,
                    stance=Stance.MIXED,
                    summary="Supports affordable housing mandates for new developments; cautious about upzoning single-family neighborhoods.",
                    source="Campaign website, 2024",
                ),
                PolicyPosition(
                    area=PolicyArea.CLIMATE,
                    stance=Stance.SUPPORTS,
                    summary="Voted for the city's climate action plan; supports electric vehicle infrastructure.",
                    source="Council voting record",
                ),
                PolicyPosition(
                    area=PolicyArea.CRIMINAL_JUSTICE,
                    stance=Stance.SUPPORTS,
                    summary="Advocates community policing and neighborhood watch programs; supports body camera mandates.",
                    source="Council resolution, 2023",
                ),
            ],
            endorsements=[
                Endorsement(endorser="Firefighters Local 237", organization_type="labor union"),
                Endorsement(endorser="Neighborhood Council Federation", organization_type="civic organization"),
            ],
        ),
    ]


class CandidateDatabase:
    """Non-partisan candidate information database.

    Provides lookup and filtering of candidates and their positions,
    voting records, and endorsements. All information is presented
    neutrally without editorial commentary.
    """

    def __init__(self, candidates: list[Candidate] | None = None) -> None:
        if candidates is None:
            candidates = _build_sample_candidates()
        self._candidates = {c.name: c for c in candidates}

    @property
    def all_candidates(self) -> list[Candidate]:
        """Return all candidates in the database."""
        return list(self._candidates.values())

    def get_candidate(self, name: str) -> Candidate | None:
        """Look up a candidate by exact name."""
        return self._candidates.get(name)

    def search(self, query: str) -> list[Candidate]:
        """Search candidates by name (case-insensitive substring match)."""
        q = query.lower()
        return [c for c in self._candidates.values() if q in c.name.lower()]

    def by_office(self, office: str) -> list[Candidate]:
        """Return all candidates running for a given office."""
        o = office.lower()
        return [c for c in self._candidates.values() if o in c.office.lower()]

    def get_positions(self, name: str, area: PolicyArea | None = None) -> list[PolicyPosition]:
        """Get a candidate's policy positions, optionally filtered by area."""
        candidate = self.get_candidate(name)
        if candidate is None:
            return []
        if area is None:
            return candidate.positions
        return [p for p in candidate.positions if p.area == area]

    def get_voting_record(self, name: str) -> list[VotingRecord]:
        """Get a candidate's voting record."""
        candidate = self.get_candidate(name)
        return candidate.voting_record if candidate else []

    def get_endorsements(self, name: str) -> list[Endorsement]:
        """Get a candidate's endorsements."""
        candidate = self.get_candidate(name)
        return candidate.endorsements if candidate else []

    def add_candidate(self, candidate: Candidate) -> None:
        """Add or update a candidate in the database."""
        self._candidates[candidate.name] = candidate

    def list_offices(self) -> list[str]:
        """Return a deduplicated list of offices being contested."""
        return sorted(set(c.office for c in self._candidates.values()))
