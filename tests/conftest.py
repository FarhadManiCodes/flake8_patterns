"""Pytest configuration and fixtures for flake8_patterns tests."""

import ast

import pytest

from flake8_patterns.checker import PerformanceChecker


@pytest.fixture()
def checker():
    """Create a PerformanceChecker instance."""

    def _checker(code: str):
        tree = ast.parse(code)
        return PerformanceChecker(tree, filename="test.py")

    return _checker


@pytest.fixture()
def run_checker():
    """Run checker on code and return errors."""

    def _run_checker(code: str) -> list[tuple[int, int, str]]:
        tree = ast.parse(code)
        checker = PerformanceChecker(tree, filename="test.py")
        return list(checker.run())

    return _run_checker


# Sample code snippets for testing
SAMPLE_STRING_CONCAT = """
result = ""
for item in items:
    result += str(item)  # Should trigger HP001
"""

SAMPLE_GOOD_STRING_JOIN = """
result = "".join(str(item) for item in items)  # Should not trigger
"""

SAMPLE_RANGE_LEN = """
items = ["a", "b", "c"]
for i in range(len(items)):  # Should trigger EP001
    print(i, items[i])
"""


@pytest.fixture()
def sample_codes():
    """Provide sample code snippets for testing."""
    return {
        "string_concat": SAMPLE_STRING_CONCAT,
        "good_string_join": SAMPLE_GOOD_STRING_JOIN,
        "range_len": SAMPLE_RANGE_LEN,
    }
