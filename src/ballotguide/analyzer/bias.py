"""Bias detection to ensure neutral, non-partisan language."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class BiasFlag:
    """A detected instance of potentially biased language."""

    text: str
    reason: str
    suggestion: str
    severity: str = "low"  # low, medium, high


# Words and phrases that may indicate bias in voter guide language.
# Organized by category for clarity.
_BIASED_PATTERNS: list[tuple[str, str, str]] = [
    # Positive bias toward a position
    (r"\bcommon[- ]sense\b", "Implies opposing views lack common sense", "Describe the policy specifics instead"),
    (r"\bbold\b", "Editorializes the nature of a proposal", "Use 'significant' or describe the scope factually"),
    (r"\bbrave\b", "Assigns positive character judgment", "Describe the action without characterizing courage"),
    (r"\blandmark\b", "Editorializes significance", "Describe the scope or impact factually"),
    (r"\bgroundbreaking\b", "Editorializes significance", "Describe what is new about the proposal"),
    (r"\bvisionary\b", "Assigns positive character judgment", "Describe the proposal's goals factually"),
    (r"\bheroic\b", "Assigns positive character judgment", "Describe the action factually"),
    (r"\bcompassionate\b", "Assigns positive character judgment", "Describe the policy's intended beneficiaries"),
    # Negative bias toward a position
    (r"\breckless\b", "Assigns negative judgment to a policy", "Describe specific risks or concerns"),
    (r"\bdangerous\b", "May overstate risk without evidence", "Cite specific risks or expert assessments"),
    (r"\bextreme\b", "Labels a position rather than describing it", "Describe the position's specifics"),
    (r"\bradical\b", "Labels a position rather than describing it", "Describe how the proposal differs from current policy"),
    (r"\bfailed\b", "May prejudge outcomes", "Describe specific results or lack of stated goals met"),
    (r"\bdisastrous\b", "Editorializes outcomes", "Describe specific negative outcomes with evidence"),
    (r"\birresponsible\b", "Assigns negative character judgment", "Describe specific concerns about the approach"),
    (r"\bweak\b", "Assigns negative judgment", "Describe specific limitations or gaps"),
    # Partisan framing
    (r"\bleft[- ]wing\b", "Partisan label", "Describe the policy position itself"),
    (r"\bright[- ]wing\b", "Partisan label", "Describe the policy position itself"),
    (r"\bliberal agenda\b", "Partisan framing", "Describe the specific policy proposals"),
    (r"\bconservative agenda\b", "Partisan framing", "Describe the specific policy proposals"),
    (r"\bsocialist\b", "Partisan label that may not be accurate", "Describe the specific economic policy"),
    (r"\bfascist\b", "Partisan label that may not be accurate", "Describe the specific policy"),
    (r"\bwoke\b", "Politically charged term", "Describe the specific social policy"),
    (r"\bnanny state\b", "Partisan framing", "Describe the specific regulation"),
    # Loaded emotional language
    (r"\bjob[- ]killing\b", "Loaded economic framing", "Describe projected employment effects with data"),
    (r"\btax[- ]and[- ]spend\b", "Partisan fiscal framing", "Describe the fiscal approach factually"),
    (r"\bcrush(ing|ed)?\b", "Emotionally loaded", "Describe the specific impact with evidence"),
    (r"\bdestroy(s|ed|ing)?\b", "Emotionally loaded unless describing physical destruction", "Describe specific effects"),
    (r"\bsavage\b", "Emotionally loaded", "Describe the specific impact"),
    (r"\boutrageous\b", "Editorializes", "Describe what is objectionable and to whom"),
    (r"\bshameful\b", "Assigns moral judgment", "Describe the criticism and its source"),
]


class BiasDetector:
    """Scans text for potentially biased or non-neutral language.

    This tool helps ensure that voter guide content maintains a strictly
    non-partisan tone. It flags loaded language, partisan labels, and
    editorial commentary, offering neutral alternatives.
    """

    def __init__(self, extra_patterns: list[tuple[str, str, str]] | None = None) -> None:
        self._patterns = list(_BIASED_PATTERNS)
        if extra_patterns:
            self._patterns.extend(extra_patterns)
        # Pre-compile patterns
        self._compiled = [
            (re.compile(pat, re.IGNORECASE), reason, suggestion)
            for pat, reason, suggestion in self._patterns
        ]

    def scan(self, text: str) -> list[BiasFlag]:
        """Scan text and return a list of bias flags.

        Args:
            text: The text to analyze for biased language.

        Returns:
            A list of BiasFlag instances for each detected issue.
        """
        flags: list[BiasFlag] = []
        for pattern, reason, suggestion in self._compiled:
            for match in pattern.finditer(text):
                severity = self._assess_severity(match.group(), reason)
                flags.append(
                    BiasFlag(
                        text=match.group(),
                        reason=reason,
                        suggestion=suggestion,
                        severity=severity,
                    )
                )
        return flags

    def is_neutral(self, text: str) -> bool:
        """Return True if no bias flags are detected in the text."""
        return len(self.scan(text)) == 0

    def neutralize(self, text: str) -> tuple[str, list[BiasFlag]]:
        """Attempt to flag biased language. Returns the original text
        and any flags found.

        Note: Automatic rewriting is not performed because neutral
        alternatives depend on context. The flags provide guidance
        for manual revision.
        """
        flags = self.scan(text)
        return text, flags

    def _assess_severity(self, matched_text: str, reason: str) -> str:
        """Heuristic severity assessment."""
        if "partisan" in reason.lower() or "label" in reason.lower():
            return "high"
        if "judgment" in reason.lower() or "emotional" in reason.lower():
            return "medium"
        return "low"
