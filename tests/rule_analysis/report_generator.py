"""
Simple report generation for rule redundancy analysis.

This module analyzes linter output to determine if existing linters
detect the same patterns our rules target.
"""

import json

# Known formatting/style violations that don't indicate pattern detection
FORMATTING_VIOLATIONS = {
    # File structure
    "INP001",  # Missing __init__.py
    "ANN201",  # Missing return type annotation
    "ANN001",  # Missing type annotation
    # Documentation
    "D100",
    "D101",
    "D102",
    "D103",
    "D104",
    "D105",
    "D106",
    "D107",
    # Style/formatting
    "W292",
    "W293",
    "C0304",
    "C0305",  # Newlines
    "E302",
    "E303",
    "E501",  # Spacing/length
    "COM812",
    "COM819",  # Commas
    "Q000",
    "Q001",
    "Q002",
    "Q003",  # Quotes
    "I001",
    "I002",  # Imports
    # Unused/naming
    "F401",
    "F811",
    "F841",  # Unused
    "C0103",
    "C0114",
    "C0115",
    "C0116",  # Naming/docs
    "W0611",
    "W0613",
    "W0622",  # Unused/redefining
    # Design (not patterns)  # noqa: ERA001
    "R0903",
    "R0913",
    "R0914",  # Too few/many
}

# Pattern detection rules that ARE relevant
PATTERN_RULES = {
    # flake8-bugbear patterns
    "B006",
    "B007",
    "B008",
    "B011",
    "B015",
    "B018",
    "B023",
    # Pylint patterns
    "R1701",
    "R1703",
    "R1705",
    "R1712",
    "R1713",
    "R1715",
    "R1726",
    "W0102",
    "W0104",
    "W0120",
    # Ruff patterns
    "PERF",
    "SIM",
    "UP",
    "PIE",
    "C4",
}


def is_pattern_violation(rule_code: str) -> bool:
    """Check if a rule code represents actual pattern detection."""
    # Direct formatting violation
    if rule_code in FORMATTING_VIOLATIONS:
        return False

    # Known pattern detection rule
    if rule_code in PATTERN_RULES:
        return True

    # Pattern rule prefixes
    if any(
        rule_code.startswith(prefix)
        for prefix in ["PERF", "SIM", "UP", "PIE", "C4", "B0"]
    ):
        return True

    # Pylint R-rules (refactoring suggestions)
    return rule_code.startswith("R1") and rule_code not in FORMATTING_VIOLATIONS


def parse_linter_violations(linter_name: str, stdout: str, _stderr: str) -> list[dict]:
    """Parse violations from linter output."""
    violations = []

    if not stdout.strip():
        return violations

    if linter_name in ["ruff", "pylint"]:
        try:
            # JSON format
            data = json.loads(stdout)

            if linter_name == "ruff":
                for item in data:
                    violations.append(
                        {
                            "rule_code": item.get("code", "UNKNOWN"),
                            "line": item.get("location", {}).get("row", 0),
                            "message": item.get("message", ""),
                        }
                    )

            elif linter_name == "pylint":
                for item in data:
                    violations.append(
                        {
                            "rule_code": item.get("message-id", "UNKNOWN"),
                            "line": item.get("line", 0),
                            "message": item.get("message", ""),
                        }
                    )
        except json.JSONDecodeError:
            pass  # No violations or unparseable output

    elif linter_name in ["flake8", "flake8-bugbear"]:
        # Try JSON first, fallback to text
        try:
            data = json.loads(stdout)
            for file_violations in data.values():
                for item in file_violations:
                    violations.append(
                        {
                            "rule_code": item.get("code", "UNKNOWN"),
                            "line": item.get("line_number", 0),
                            "message": item.get("text", ""),
                        }
                    )
        except json.JSONDecodeError:
            # Fallback to text parsing
            for line in stdout.strip().split("\n"):
                if ":" in line:
                    parts = line.split(":", 3)
                    if len(parts) >= 4:
                        try:
                            line_num = int(parts[1])
                            code_msg = parts[3].strip()
                            if " " in code_msg:
                                code, message = code_msg.split(" ", 1)
                                violations.append(
                                    {
                                        "rule_code": code,
                                        "line": line_num,
                                        "message": message,
                                    }
                                )
                        except (ValueError, IndexError):
                            continue

    return violations


