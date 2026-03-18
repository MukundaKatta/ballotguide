"""CLI for ballotguide."""
import sys, json, argparse
from .core import Ballotguide

def main():
    parser = argparse.ArgumentParser(description="BallotGuide — AI Voter Guide. Non-partisan candidate and ballot measure analysis for informed voting.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = Ballotguide()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.process(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"ballotguide v0.1.0 — BallotGuide — AI Voter Guide. Non-partisan candidate and ballot measure analysis for informed voting.")

if __name__ == "__main__":
    main()
