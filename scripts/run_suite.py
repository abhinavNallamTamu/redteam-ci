#!/usr/bin/env python3
"""
scripts/run_suite.py
────────────────────
Main entry point for the RedTeam-CI harness.

Usage:
    python scripts/run_suite.py --runner mock --policy policies/default.yaml
    python scripts/run_suite.py --runner ollama --model llama3 --policy policies/default.yaml
"""

import argparse
import sys
from pathlib import Path

# Ensure src/ is on the path when running as a script
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def parse_args():
    parser = argparse.ArgumentParser(
        description="RedTeam-CI: Prompt Guardrails & Red-Team Harness"
    )
    parser.add_argument(
        "--runner",
        choices=["mock", "ollama", "llamacpp"],
        default="mock",
        help="LLM backend to use (default: mock)",
    )
    parser.add_argument(
        "--model",
        default="llama3",
        help="Model name for Ollama/llama.cpp runners",
    )
    parser.add_argument(
        "--policy",
        default="policies/default.yaml",
        help="Path to policy YAML file",
    )
    parser.add_argument(
        "--output",
        default="reports/latest.html",
        help="Path for output HTML report",
    )
    parser.add_argument(
        "--category",
        default=None,
        help="Run only a specific test category (e.g. jailbreaks)",
    )
    parser.add_argument(
        "--compare-baseline",
        default=None,
        dest="baseline",
        help="Path to baseline JSON for regression detection",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"[redteam-ci] Runner: {args.runner}")
    print(f"[redteam-ci] Policy: {args.policy}")
    print(f"[redteam-ci] Output: {args.output}")
    print()
    print("⚠️  Core modules not yet implemented — coming in Step 2+")
    print("   This scaffold confirms the CLI entry point is wired up correctly.")


if __name__ == "__main__":
    main()
