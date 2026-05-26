#!/usr/bin/env python3
"""
scripts/export_baseline.py
──────────────────────────
Snapshot the most recent run as a new baseline for regression detection.

Usage:
    python scripts/export_baseline.py --tag v0.1.0
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def parse_args():
    parser = argparse.ArgumentParser(description="Export current run as baseline")
    parser.add_argument("--tag", default="manual", help="Label for this baseline")
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"[export-baseline] Tag: {args.tag}")
    print("⚠️  Storage module not yet implemented — coming in Step 4")


if __name__ == "__main__":
    main()
