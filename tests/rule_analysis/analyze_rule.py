#!/usr/bin/env python3
"""
Simple rule redundancy analysis.

This script runs existing linters on rule analysis files to check if they
detect the same patterns our rules target.

Usage:
    python analyze_rule.py efp105
    python analyze_rule.py efp105 --linters ruff,pylint
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

# Handle imports gracefully
try:
    from .report_generator import analyze_linter_output, generate_report
except (ImportError, ValueError):
    sys.path.insert(0, str(Path(__file__).parent))
    from report_generator import analyze_linter_output, generate_report


def run_linter(linter_name: str, file_path: Path) -> dict:
    """Run a single linter on a file and return parsed results."""

    commands = {
        "ruff": ["ruff", "check", "--output-format=json", str(file_path)],
        "pylint": ["pylint", "--output-format=json", "--reports=n", str(file_path)],
        "flake8-bugbear": ["flake8", "--select=B", "--format=json", str(file_path)],
        "flake8": ["flake8", "--format=json", str(file_path)],
    }

    if linter_name not in commands:
        return {"error": f"Unknown linter: {linter_name}"}

    try:
        result = subprocess.run(
            commands[linter_name],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,  # Don't raise on lint violations
        )

        return {
            "linter": linter_name,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {"error": f"{linter_name} timed out"}
    except FileNotFoundError:
        return {"error": f"{linter_name} not found - please install it"}
    except Exception as e:
        return {"error": f"{linter_name} failed: {e}"}


def run_all_linters(file_path: Path, linters: list[str]) -> dict[str, dict]:
    """Run multiple linters on a file."""
    results = {}

    for linter in linters:
        print(f"Running {linter}...", end=" ", flush=True)
        result = run_linter(linter, file_path)
        results[linter] = result

        if "error" in result:
            print(f"❌ {result['error']}")
        else:
            print("✓")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Analyze rule redundancy with existing linters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_rule.py efp105
  python analyze_rule.py efp105 --linters ruff,pylint
  python analyze_rule.py efp105 --output json
        """.strip(),
    )

    parser.add_argument("rule_code", help="Rule code (e.g., efp105)")
    parser.add_argument(
        "--linters",
        default="ruff,pylint,flake8-bugbear,flake8",
        help="Comma-separated linters (default: all)",
    )
    parser.add_argument(
        "--output", choices=["console", "json"], default="console", help="Output format"
    )
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()

    # Find the analysis file
    analysis_file = Path(__file__).parent / f"{args.rule_code.lower()}_analysis.py"
    if not analysis_file.exists():
        print(f"Error: Analysis file not found: {analysis_file}")
        available = list(Path(__file__).parent.glob("*_analysis.py"))
        if available:
            rules = [f.stem.replace("_analysis", "") for f in available]
            print(f"Available rules: {', '.join(rules)}")
        return 1

    # Parse linters
    linters = [linter.strip() for linter in args.linters.split(",") if linter.strip()]

    if args.verbose:
        print(f"Analyzing {args.rule_code.upper()} redundancy...")
        print(f"File: {analysis_file}")
        print(f"Linters: {', '.join(linters)}")
        print()

    # Run linters
    linter_results = run_all_linters(analysis_file, linters)

    print()

    # Analyze results
    analysis = analyze_linter_output(args.rule_code.upper(), linter_results)

    # Generate output
    if args.output == "json":
        print(json.dumps(analysis, indent=2))
    else:
        detailed = linter_results if args.verbose else None
        report = generate_report(analysis, detailed)
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
