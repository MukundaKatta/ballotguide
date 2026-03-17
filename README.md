# BallotGuide

AI Voter Guide - strictly non-partisan.

BallotGuide provides balanced, factual information about candidates and ballot measures to help voters make informed decisions. It does not endorse or oppose any candidate, party, or measure.

## Features

- **Candidate Database** - Positions, voting records, and endorsements for candidates
- **Ballot Measure Analyzer** - Balanced pros/cons and fiscal impact analysis
- **Candidate Comparator** - Side-by-side issue comparisons
- **Bias Detector** - Scans text for non-neutral or partisan language
- **Position Tracker** - Tracks candidate stances across 16 policy areas
- **Impact Estimator** - Projects potential policy effects with appropriate caveats
- **Rich Reports** - Formatted terminal output with tables and panels

## Policy Areas Covered

Economy, Healthcare, Education, Immigration, Climate, Criminal Justice, Housing, Taxation, Foreign Policy, Gun Policy, Infrastructure, Labor, Technology, Agriculture, Veterans, Civil Rights.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Display full sample voter guide
ballotguide guide

# List or search candidates
ballotguide candidates
ballotguide candidates Santos

# List or search ballot measures
ballotguide measures
ballotguide measures "Proposition 1"

# Compare candidates for an office
ballotguide compare "senate"

# Check text for biased language
ballotguide check-bias "This radical plan would destroy the economy."

# Show policy impact estimates for a candidate
ballotguide impact Santos

# Show policy area coverage for a candidate
ballotguide coverage Santos
```

## Project Structure

```
src/ballotguide/
    models.py          # Pydantic models (Candidate, BallotMeasure, PolicyPosition, VoterGuide)
    cli.py             # Click CLI commands
    report.py          # Rich report generation
    guide/
        candidates.py  # CandidateDatabase with sample data
        measures.py    # BallotMeasureAnalyzer with sample measures
        comparator.py  # CandidateComparator for side-by-side comparison
    analyzer/
        bias.py        # BiasDetector for neutral language enforcement
        positions.py   # PositionTracker across 16 policy areas
        impact.py      # ImpactEstimator for projecting policy effects
tests/
    test_models.py
    test_candidates.py
    test_measures.py
    test_comparator.py
    test_bias.py
    test_positions.py
    test_impact.py
    test_report.py
```

## Running Tests

```bash
pytest tests/ -v
```

## Non-Partisan Commitment

All content in BallotGuide is presented without editorial bias. The bias detector actively flags partisan labels, loaded language, and editorial commentary. Sample data uses fictional candidates without party affiliations to demonstrate balanced presentation.
