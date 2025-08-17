"""
Rule redundancy testing framework.

This module provides the core infrastructure for testing whether
flake8-patterns
rules are redundant with existing linters (ruff, pylint, flake8-bugbear, and
flake8).
"""

from dataclasses import dataclass
from enum import Enum


class LinterName(Enum):
    """Supported linters for redundancy testing."""

    RUFF = "ruff"
    PYLINT = "pylint"
    FLAKE8_BUGBEAR = "flake8-bugbear"
    FLAKE8 = "flake8"


@dataclass
class CodeSample:
    """Represents a code sample for testing against linters."""

    name: str  # Descriptive name for the sample
    code: str  # Python code to test
    should_trigger: bool  # Whether our rule should trigger on this code
    description: str  # What pattern this sample tests
    category: str  # e.g., "positive", "negative", "edge_case"


@dataclass
class LinterViolation:
    """Represents a violation found by a linter."""

    linter: str  # Name of the linter that found this violation
    rule_code: str  # Rule code (e.g., "R1707", "B007")
    line: int  # Line number where violation occurs
    column: int  # Column number where violation occurs
    message: str  # Violation message
    severity: str  # Severity level (error, warning, info)


@dataclass
class LinterResults:
    """Results from running linters against a code sample."""

    sample_name: str  # Name of the tested sample
    violations_by_linter: dict[str, list[LinterViolation]]  # Linter name -> violations
    execution_errors: dict[str, str]  # Linter name -> error message


@dataclass
class RedundancyAnalysis:
    """Analysis of redundancy between our rule and existing linters."""

    rule_code: str  # Our rule code (e.g., "EFP105")
    total_samples: int  # Total number of samples tested
    samples_with_existing_coverage: list[
        str
    ]  # Samples where existing linters found issues
    samples_with_no_coverage: list[str]  # Samples where no existing linter found issues
    overlapping_rules: dict[
        str, list[str]
    ]  # Linter name -> list of overlapping rule codes
    coverage_percentage: float  # Percentage covered by existing linters
    recommendation: str  # Implementation recommendation


class TestCategory:
    """Constants for test sample categories."""

    POSITIVE = "positive"  # Should trigger our rule
    NEGATIVE = "negative"  # Should NOT trigger our rule
    EDGE_CASE = "edge_case"  # Edge cases and boundary conditions


class Severity:
    """Constants for violation severity levels."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


def create_code_sample(
    name: str,
    code: str,
    should_trigger: bool,
    description: str,
    category: str = TestCategory.POSITIVE,
) -> CodeSample:
    """Helper function to create a CodeSample with validation."""
    if category not in [
        TestCategory.POSITIVE,
        TestCategory.NEGATIVE,
        TestCategory.EDGE_CASE,
    ]:
        msg = f"Invalid category: {category}"
        raise ValueError(msg)

    return CodeSample(
        name=name,
        code=code.strip() + "\n",  # Ensure proper newline ending
        should_trigger=should_trigger,
        description=description,
        category=category,
    )


def create_linter_violation(
    linter: str,
    rule_code: str,
    line: int,
    column: int,
    message: str,
    severity: str = Severity.WARNING,
) -> LinterViolation:
    """Helper function to create a LinterViolation with validation."""
    if severity not in [Severity.ERROR, Severity.WARNING, Severity.INFO]:
        msg = f"Invalid severity: {severity}"
        raise ValueError(msg)

    return LinterViolation(
        linter=linter,
        rule_code=rule_code,
        line=line,
        column=column,
        message=message,
        severity=severity,
    )


__all__ = [
    "CodeSample",
    "LinterName",
    "LinterResults",
    "LinterViolation",
    "RedundancyAnalysis",
    "Severity",
    "TestCategory",
    "create_code_sample",
    "create_linter_violation",
]
