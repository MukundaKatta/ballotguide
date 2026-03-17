"""Impact estimation for policy proposals."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ballotguide.models import PolicyArea, PolicyPosition


class ImpactLevel(str, Enum):
    """Qualitative impact level based on available evidence."""

    MINIMAL = "minimal"
    MODERATE = "moderate"
    SIGNIFICANT = "significant"
    MAJOR = "major"
    UNCERTAIN = "uncertain"


class ImpactDirection(str, Enum):
    """Direction of projected impact, stated neutrally."""

    INCREASE = "increase"
    DECREASE = "decrease"
    MIXED = "mixed"
    NEUTRAL = "neutral"
    UNCERTAIN = "uncertain"


@dataclass
class PolicyImpactEstimate:
    """Projected impact of a policy position."""

    area: PolicyArea
    affected_populations: list[str]
    fiscal_direction: ImpactDirection
    fiscal_level: ImpactLevel
    employment_direction: ImpactDirection
    employment_level: ImpactLevel
    narrative: str
    caveats: list[str]


# Mapping from policy area to baseline impact assessment templates.
# These provide general frameworks; real analysis would require detailed
# economic modeling and data.
_IMPACT_TEMPLATES: dict[PolicyArea, dict] = {
    PolicyArea.ECONOMY: {
        "affected_populations": ["workers", "businesses", "consumers"],
        "default_caveats": [
            "Economic projections depend on multiple external factors.",
            "Actual outcomes may differ substantially from estimates.",
        ],
    },
    PolicyArea.HEALTHCARE: {
        "affected_populations": ["patients", "healthcare providers", "insurers", "taxpayers"],
        "default_caveats": [
            "Healthcare cost projections are inherently uncertain.",
            "Coverage effects depend on enrollment assumptions.",
        ],
    },
    PolicyArea.EDUCATION: {
        "affected_populations": ["students", "teachers", "school districts", "taxpayers"],
        "default_caveats": [
            "Educational outcomes are influenced by many factors beyond funding.",
            "Long-term effects may take years to measure.",
        ],
    },
    PolicyArea.IMMIGRATION: {
        "affected_populations": ["immigrants", "employers", "local communities", "federal agencies"],
        "default_caveats": [
            "Immigration policy effects depend on enforcement implementation.",
            "Economic effects of immigration are debated among researchers.",
        ],
    },
    PolicyArea.CLIMATE: {
        "affected_populations": ["energy sector workers", "consumers", "coastal communities", "agriculture"],
        "default_caveats": [
            "Climate policy effects unfold over decades.",
            "Cost estimates depend on technology development trajectories.",
        ],
    },
    PolicyArea.CRIMINAL_JUSTICE: {
        "affected_populations": ["defendants", "victims", "law enforcement", "communities"],
        "default_caveats": [
            "Recidivism effects depend on program implementation quality.",
            "Public safety outcomes are influenced by many factors.",
        ],
    },
    PolicyArea.HOUSING: {
        "affected_populations": ["renters", "homeowners", "developers", "local governments"],
        "default_caveats": [
            "Housing market effects depend on local conditions.",
            "Construction timelines may delay observable impacts.",
        ],
    },
    PolicyArea.TAXATION: {
        "affected_populations": ["individual taxpayers", "businesses", "state/local governments"],
        "default_caveats": [
            "Revenue projections depend on economic conditions.",
            "Behavioral responses to tax changes are difficult to predict.",
        ],
    },
    PolicyArea.INFRASTRUCTURE: {
        "affected_populations": ["commuters", "businesses", "construction workers", "taxpayers"],
        "default_caveats": [
            "Infrastructure project costs frequently exceed initial estimates.",
            "Completion timelines are subject to permitting and supply chain delays.",
        ],
    },
    PolicyArea.LABOR: {
        "affected_populations": ["workers", "employers", "unions", "consumers"],
        "default_caveats": [
            "Labor market effects depend on broader economic conditions.",
            "Wage and employment effects are debated among economists.",
        ],
    },
}


class ImpactEstimator:
    """Projects potential effects of policy positions.

    Estimates are presented with appropriate uncertainty and caveats.
    This tool does not advocate for or against any position; it provides
    a structured framework for understanding potential consequences.
    """

    def estimate(self, position: PolicyPosition) -> PolicyImpactEstimate:
        """Generate an impact estimate for a policy position.

        Args:
            position: The policy position to analyze.

        Returns:
            A PolicyImpactEstimate with projected effects and caveats.
        """
        template = _IMPACT_TEMPLATES.get(position.area, {})
        affected = template.get("affected_populations", ["general public"])
        caveats = list(template.get("default_caveats", [
            "Insufficient data for detailed impact projection.",
            "Estimates should be treated as preliminary.",
        ]))

        # Determine fiscal and employment direction based on stance
        fiscal_dir, fiscal_level = self._estimate_fiscal(position)
        emp_dir, emp_level = self._estimate_employment(position)

        narrative = self._build_narrative(position, fiscal_dir, emp_dir)

        return PolicyImpactEstimate(
            area=position.area,
            affected_populations=affected,
            fiscal_direction=fiscal_dir,
            fiscal_level=fiscal_level,
            employment_direction=emp_dir,
            employment_level=emp_level,
            narrative=narrative,
            caveats=caveats,
        )

    def estimate_multiple(self, positions: list[PolicyPosition]) -> list[PolicyImpactEstimate]:
        """Estimate impacts for multiple positions."""
        return [self.estimate(p) for p in positions]

    def _estimate_fiscal(self, position: PolicyPosition) -> tuple[ImpactDirection, ImpactLevel]:
        """Estimate fiscal direction and level from the position summary."""
        text = position.summary.lower()

        # Look for fiscal signals in the summary text
        spending_signals = ["fund", "invest", "expand", "increase", "subsid"]
        saving_signals = ["cut", "reduc", "eliminat", "streamlin", "lower"]

        has_spending = any(s in text for s in spending_signals)
        has_saving = any(s in text for s in saving_signals)

        if has_spending and has_saving:
            return ImpactDirection.MIXED, ImpactLevel.MODERATE
        if has_spending:
            return ImpactDirection.INCREASE, ImpactLevel.MODERATE
        if has_saving:
            return ImpactDirection.DECREASE, ImpactLevel.MODERATE
        return ImpactDirection.UNCERTAIN, ImpactLevel.UNCERTAIN

    def _estimate_employment(self, position: PolicyPosition) -> tuple[ImpactDirection, ImpactLevel]:
        """Estimate employment direction from the position summary."""
        text = position.summary.lower()

        job_positive = ["job", "employ", "hire", "workforce", "training"]
        job_negative = ["automat", "outsourc", "layoff", "downsiz"]

        has_positive = any(s in text for s in job_positive)
        has_negative = any(s in text for s in job_negative)

        if has_positive and has_negative:
            return ImpactDirection.MIXED, ImpactLevel.MODERATE
        if has_positive:
            return ImpactDirection.INCREASE, ImpactLevel.MINIMAL
        if has_negative:
            return ImpactDirection.DECREASE, ImpactLevel.MODERATE
        return ImpactDirection.UNCERTAIN, ImpactLevel.UNCERTAIN

    def _build_narrative(
        self,
        position: PolicyPosition,
        fiscal: ImpactDirection,
        employment: ImpactDirection,
    ) -> str:
        """Build a neutral narrative description of projected impacts."""
        area_name = position.area.value.replace("_", " ")
        parts = [
            f"This {area_name} position",
        ]

        if fiscal == ImpactDirection.INCREASE:
            parts.append("is projected to involve increased government expenditure")
        elif fiscal == ImpactDirection.DECREASE:
            parts.append("is projected to reduce government expenditure")
        elif fiscal == ImpactDirection.MIXED:
            parts.append("has mixed fiscal implications, with both costs and savings")
        else:
            parts.append("has uncertain fiscal implications based on available information")

        if employment == ImpactDirection.INCREASE:
            parts.append("and may have positive employment effects")
        elif employment == ImpactDirection.DECREASE:
            parts.append("and may affect employment levels")
        elif employment == ImpactDirection.MIXED:
            parts.append("with mixed employment effects across sectors")
        else:
            parts.append("with employment effects that are difficult to project")

        return ". ".join(parts) + ". All estimates are preliminary and subject to significant uncertainty."
