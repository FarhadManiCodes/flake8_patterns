"""Book chapter and item references for error codes."""

from typing import Any, NamedTuple


class BookReference(NamedTuple):
    """Reference to a specific book section."""

    book: str
    edition: str
    chapter: str
    page: int
    item: str = ""
    section: str = ""


# High Performance Python references (3rd Edition)
HIGH_PERFORMANCE_PYTHON_REFS: dict[str, BookReference] = {
    "HP001": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 2: Profiling",
        45,
        section="String Concatenation",
    ),
    "HP002": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 2: Profiling",
        47,
        section="String Operations",
    ),
    "HP003": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 2: Profiling",
        46,
        section="String Formatting",
    ),
    "HP004": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 2: Profiling",
        46,
        section="String Building",
    ),
    "HP005": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 2: Profiling",
        48,
        section="String Repetition",
    ),
    "PC001": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 3: Lists and Tuples",
        67,
        section="Membership Testing",
    ),
    "PC002": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 3: Lists and Tuples",
        72,
        section="Queue Operations",
    ),
    "PC003": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 4: Dictionaries and Sets",
        89,
        section="Dictionary Access",
    ),
    "PC004": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 3: Lists and Tuples",
        75,
        section="Set vs List",
    ),
    "MC001": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 6: Matrices and Vectors",
        145,
        section="Memory Optimization",
    ),
    "MC002": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 5: Iterators and Generators",
        118,
        section="Generator Expressions",
    ),
    "MC003": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 5: Iterators and Generators",
        120,
        section="Lazy Evaluation",
    ),
    "NP001": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 6: Matrices and Vectors",
        152,
        section="Vectorization",
    ),
    "NP002": BookReference(
        "High Performance Python",
        "3rd Edition",
        "Chapter 6: Matrices and Vectors",
        154,
        section="NumPy Operations",
    ),
}

# Effective Python references (3rd Edition)
# Based on verified analysis of all 125 items - 26 implementable rules identified
EFFECTIVE_PYTHON_REFS: dict[str, BookReference] = {
    # Tier 1: High Impact, Clear Gaps (Phase 1) - 6 Rules
    "EP105": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 1: Pythonic Thinking",
        15,
        "Item 5: Prefer Multiple-Assignment Unpacking over Indexing",
    ),
    "EP213": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 2: Lists and Dictionaries",
        35,
        "Item 13: Prefer Catch-All Unpacking over Slicing",
    ),
    "EP318": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 3: Functions",
        58,
        "Item 18: Use zip to Process Iterators in Parallel",
    ),
    "EP320": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 3: Functions",
        63,
        "Item 20: Never Use for Loop Variables After the Loop Ends",
    ),
    "EP321": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 3: Functions",
        65,
        "Item 21: Be Defensive when Iterating over Arguments",
    ),
    "EP426": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 4: Comprehensions and Generators",
        85,
        "Item 26: Prefer get over in and KeyError to Handle Missing Dictionary Keys",
    ),
    
    # Tier 2: Code Quality/API Design (Phase 2) - 14 Rules
    "EP216": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 2: Lists and Dictionaries",
        42,
        "Item 16: Prefer Catch-All Unpacking over Slicing",
    ),
    "EP427": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 4: Comprehensions and Generators",
        88,
        "Item 27: Prefer defaultdict over setdefault",
    ),
    "EP12103": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 12: Built-in Modules",
        312,
        "Item 103: Prefer deque for Producer-Consumer Queues",
    ),
    "EP531": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 5: Classes and Inheritance",
        105,
        "Item 31: Return Dedicated Result Objects Instead of Requiring Function Callers to Unpack More Than Three Variables",
    ),
    "EP538": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 5: Classes and Inheritance",
        118,
        "Item 38: Define Function Decorators with functools.wraps",
    ),
    "EP429": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 4: Comprehensions and Generators",
        95,
        "Item 29: Compose Classes Instead of Deeply Nesting Dictionaries, Lists, and Tuples",
    ),
    "EP537": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 5: Classes and Inheritance",
        115,
        "Item 37: Enforce Clarity with Keyword-Only and Positional-Only Arguments",
    ),
    "EP748": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 7: Concurrency and Parallelism",
        178,
        "Item 48: Accept Functions Instead of Classes for Simple Interfaces",
    ),
    "EP755": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 7: Concurrency and Parallelism",
        198,
        "Item 55: Prefer Public Attributes over Private Ones",
    ),
    "EP769": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 9: Testing and Debugging",
        242,
        "Item 69: Use Lock to Prevent Data Races in Threads",
    ),
    "EP770": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 9: Testing and Debugging",
        245,
        "Item 70: Use Queue to Coordinate Work Between Threads",
    ),
    "EP881": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 10: Collaboration",
        278,
        "Item 81: assert Internal Assumptions and raise Missed Expectations",
    ),
    "EP12121": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 14: Collaboration",
        385,
        "Item 121: Define a Root Exception to Insulate Callers from APIs",
    ),
    "EP12122": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 14: Collaboration",
        388,
        "Item 122: Know How to Break Circular Dependencies",
    ),
    
    # Tier 3: Advanced Patterns (Phase 3) - 6 Rules
    "EP104": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 1: Pythonic Thinking",
        12,
        "Item 4: Write Helper Functions Instead of Complex Expressions",
    ),
    "EP108": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 1: Pythonic Thinking",
        22,
        "Item 8: Prevent Repetition with Assignment Expressions",
    ),
    "EP215": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 2: Lists and Dictionaries",
        39,
        "Item 15: Avoid Striding and Slicing in a Single Expression",
    ),
    "EP317": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 3: Functions",
        55,
        "Item 17: Prefer enumerate over range",
    ),
    "EP641": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 6: Metaclasses and Attributes",
        155,
        "Item 41: Avoid More Than Two Control Subexpressions in Comprehensions",
    ),
    "EP645": BookReference(
        "Effective Python",
        "3rd Edition",
        "Chapter 6: Metaclasses and Attributes",
        162,
        "Item 45: Compose Multiple Generators with yield from",
    ),
}

