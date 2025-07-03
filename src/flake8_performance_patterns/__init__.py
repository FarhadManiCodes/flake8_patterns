"""
flake8-performance-patterns: A flake8 plugin for performance patterns.

Based on patterns from "High Performance Python" (3rd Edition) and "Effective Python" (3rd Edition).

This plugin detects performance anti-patterns and suggests better alternatives
with direct references to authoritative Python performance books.
"""

from .checker import PerformanceChecker
from .messages import (
    ALL_MESSAGES,
    get_error_message,
    get_error_info,
    get_all_error_codes,
    get_error_codes_by_category,
)
from .book_refs import (
    get_book_reference,
    get_formatted_reference,
    get_book_stats,
)
from .utils import PYTHON_VERSION, PYTHON_313_PLUS

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Main exports
__all__ = [
    # Main checker class
    "PerformanceChecker",
    # Message system
    "ALL_MESSAGES",
    "get_error_message",
    "get_error_info",
    "get_all_error_codes",
    "get_error_codes_by_category",
    # Book reference system
    "get_book_reference",
    "get_formatted_reference",
    "get_book_stats",
    # Utilities
    "PYTHON_VERSION",
    "PYTHON_313_PLUS",
    # Metadata
    "__version__",
    "__author__",
    "__email__",
]


# Plugin information for flake8
def get_plugin_info() -> dict:
    """Get plugin information."""
    return {
        "name": "flake8-performance-patterns",
        "version": __version__,
        "author": __author__,
        "description": "Performance patterns from High Performance Python and Effective Python",
        "python_version": f"{PYTHON_VERSION.major}.{PYTHON_VERSION.minor}.{PYTHON_VERSION.micro}",
        "total_rules": len(ALL_MESSAGES),
        "rule_categories": len(get_error_codes_by_category()),
        "book_coverage": f"{len(get_book_reference.__defaults__ or [])} books referenced",
    }


# Quick access to rule counts
RULE_COUNTS = {
    "string_operations": len([k for k in ALL_MESSAGES.keys() if k.startswith("HP")]),
    "collection_performance": len(
        [k for k in ALL_MESSAGES.keys() if k.startswith("PC")]
    ),
    "iteration_patterns": len([k for k in ALL_MESSAGES.keys() if k.startswith("EP")]),
    "memory_optimization": len([k for k in ALL_MESSAGES.keys() if k.startswith("MC")]),
    "numpy_patterns": len([k for k in ALL_MESSAGES.keys() if k.startswith("NP")]),
}


# Development utilities
def print_rule_summary() -> None:
    """Print a summary of all rules (useful for development)."""
    print(f"flake8-performance-patterns v{__version__}")
    print(
        f"Python {PYTHON_VERSION.major}.{PYTHON_VERSION.minor}.{PYTHON_VERSION.micro}"
    )
    print(f"Total rules: {len(ALL_MESSAGES)}")
    print("")

    categories = get_error_codes_by_category()
    for category, codes in categories.items():
        if codes:
            print(f"{category}: {len(codes)} rules")
            for code in sorted(codes)[:3]:  # Show first 3
                info = get_error_info(code)
                if info:
                    print(f"  {code}: {info[0][:60]}...")
            if len(codes) > 3:
                print(f"  ... and {len(codes) - 3} more")
            print("")


def print_book_coverage() -> None:
    """Print book reference coverage (useful for development)."""
    stats = get_book_stats()
    print(f"Book Reference Coverage: {stats['coverage_percentage']:.1f}%")
    print(f"Books referenced: {stats['books_referenced']}")
    print(f"Chapters covered: {stats['chapters_covered']}")
    print("")

    for book, count in stats.get("by_book", {}).items():
        print(f"{book}: {count} rules")


# Version compatibility info
if PYTHON_313_PLUS:
    _performance_note = "Running on Python 3.13+ with latest performance optimizations"
elif PYTHON_VERSION >= (3, 10):
    _performance_note = "Running on Python 3.10+ with modern features"
else:
    _performance_note = "Running on legacy Python version with basic compatibility"


def get_version_info() -> dict:
    """Get detailed version and compatibility information."""
    return {
        "plugin_version": __version__,
        "python_version": f"{PYTHON_VERSION.major}.{PYTHON_VERSION.minor}.{PYTHON_VERSION.micro}",
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
PerformancePatternChecker = PerformanceChecker  # Alternative name for compatibility
