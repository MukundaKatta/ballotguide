"""Command-line interface for BallotGuide."""

from __future__ import annotations

import click
from rich.console import Console

from ballotguide.analyzer.bias import BiasDetector
from ballotguide.analyzer.impact import ImpactEstimator
from ballotguide.analyzer.positions import PositionTracker
from ballotguide.guide.candidates import CandidateDatabase
from ballotguide.guide.comparator import CandidateComparator
from ballotguide.guide.measures import BallotMeasureAnalyzer
from ballotguide.models import PolicyArea, VoterGuide
from ballotguide.report import ReportGenerator


console = Console()


@click.group()
@click.version_option(package_name="ballotguide")
def cli() -> None:
    """BallotGuide - AI Voter Guide (strictly non-partisan).

    Provides balanced, factual information about candidates and ballot
    measures to help voters make informed decisions.
    """


@cli.command()
def guide() -> None:
    """Display the full sample voter guide."""
    db = CandidateDatabase()
    analyzer = BallotMeasureAnalyzer()
    comparator = CandidateComparator(db)

    # Build comparisons for each contested office
    comparisons = []
    for office in db.list_offices():
        comp = comparator.compare_by_office(office)
        if comp and len(comp.candidates) >= 2:
            comparisons.append(comp)

    voter_guide = VoterGuide(
        election_name="Sample General Election 2024",
        election_date="November 5, 2024",
        jurisdiction="Sample State",
        candidates=db.all_candidates,
        measures=analyzer.all_measures,
        comparisons=comparisons,
    )

    report = ReportGenerator(console)
    report.print_full_guide(voter_guide)


@cli.command()
@click.argument("name", required=False)
def candidates(name: str | None) -> None:
    """List candidates or show details for a specific candidate."""
    db = CandidateDatabase()
    report = ReportGenerator(console)
    report.print_disclaimer()

    if name:
        results = db.search(name)
        if not results:
            console.print(f"[red]No candidates found matching '{name}'.[/red]")
            return
        for candidate in results:
            report.print_candidate(candidate)
    else:
        for candidate in db.all_candidates:
            incumbent = " (Incumbent)" if candidate.incumbent else ""
            console.print(f"  [bold]{candidate.name}[/bold]{incumbent} - {candidate.office}")
        console.print()
        console.print("[dim]Use 'ballotguide candidates <name>' for details.[/dim]")


@cli.command()
@click.argument("identifier", required=False)
def measures(identifier: str | None) -> None:
    """List ballot measures or show details for a specific one."""
    analyzer = BallotMeasureAnalyzer()
    report = ReportGenerator(console)
    report.print_disclaimer()

    if identifier:
        results = analyzer.search(identifier)
        if not results:
            console.print(f"[red]No measures found matching '{identifier}'.[/red]")
            return
        for measure in results:
            report.print_measure(measure)
    else:
        for measure in analyzer.all_measures:
            console.print(f"  [bold]{measure.identifier}:[/bold] {measure.title}")
        console.print()
        console.print("[dim]Use 'ballotguide measures <identifier>' for details.[/dim]")


@cli.command()
@click.argument("office")
def compare(office: str) -> None:
    """Compare candidates running for the same office."""
    db = CandidateDatabase()
    comparator = CandidateComparator(db)
    report = ReportGenerator(console)
    report.print_disclaimer()

    comparison = comparator.compare_by_office(office)
    if comparison is None:
        console.print(f"[red]No candidates found for office matching '{office}'.[/red]")
        console.print("[dim]Available offices:[/dim]")
        for office_name in db.list_offices():
            console.print(f"  - {office_name}")
        return

    report.print_comparison(comparison)


@cli.command("check-bias")
@click.argument("text")
def check_bias(text: str) -> None:
    """Check text for potentially biased language."""
    detector = BiasDetector()
    flags = detector.scan(text)

    if not flags:
        console.print("[green]No biased language detected. Text appears neutral.[/green]")
        return

    console.print(f"[yellow]Found {len(flags)} potential bias flag(s):[/yellow]")
    console.print()
    for flag in flags:
        severity_color = {"low": "dim", "medium": "yellow", "high": "red"}.get(flag.severity, "white")
        console.print(f"  [{severity_color}][{flag.severity.upper()}][/{severity_color}] \"{flag.text}\"")
        console.print(f"    Reason: {flag.reason}")
        console.print(f"    Suggestion: {flag.suggestion}")
        console.print()


@cli.command()
@click.argument("candidate_name")
def impact(candidate_name: str) -> None:
    """Show projected policy impact estimates for a candidate."""
    db = CandidateDatabase()
    report = ReportGenerator(console)
    report.print_disclaimer()

    results = db.search(candidate_name)
    if not results:
        console.print(f"[red]No candidate found matching '{candidate_name}'.[/red]")
        return

    estimator = ImpactEstimator()

    for candidate in results:
        console.print(f"\n[bold]Impact Estimates for {candidate.name}[/bold]\n")
        for pos in candidate.positions:
            est = estimator.estimate(pos)
            area_label = est.area.value.replace("_", " ").title()
            console.print(f"  [bold]{area_label}[/bold]")
            console.print(f"    Fiscal: {est.fiscal_direction.value} ({est.fiscal_level.value})")
            console.print(f"    Employment: {est.employment_direction.value} ({est.employment_level.value})")
            console.print(f"    {est.narrative}")
            if est.caveats:
                console.print(f"    Caveats: {'; '.join(est.caveats)}")
            console.print()


@cli.command()
@click.argument("candidate_name")
def coverage(candidate_name: str) -> None:
    """Show which policy areas a candidate has addressed."""
    db = CandidateDatabase()
    tracker = PositionTracker(db.all_candidates)

    results = db.search(candidate_name)
    if not results:
        console.print(f"[red]No candidate found matching '{candidate_name}'.[/red]")
        return

    for candidate in results:
        console.print(f"\n[bold]Policy Coverage for {candidate.name}[/bold]\n")
        report = tracker.coverage_report(candidate.name)
        for area, covered in report.items():
            label = area.value.replace("_", " ").title()
            status = "[green]Stated[/green]" if covered else "[dim]No position[/dim]"
            console.print(f"  {label:25s} {status}")

        gaps = tracker.coverage_gaps(candidate.name)
        if gaps:
            console.print(f"\n  [yellow]{len(gaps)} policy area(s) without a stated position.[/yellow]")
        console.print()


if __name__ == "__main__":
    cli()
