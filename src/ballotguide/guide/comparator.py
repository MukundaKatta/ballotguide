"""Side-by-side candidate comparison on issues."""

from __future__ import annotations

from ballotguide.guide.candidates import CandidateDatabase
from ballotguide.models import CandidateComparison, PolicyArea, Stance


class CandidateComparator:
    """Generates non-partisan side-by-side comparisons of candidates.

    Comparisons present each candidate's stated position on the same
    issues, without editorial judgment or ranking.
    """

    def __init__(self, db: CandidateDatabase | None = None) -> None:
        self._db = db or CandidateDatabase()

    def compare_by_office(
        self,
        office: str,
        issues: list[PolicyArea] | None = None,
    ) -> CandidateComparison | None:
        """Compare all candidates running for a given office.

        Args:
            office: The office to look up candidates for.
            issues: Policy areas to compare on. If None, uses all areas
                where at least one candidate has a stated position.

        Returns:
            A CandidateComparison, or None if no candidates found.
        """
        candidates = self._db.by_office(office)
        if not candidates:
            return None

        # Determine which issues to compare
        if issues is None:
            issue_set: set[PolicyArea] = set()
            for c in candidates:
                for p in c.positions:
                    issue_set.add(p.area)
            issues = sorted(issue_set, key=lambda a: a.value)

        if not issues:
            return None

        names = [c.name for c in candidates]

        # Build comparison rows: one per issue
        comparison_rows: list[dict[str, str]] = []
        for area in issues:
            row: dict[str, str] = {"issue": area.value}
            for c in candidates:
                matching = [p for p in c.positions if p.area == area]
                if matching:
                    pos = matching[0]
                    row[c.name] = f"[{pos.stance.value}] {pos.summary}"
                else:
                    row[c.name] = f"[{Stance.NO_POSITION.value}] No stated position on this issue."
            comparison_rows.append(row)

        return CandidateComparison(
            office=office,
            candidates=names,
            issues=issues,
            comparison_rows=comparison_rows,
        )

    def compare_candidates(
        self,
        names: list[str],
        issues: list[PolicyArea] | None = None,
    ) -> CandidateComparison | None:
        """Compare specific candidates by name.

        Args:
            names: List of candidate names.
            issues: Policy areas to compare on.

        Returns:
            A CandidateComparison, or None if candidates not found.
        """
        candidates = [self._db.get_candidate(n) for n in names]
        candidates = [c for c in candidates if c is not None]

        if len(candidates) < 2:
            return None

        if issues is None:
            issue_set: set[PolicyArea] = set()
            for c in candidates:
                for p in c.positions:
                    issue_set.add(p.area)
            issues = sorted(issue_set, key=lambda a: a.value)

        comparison_rows: list[dict[str, str]] = []
        for area in issues:
            row: dict[str, str] = {"issue": area.value}
            for c in candidates:
                matching = [p for p in c.positions if p.area == area]
                if matching:
                    pos = matching[0]
                    row[c.name] = f"[{pos.stance.value}] {pos.summary}"
                else:
                    row[c.name] = f"[{Stance.NO_POSITION.value}] No stated position on this issue."
            comparison_rows.append(row)

        office = candidates[0].office if all(c.office == candidates[0].office for c in candidates) else "Multiple offices"

        return CandidateComparison(
            office=office,
            candidates=[c.name for c in candidates],
            issues=issues,
            comparison_rows=comparison_rows,
        )
