"""Report generation for voter guides using Rich."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ballotguide.analyzer.bias import BiasDetector
from ballotguide.guide.candidates import CandidateDatabase
from ballotguide.guide.comparator import CandidateComparator
from ballotguide.guide.measures import BallotMeasureAnalyzer
from ballotguide.models import BallotMeasure, Candidate, CandidateComparison, VoterGuide


_DISCLAIMER = (
    "DISCLAIMER: This voter guide is strictly non-partisan. It does not "
    "endorse or oppose any candidate or measure. Information is presented "
    "for educational purposes only. Voters are encouraged to conduct "
    "their own research."
)


class ReportGenerator:
    """Generates formatted voter guide reports using Rich.

    All output is strictly non-partisan and balanced.
    """

    def __init__(self, console: Console | None = None) -> None:
        self.console = console or Console()

    def print_disclaimer(self) -> None:
        """Print the non-partisan disclaimer."""
        self.console.print()
        self.console.print(
            Panel(
                _DISCLAIMER,
                title="Non-Partisan Voter Guide",
                border_style="blue",
            )
        )
        self.console.print()

    def print_candidate(self, candidate: Candidate) -> None:
        """Print a single candidate's profile."""
        title = candidate.name
        if candidate.incumbent:
            title += " (Incumbent)"

        self.console.print(Panel(f"[bold]{title}[/bold]", subtitle=candidate.office, border_style="cyan"))

        if candidate.biography:
            self.console.print(f"  {candidate.biography}")
            self.console.print()

        if candidate.positions:
            table = Table(title="Policy Positions", show_lines=True)
            table.add_column("Policy Area", style="bold", width=20)
            table.add_column("Stance", width=12)
            table.add_column("Summary", ratio=3)

            for pos in candidate.positions:
                area_label = pos.area.value.replace("_", " ").title()
                stance_color = {
                    "supports": "green",
                    "opposes": "red",
                    "mixed": "yellow",
                    "no_position": "dim",
                }.get(pos.stance.value, "white")
                table.add_row(
                    area_label,
                    f"[{stance_color}]{pos.stance.value}[/{stance_color}]",
                    pos.summary,
                )
            self.console.print(table)

        if candidate.voting_record:
            self.console.print()
            vote_table = Table(title="Voting Record", show_lines=True)
            vote_table.add_column("Bill", width=30)
            vote_table.add_column("Vote", width=10)
            vote_table.add_column("Date", width=12)
            vote_table.add_column("Description", ratio=2)
            for vr in candidate.voting_record:
                vote_table.add_row(vr.bill_name, vr.vote, vr.date, vr.description)
            self.console.print(vote_table)

        if candidate.endorsements:
            self.console.print()
            self.console.print("[bold]Endorsements:[/bold]")
            for e in candidate.endorsements:
                org_info = f" ({e.organization_type})" if e.organization_type else ""
                self.console.print(f"  - {e.endorser}{org_info}")

        self.console.print()

    def print_measure(self, measure: BallotMeasure) -> None:
        """Print a ballot measure analysis."""
        self.console.print(
            Panel(
                f"[bold]{measure.identifier}: {measure.title}[/bold]",
                border_style="magenta",
            )
        )
        self.console.print(f"  {measure.summary}")
        self.console.print()

        # Pros and cons side by side
        grid = Table.grid(padding=(0, 2))
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)

        pros_text = Text()
        pros_text.append("Arguments For:\n", style="bold green")
        for p in measure.pros:
            pros_text.append(f"  + {p}\n")

        cons_text = Text()
        cons_text.append("Arguments Against:\n", style="bold red")
        for c in measure.cons:
            cons_text.append(f"  - {c}\n")

        grid.add_row(pros_text, cons_text)
        self.console.print(grid)

        if measure.fiscal_impact:
            fi = measure.fiscal_impact
            self.console.print(Panel(
                f"[bold]Cost:[/bold] {fi.estimated_cost}\n"
                f"[bold]Revenue Effect:[/bold] {fi.revenue_effect}\n"
                f"[bold]Funding Source:[/bold] {fi.funding_source}\n\n"
                f"{fi.summary}",
                title="Fiscal Impact",
                border_style="yellow",
            ))

        if measure.supporters or measure.opponents:
            self.console.print()
            if measure.supporters:
                self.console.print(f"  [bold]Supporters:[/bold] {', '.join(measure.supporters)}")
            if measure.opponents:
                self.console.print(f"  [bold]Opponents:[/bold] {', '.join(measure.opponents)}")

        self.console.print()

    def print_comparison(self, comparison: CandidateComparison) -> None:
        """Print a side-by-side candidate comparison table."""
        table = Table(
            title=f"Candidate Comparison: {comparison.office}",
            show_lines=True,
        )
        table.add_column("Issue", style="bold", width=20)
        for name in comparison.candidates:
            table.add_column(name, ratio=1)

        for row in comparison.comparison_rows:
            issue = row.get("issue", "")
            cells = [issue.replace("_", " ").title()]
            for name in comparison.candidates:
                cells.append(row.get(name, "N/A"))
            table.add_row(*cells)

        self.console.print(table)
        self.console.print()

    def print_full_guide(self, guide: VoterGuide) -> None:
        """Print a complete voter guide."""
        self.console.print()
        self.console.print(
            Panel(
                f"[bold]{guide.election_name}[/bold]\n"
                f"Date: {guide.election_date}\n"
                f"Jurisdiction: {guide.jurisdiction}",
                title="Voter Guide",
                border_style="blue",
            )
        )
        self.print_disclaimer()

        if guide.candidates:
            self.console.rule("[bold]Candidates[/bold]")
            for candidate in guide.candidates:
                self.print_candidate(candidate)

        if guide.measures:
            self.console.rule("[bold]Ballot Measures[/bold]")
            for measure in guide.measures:
                self.print_measure(measure)

        if guide.comparisons:
            self.console.rule("[bold]Candidate Comparisons[/bold]")
            for comp in guide.comparisons:
                self.print_comparison(comp)

        self.console.print(
            Panel(guide.disclaimer, title="Disclaimer", border_style="dim")
        )
