"""Position tracking across 15+ policy areas."""

from __future__ import annotations

from collections import defaultdict

from ballotguide.models import Candidate, PolicyArea, PolicyPosition, Stance


class PositionTracker:
    """Tracks and organizes candidate positions across policy areas.

    Covers 16 policy areas: economy, healthcare, education, immigration,
    climate, criminal justice, housing, taxation, foreign policy,
    gun policy, infrastructure, labor, technology, agriculture,
    veterans, and civil rights.

    All tracking is strictly factual and non-partisan.
    """

    ALL_POLICY_AREAS: list[PolicyArea] = list(PolicyArea)

    def __init__(self, candidates: list[Candidate] | None = None) -> None:
        self._candidates = {c.name: c for c in (candidates or [])}

    def add_candidate(self, candidate: Candidate) -> None:
        """Register a candidate for tracking."""
        self._candidates[candidate.name] = candidate

    def get_position(self, candidate_name: str, area: PolicyArea) -> PolicyPosition | None:
        """Get a single candidate's position on a specific area."""
        candidate = self._candidates.get(candidate_name)
        if candidate is None:
            return None
        for pos in candidate.positions:
            if pos.area == area:
                return pos
        return None

    def positions_by_area(self, area: PolicyArea) -> dict[str, PolicyPosition | None]:
        """Get all candidates' positions on a given policy area.

        Returns a dict mapping candidate name to their position (or None).
        """
        result: dict[str, PolicyPosition | None] = {}
        for name, candidate in self._candidates.items():
            match = None
            for pos in candidate.positions:
                if pos.area == area:
                    match = pos
                    break
            result[name] = match
        return result

    def coverage_report(self, candidate_name: str) -> dict[PolicyArea, bool]:
        """Show which policy areas a candidate has stated positions on."""
        candidate = self._candidates.get(candidate_name)
        covered_areas = {pos.area for pos in candidate.positions} if candidate else set()
        return {area: area in covered_areas for area in self.ALL_POLICY_AREAS}

    def coverage_gaps(self, candidate_name: str) -> list[PolicyArea]:
        """Return policy areas where a candidate has no stated position."""
        report = self.coverage_report(candidate_name)
        return [area for area, covered in report.items() if not covered]

    def stance_summary(self) -> dict[str, dict[PolicyArea, Stance]]:
        """Return a summary of stances: candidate -> area -> stance."""
        result: dict[str, dict[PolicyArea, Stance]] = {}
        for name, candidate in self._candidates.items():
            stances: dict[PolicyArea, Stance] = {}
            for pos in candidate.positions:
                stances[pos.area] = pos.stance
            result[name] = stances
        return result

    def find_agreement(self, name1: str, name2: str) -> list[PolicyArea]:
        """Find policy areas where two candidates share the same stance."""
        c1 = self._candidates.get(name1)
        c2 = self._candidates.get(name2)
        if not c1 or not c2:
            return []

        stances1 = {p.area: p.stance for p in c1.positions}
        stances2 = {p.area: p.stance for p in c2.positions}

        return [
            area
            for area in stances1
            if area in stances2 and stances1[area] == stances2[area]
        ]

    def find_disagreement(self, name1: str, name2: str) -> list[PolicyArea]:
        """Find policy areas where two candidates have different stances."""
        c1 = self._candidates.get(name1)
        c2 = self._candidates.get(name2)
        if not c1 or not c2:
            return []

        stances1 = {p.area: p.stance for p in c1.positions}
        stances2 = {p.area: p.stance for p in c2.positions}

        return [
            area
            for area in stances1
            if area in stances2 and stances1[area] != stances2[area]
        ]
