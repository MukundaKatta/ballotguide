"""Ballot measure analysis - pros, cons, and fiscal impact."""

from __future__ import annotations

from ballotguide.models import BallotMeasure, FiscalImpact


def _build_sample_measures() -> list[BallotMeasure]:
    """Build sample ballot measures for demonstration.

    These are fictional measures designed to illustrate balanced
    presentation of arguments for and against.
    """
    return [
        BallotMeasure(
            identifier="Proposition 1",
            title="Clean Water Infrastructure Bond",
            summary=(
                "Authorizes $2.5 billion in state bonds to fund upgrades to "
                "water treatment plants, replace aging pipelines, and improve "
                "stormwater management systems."
            ),
            pros=[
                "Addresses documented deficiencies in aging water infrastructure.",
                "Creates an estimated 15,000 construction and engineering jobs.",
                "Improves water quality and reduces risk of contamination events.",
                "Includes provisions for disadvantaged community water systems.",
            ],
            cons=[
                "Increases state debt and annual debt service payments by approximately $160 million.",
                "Bond financing costs mean taxpayers pay roughly $4.1 billion total over 30 years.",
                "Some analysts argue pay-as-you-go funding would be more cost-effective.",
                "Does not address long-term operational and maintenance funding.",
            ],
            fiscal_impact=FiscalImpact(
                estimated_cost="$2.5 billion in bond principal",
                revenue_effect="No direct revenue; estimated $160 million/year in debt service",
                funding_source="General obligation bonds repaid from the General Fund",
                summary=(
                    "Total cost to taxpayers over the 30-year bond term is estimated at "
                    "$4.1 billion including interest. Annual debt service of approximately "
                    "$160 million would come from the state General Fund."
                ),
            ),
            supporters=["State Water Engineers Association", "Environmental Defense Fund"],
            opponents=["Taxpayers for Fiscal Responsibility", "State Chamber of Commerce"],
        ),
        BallotMeasure(
            identifier="Measure A",
            title="Local Sales Tax Increase for Public Transit",
            summary=(
                "Increases the city sales tax by 0.5% to fund expansion of "
                "bus rapid transit lines, improved bus frequency, and reduced "
                "fares for low-income riders."
            ),
            pros=[
                "Provides dedicated, stable funding source for transit improvements.",
                "Projected to reduce average commute times by 12% within 5 years.",
                "Reduced fares would benefit approximately 40,000 low-income riders.",
                "May reduce traffic congestion and vehicle emissions.",
            ],
            cons=[
                "Sales taxes are regressive, disproportionately affecting lower-income consumers.",
                "Tax increase is permanent with no sunset clause.",
                "Transit ridership projections may be optimistic based on historical trends.",
                "Some neighborhoods would not see service improvements for 8-10 years.",
            ],
            fiscal_impact=FiscalImpact(
                estimated_cost="Implementation costs approximately $800 million over 10 years",
                revenue_effect="Generates an estimated $120 million annually",
                funding_source="0.5% increase in local sales tax",
                summary=(
                    "The 0.5% sales tax increase is projected to generate $120 million "
                    "per year. Over the 10-year capital plan, approximately $800 million "
                    "would be spent on transit expansion and fare subsidies."
                ),
            ),
            supporters=["Transit Riders Union", "Downtown Business Association"],
            opponents=["Anti-Tax Coalition", "Suburban Neighborhood Alliance"],
        ),
        BallotMeasure(
            identifier="Proposition 3",
            title="Criminal Sentencing Reform Act",
            summary=(
                "Reclassifies certain non-violent felonies as misdemeanors, "
                "expands eligibility for diversion programs, and redirects "
                "a portion of state prison savings to community-based "
                "rehabilitation services."
            ),
            pros=[
                "Projected to reduce state prison population by approximately 8,000 inmates.",
                "Estimated $450 million in annual prison cost savings.",
                "Evidence from other jurisdictions suggests diversion programs reduce recidivism.",
                "Directs savings to substance abuse treatment and job training programs.",
            ],
            cons=[
                "Critics argue reclassification could reduce deterrence for property crimes.",
                "Law enforcement groups express concern about repeat offenders receiving lighter sentences.",
                "Savings projections depend on assumptions about reduced incarceration that may not materialize.",
                "Implementation requires coordination across 58 county court systems.",
            ],
            fiscal_impact=FiscalImpact(
                estimated_cost="$50 million in initial implementation costs",
                revenue_effect="Estimated $450 million/year in prison cost savings after full implementation",
                funding_source="Savings redirected from Department of Corrections budget",
                summary=(
                    "Initial implementation costs of approximately $50 million for court "
                    "system changes and program setup. Once fully implemented, estimated "
                    "annual savings of $450 million from reduced incarceration costs, with "
                    "a portion directed to community rehabilitation programs."
                ),
            ),
            supporters=["Criminal Justice Reform Alliance", "Public Defenders Association"],
            opponents=["State Police Officers Association", "Victims' Rights Coalition"],
        ),
    ]


class BallotMeasureAnalyzer:
    """Analyzes ballot measures with balanced presentation of pros, cons,
    and fiscal impact.

    All analysis is strictly non-partisan. Arguments for and against are
    presented with equal weight and sourcing.
    """

    def __init__(self, measures: list[BallotMeasure] | None = None) -> None:
        if measures is None:
            measures = _build_sample_measures()
        self._measures = {m.identifier: m for m in measures}

    @property
    def all_measures(self) -> list[BallotMeasure]:
        """Return all ballot measures."""
        return list(self._measures.values())

    def get_measure(self, identifier: str) -> BallotMeasure | None:
        """Look up a measure by its identifier."""
        return self._measures.get(identifier)

    def search(self, query: str) -> list[BallotMeasure]:
        """Search measures by title or identifier (case-insensitive)."""
        q = query.lower()
        return [
            m
            for m in self._measures.values()
            if q in m.identifier.lower() or q in m.title.lower()
        ]

    def get_pros(self, identifier: str) -> list[str]:
        """Get arguments in favor of a measure."""
        measure = self.get_measure(identifier)
        return measure.pros if measure else []

    def get_cons(self, identifier: str) -> list[str]:
        """Get arguments against a measure."""
        measure = self.get_measure(identifier)
        return measure.cons if measure else []

    def get_fiscal_impact(self, identifier: str) -> FiscalImpact | None:
        """Get the fiscal impact analysis for a measure."""
        measure = self.get_measure(identifier)
        return measure.fiscal_impact if measure else None

    def summarize(self, identifier: str) -> dict[str, object]:
        """Return a balanced summary dict for a measure."""
        measure = self.get_measure(identifier)
        if measure is None:
            return {}
        return {
            "identifier": measure.identifier,
            "title": measure.title,
            "summary": measure.summary,
            "pros": measure.pros,
            "cons": measure.cons,
            "fiscal_impact": measure.fiscal_impact.model_dump() if measure.fiscal_impact else None,
            "supporters": measure.supporters,
            "opponents": measure.opponents,
        }

    def add_measure(self, measure: BallotMeasure) -> None:
        """Add or update a ballot measure."""
        self._measures[measure.identifier] = measure