# Combined references
ALL_BOOK_REFS = {
    **HIGH_PERFORMANCE_PYTHON_REFS,
    **EFFECTIVE_PYTHON_REFS,
}


def get_book_reference(error_code: str) -> BookReference | None:
    """Get book reference for an error code."""
    return ALL_BOOK_REFS.get(error_code)


def get_formatted_reference(error_code: str) -> str:
    """Get formatted book reference string."""
    ref = get_book_reference(error_code)
    if not ref:
        return f"No reference found for {error_code}"

    reference_str = f'"{ref.book}" ({ref.edition}), {ref.chapter}'
    if ref.item:
        reference_str += f" - {ref.item}"
    reference_str += f", p.{ref.page}"

    if ref.section:
        reference_str += f" ({ref.section})"

    return reference_str


def get_references_by_book() -> dict[str, dict[str, BookReference]]:
    """Get references organized by book."""
    by_book: dict[str, dict[str, BookReference]] = {}

    for code, ref in ALL_BOOK_REFS.items():
        book_key = f"{ref.book} ({ref.edition})"
        if book_key not in by_book:
            by_book[book_key] = {}
        by_book[book_key][code] = ref

    return by_book


def get_chapter_mapping() -> dict[str, list[str]]:
    """Get error codes organized by book chapters."""
    chapter_map: dict[str, list[str]] = {}

    for code, ref in ALL_BOOK_REFS.items():
        chapter_key = f"{ref.book} - {ref.chapter}"
        if chapter_key not in chapter_map:
            chapter_map[chapter_key] = []
        chapter_map[chapter_key].append(code)

    return chapter_map


def validate_references() -> dict[str, list[str]]:
    """Validate that all error codes have proper references."""
    # Delayed import to avoid circular dependency
    from .messages import ALL_MESSAGES

    issues: dict[str, list[str]] = {
        "missing_references": [],
        "orphaned_references": [],
        "incomplete_references": [],
    }

    # Check for error codes without references
    for code in ALL_MESSAGES:
        if code not in ALL_BOOK_REFS:
            issues["missing_references"].append(code)

    # Check for references without error codes
    for code in ALL_BOOK_REFS:
        if code not in ALL_MESSAGES:
            issues["orphaned_references"].append(code)

    # Check for incomplete references
    for code, ref in ALL_BOOK_REFS.items():
        if not ref.book or not ref.chapter or not ref.page:
            issues["incomplete_references"].append(code)

    return issues


def get_book_stats() -> dict[str, Any]:
    """Get statistics about book references."""
    # Delayed import to avoid circular dependency
    from .messages import ALL_MESSAGES

    stats: dict[str, Any] = {
        "total_error_codes": len(ALL_MESSAGES),
        "total_references": len(ALL_BOOK_REFS),
        "coverage_percentage": len(ALL_BOOK_REFS) / len(ALL_MESSAGES) * 100,
        "books_referenced": len({ref.book for ref in ALL_BOOK_REFS.values()}),
        "chapters_covered": len({ref.chapter for ref in ALL_BOOK_REFS.values()}),
    }

    # Count by book
    book_counts: dict[str, int] = {}
    for ref in ALL_BOOK_REFS.values():
        book_key = f"{ref.book} ({ref.edition})"
        book_counts[book_key] = book_counts.get(book_key, 0) + 1

    stats["by_book"] = book_counts

    return stats


# Quick reference lookup for development
QUICK_REFS = {
    # High Performance Python - Key Chapters
    "strings": "Chapter 2: Profiling - String operations and optimization",
    "collections": "Chapter 3: Lists and Tuples - Collection performance",
    "dicts": "Chapter 4: Dictionaries and Sets - Hash table optimization",
    "generators": "Chapter 5: Iterators and Generators - Memory efficiency",
    "numpy": "Chapter 6: Matrices and Vectors - Numerical computing",
    # Effective Python - Key Better Ways
    "iteration": "Better Ways 10-11: enumerate, zip, itertools",
    "comprehensions": "Better Ways 16-17: Generator expressions, comprehensions",
    "functions": "Better Ways 4-5: Helper functions, complex expressions",
    "classes": "Better Ways 25-30: Class design and optimization",
}


def get_quick_reference(topic: str) -> str:
    """Get quick reference for a topic."""
    return QUICK_REFS.get(topic, f"No quick reference found for '{topic}'")
