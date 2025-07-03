"""Error messages and codes for flake8_patterns."""

# Error message format: (message_template, book_reference, performance_impact)
ErrorInfo = tuple[str, str, str]

# String operation errors (HP001-HP020)
STRING_MESSAGES: dict[str, ErrorInfo] = {
    "HP001": (
        "String concatenation using += in loop, consider str.join()",
        "'High Performance Python' (3rd Edition), Chapter 2: Profiling, p.45",
        "O(n²) → O(n), ~10x faster for 100+ items",
    ),
    "HP002": (
        "Multiple string concatenations, consider str.join() or f-strings",
        "'High Performance Python' (3rd Edition), Chapter 2: Profiling, p.47",
        "~3x faster for multiple concatenations",
    ),
    "HP003": (
        "String formatting using % operator, consider f-strings",
        "'Effective Python' (3rd Edition), Item 4: Write Helper Functions, p.12",
        "~20% faster and more readable",
    ),
    "HP004": (
        "Repeated string concatenation outside loop, consider str.join()",
        "'High Performance Python' (3rd Edition), Chapter 2: Profiling, p.46",
        "~5x faster for 5+ concatenations",
    ),
    "HP005": (
        "String multiplication for repetition, consider str.join() with repeat",
        "'High Performance Python' (3rd Edition), Chapter 2: Profiling, p.48",
        "~2x faster for large repetitions",
    ),
}

# Collection performance errors (PC001-PC020)
COLLECTION_MESSAGES: dict[str, ErrorInfo] = {
    "PC001": (
        "List membership testing, consider using set for O(1) lookup",
        "'High Performance Python' (3rd Edition), Chapter 3: Lists and Tuples, p.67",
        "O(n) → O(1), ~100x faster for large collections",
    ),
    "PC002": (
        "List.pop(0) in loop, consider collections.deque.popleft()",
        "'High Performance Python' (3rd Edition), Chapter 3: Lists and Tuples, p.72",
        "O(n) → O(1), ~1000x faster for large lists",
    ),
    "PC003": (
        "Dictionary key access without default, consider dict.get()",
        "'High Performance Python' (3rd Edition), Chapter 4: Dictionaries, p.89",
        "Avoids KeyError exceptions, ~20% faster",
    ),
    "PC004": (
        "List comprehension where set comprehension appropriate",
        "'High Performance Python' (3rd Edition), Chapter 3: Lists and Tuples, p.75",
        "Better memory usage, faster membership testing",
    ),
    "PC005": (
        "Manual iteration over dict.keys(), use dict.items()",
        "'Effective Python' (3rd Edition), Item 14: Sort by Complex Criteria, p.34",
        "More efficient, avoids extra key lookups",
    ),
}

# Effective Python iteration patterns (EP001-EP020)
ITERATION_MESSAGES: dict[str, ErrorInfo] = {
    "EP001": (
        "Use enumerate() instead of range(len()) for cleaner iteration",
        "'Effective Python' (3rd Edition), Item 10: Prefer enumerate, p.23",
        "More readable, less error-prone, same performance",
    ),
    "EP002": (
        "Use zip() for parallel iteration instead of manual indexing",
        "'Effective Python' (3rd Edition), Item 11: Use zip to Process Iterators, p.25",
        "More readable, less error-prone, same performance",
    ),
    "EP003": (
        "Manual index tracking in loop, consider enumerate()",
        "'Effective Python' (3rd Edition), Item 10: Prefer enumerate, p.24",
        "Cleaner code, reduces off-by-one errors",
    ),
    "EP004": (
        "Nested loop for iteration, consider itertools.product()",
        "'Effective Python' (3rd Edition), Item 16: Consider Generator Expressions, p.38",
        "More memory efficient, cleaner code",
    ),
    "EP005": (
        "Manual list reversal in loop, use reversed()",
        "'Effective Python' (3rd Edition), Item 10: Prefer enumerate, p.24",
        "Built-in is optimized, more readable",
    ),
}

# Memory optimization patterns (MC001-MC020)
MEMORY_MESSAGES: dict[str, ErrorInfo] = {
    "MC001": (
        "Class without __slots__, consider adding for memory efficiency",
        "'High Performance Python' (3rd Edition), Chapter 6: Matrices and Vectors, p.145",
        "~40% less memory usage for data classes",
    ),
    "MC002": (
        "Large list comprehension, consider generator expression",
        "'High Performance Python' (3rd Edition), Chapter 5: Iterators and Generators, p.118",
        "Lazy evaluation, constant memory usage",
    ),
    "MC003": (
        "Creating large intermediate list, consider itertools",
        "'Effective Python' (3rd Edition), Item 17: Be Defensive When Iterating, p.40",
        "Memory efficient, lazy evaluation",
    ),
}

# NumPy performance patterns (NP001-NP020)
NUMPY_MESSAGES: dict[str, ErrorInfo] = {
    "NP001": (
        "Manual loop over array, consider vectorized operations",
        "'High Performance Python' (3rd Edition), Chapter 6: Matrices and Vectors, p.152",
        "~50-100x faster with NumPy vectorization",
    ),
    "NP002": (
        "List comprehension on array, use NumPy operations",
        "'High Performance Python' (3rd Edition), Chapter 6: Matrices and Vectors, p.154",
        "Vectorized operations are much faster",
    ),
}

# All messages combined
ALL_MESSAGES = {
    **STRING_MESSAGES,
    **COLLECTION_MESSAGES,
    **ITERATION_MESSAGES,
    **MEMORY_MESSAGES,
    **NUMPY_MESSAGES,
}


def get_error_message(code: str) -> str:
    """Get the full error message for a given error code."""
    if code not in ALL_MESSAGES:
        return f"Unknown error code: {code}"

    message, book_ref, performance = ALL_MESSAGES[code]
    return f"{message} → {book_ref} → Performance: {performance}"


def get_error_info(code: str) -> ErrorInfo | None:
    """Get the error info tuple for a given error code."""
    return ALL_MESSAGES.get(code)


def get_all_error_codes() -> list[str]:
    """Get all available error codes."""
    return sorted(ALL_MESSAGES.keys())


def get_error_codes_by_category() -> dict[str, list[str]]:
    """Get error codes organized by category."""
    return {
        "String Operations (HP001-HP020)": [
            k for k in ALL_MESSAGES if k.startswith("HP")
        ],
        "Collection Performance (PC001-PC020)": [
            k for k in ALL_MESSAGES if k.startswith("PC")
        ],
        "Iteration Patterns (EP001-EP020)": [
            k for k in ALL_MESSAGES if k.startswith("EP")
        ],
        "Memory Optimization (MC001-MC020)": [
            k for k in ALL_MESSAGES if k.startswith("MC")
        ],
        "NumPy Performance (NP001-NP020)": [
            k for k in ALL_MESSAGES if k.startswith("NP")
        ],
    }
