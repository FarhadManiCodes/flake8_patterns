"""flake8_patterns: A flake8 plugin for performance patterns.

Based on patterns from "High Performance Python" (3rd Edition) and
"Effective Python" (3rd Edition).

This plugin detects performance anti-patterns and suggests better alternatives
with direct references to authoritative Python performance books.
"""

from typing import Any

from .book_refs import get_book_reference, get_book_stats, get_formatted_reference
from .checker import PatternChecker
from .messages import (
    ALL_MESSAGES,
    get_all_error_codes,
    get_error_codes_by_category,
    get_error_info,
    get_error_message,
)
from .utils import PYTHON_313_PLUS, PYTHON_VERSION

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Main exports
__all__ = [
    # Message system
    "ALL_MESSAGES",
    "PYTHON_313_PLUS",
    # Utilities
    "PYTHON_VERSION",
    # Main checker class
    "PatternChecker",
    "__author__",
    "__email__",
    # Metadata
    "__version__",
    "get_all_error_codes",
    # Book reference system
    "get_book_reference",
    "get_book_stats",
    "get_error_codes_by_category",
    "get_error_info",
    "get_error_message",
    "get_formatted_reference",
]


# Plugin information for flake8
def get_plugin_info() -> dict[str, str | int]:
    """Get plugin information."""
    return {
        "name": "flake8-patterns",
        "version": __version__,
        "author": __author__,
        "description": "Performance patterns from High Performance Python and "
        "Effective Python",
        "python_version": f"{PYTHON_VERSION.major}.{PYTHON_VERSION.minor}."
        f"{PYTHON_VERSION.micro}",
        "total_rules": len(ALL_MESSAGES),
        "rule_categories": len(get_error_codes_by_category()),
        "book_coverage": (
            f"{len(get_book_reference.__defaults__ or [])} books referenced"
        ),
    }


# Quick access to rule counts
RULE_COUNTS = {
    "string_operations": len([k for k in ALL_MESSAGES if k.startswith("HP")]),
    "collection_performance": len([k for k in ALL_MESSAGES if k.startswith("PC")]),
    "iteration_patterns": len([k for k in ALL_MESSAGES if k.startswith("EP")]),
    "memory_optimization": len([k for k in ALL_MESSAGES if k.startswith("MC")]),
    "numpy_patterns": len([k for k in ALL_MESSAGES if k.startswith("NP")]),
}


# Development utilities
def print_rule_summary() -> None:
    """Print a summary of all rules (useful for development)."""
    categories = get_error_codes_by_category()
    for codes in categories.values():
        if codes:
            for code in sorted(codes)[:3]:  # Show first 3
                info = get_error_info(code)
                if info:
                    pass
            if len(codes) > 3:
                pass


def print_book_coverage() -> None:
    """Print book reference coverage (useful for development)."""
    stats = get_book_stats()

    by_book = stats.get("by_book", {})
    if isinstance(by_book, dict):
        for _book, _count in by_book.items():
            pass


# Version compatibility info
if PYTHON_313_PLUS:
    _performance_note = "Running on Python 3.13+ with latest performance optimizations"
elif PYTHON_VERSION >= (3, 10):
    _performance_note = "Running on Python 3.10+ with modern features"
else:
    _performance_note = "Running on legacy Python version with basic compatibility"


def get_version_info() -> dict[str, Any]:
    """Get detailed version and compatibility information."""
    return {
        "plugin_version": __version__,
        "python_version": f"{PYTHON_VERSION.major}.{PYTHON_VERSION.minor}."
        f"{PYTHON_VERSION.micro}",
        "python_version_tuple": PYTHON_VERSION,
        "performance_tier": (
            "optimized"
            if PYTHON_313_PLUS
            else "standard" if PYTHON_VERSION >= (3, 10) else "legacy"
        ),
        "performance_note": _performance_note,
        "supported_features": {
            "pattern_matching": PYTHON_VERSION >= (3, 10),
            "exception_groups": PYTHON_VERSION >= (3, 11),
            "type_hints": True,
            "modern_ast": True,
        },
    }


# Backwards compatibility
PerformanceChecker = PatternChecker  # Alternative name for compatibility