def analyze_linter_output(rule_code: str, linter_results: dict[str, dict]) -> dict:
    """Analyze linter results for redundancy."""
    total_violations = 0
    pattern_violations = 0
    linters_with_patterns = set()
    pattern_rules_found = set()

    all_violations = {}

    for linter_name, result in linter_results.items():
        if "error" in result:
            all_violations[linter_name] = {"error": result["error"]}
            continue

        violations = parse_linter_violations(
            linter_name, result["stdout"], result["stderr"]
        )

        linter_pattern_violations = []

        for violation in violations:
            total_violations += 1

            if is_pattern_violation(violation["rule_code"]):
                pattern_violations += 1
                linters_with_patterns.add(linter_name)
                pattern_rules_found.add(violation["rule_code"])
                linter_pattern_violations.append(violation)

        all_violations[linter_name] = {
            "total_violations": len(violations),
            "pattern_violations": linter_pattern_violations,
            "all_violations": violations,
        }

    # Calculate redundancy
    redundancy_percentage = 0.0
    if total_violations > 0:
        redundancy_percentage = (pattern_violations / max(1, total_violations)) * 100

    # Determine recommendation
    if pattern_violations == 0:
        recommendation = (
            f"✅ NO REDUNDANCY - Proceed with {rule_code}. "
            "No existing linters detect the target patterns."
        )
    elif pattern_violations < 3:
        recommendation = (
            f"⚠️  LOW REDUNDANCY - Consider {rule_code}. "
            f"Only {pattern_violations} pattern violations found."
        )
    else:
        recommendation = (
            f"❌ POTENTIAL REDUNDANCY - Review {rule_code}. "
            f"{pattern_violations} pattern violations found."
        )

    return {
        "rule_code": rule_code,
        "total_violations": total_violations,
        "pattern_violations": pattern_violations,
        "redundancy_percentage": redundancy_percentage,
        "linters_with_patterns": sorted(linters_with_patterns),
        "pattern_rules_found": sorted(pattern_rules_found),
        "recommendation": recommendation,
        "detailed_results": all_violations,
    }


def generate_report(analysis: dict, detailed_results: dict | None = None) -> str:
    """Generate a formatted report."""
    lines = [
        "=" * 60,
        f"REDUNDANCY ANALYSIS: {analysis['rule_code']}",
        "=" * 60,
        "",
        "📊 SUMMARY",
        "-" * 20,
        f"Total violations found: {analysis['total_violations']}",
        f"Pattern-related violations: {analysis['pattern_violations']}",
        f"Redundancy indicator: {analysis['redundancy_percentage']:.1f}%",
        "",
        "💡 RECOMMENDATION",
        "-" * 20,
        analysis["recommendation"],
        "",
    ]

    if analysis["linters_with_patterns"]:
        lines.extend(
            [
                "🔍 LINTERS WITH PATTERN DETECTION",
                "-" * 35,
            ]
        )
        for linter in analysis["linters_with_patterns"]:
            lines.append(f"  • {linter}")
        lines.append("")

    if analysis["pattern_rules_found"]:
        lines.extend(
            [
                "📋 PATTERN RULES DETECTED",
                "-" * 25,
            ]
        )
        for rule in analysis["pattern_rules_found"]:
            lines.append(f"  • {rule}")
        lines.append("")

    if detailed_results:
        lines.extend(
            [
                "=" * 60,
                "DETAILED RESULTS",
                "=" * 60,
                "",
            ]
        )

        for linter, result in detailed_results.items():
            lines.append(f"📝 {linter.upper()}")
            lines.append("-" * 40)

            if "error" in result:
                lines.append(f"❌ Error: {result['error']}")
            else:
                linter_result = analysis["detailed_results"][linter]
                total = linter_result["total_violations"]
                patterns = len(linter_result["pattern_violations"])

                lines.append(f"Total violations: {total}")
                lines.append(f"Pattern violations: {patterns}")

                if linter_result["pattern_violations"]:
                    lines.append("Pattern violations found:")
                    for v in linter_result["pattern_violations"]:
                        lines.append(
                            f"  {v['rule_code']} (line {v['line']}): " f"{v['message']}"
                        )
                else:
                    lines.append("✅ No pattern violations")

            lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)
