"""Error messages and codes for flake8_patterns."""

# Error message format: (message_template, book_reference, performance_impact)
ErrorInfo = tuple[str, str, str]

# TIER 1: High Impact, Clear Gaps (Phase 1 - v0.1.0-0.3.0)
TIER1_MESSAGES: dict[str, ErrorInfo] = {
    "EFP105": (
        "Sequential indexing pattern, prefer multiple-assignment unpacking",
        "'Effective Python' (3rd Edition), Item 5: "
        "Prefer Multiple-Assignment Unpacking over Indexing",
        "More readable, less error-prone, prevents index errors",
    ),
    "EFP213": (
        "Implicit string concatenation in collection, add explicit concatenation",
        "'Effective Python' (3rd Edition), Item 13: "
        "Prefer Explicit String Concatenation",
        "Prevents silent bugs from missing commas in lists",
    ),
    "EFP318": (
        "Manual parallel iteration, use zip() for cleaner code",
        "'Effective Python' (3rd Edition), Item 18: "
        "Use zip to Process Iterators in Parallel",
        "More readable, less error-prone, same performance",
    ),
    "EFP320": (
        "Loop variable used after loop completion, creates potential bugs",
        "'Effective Python' (3rd Edition), Item 20: "
        "Never Use for Loop Variables After the Loop Ends",
        "Prevents undefined behavior and runtime errors",
    ),
    "EFP321": (
        "Function iterates over same argument multiple times, "
        "check for iterator exhaustion",
        "'Effective Python' (3rd Edition), Item 21: "
        "Be Defensive when Iterating over Arguments",
        "Prevents silent bugs with generator arguments",
    ),
    "EFP426": (
        "Dictionary key access without default, "
        "consider dict.get() or try/except pattern",
        "'Effective Python' (3rd Edition), Item 26: Prefer get over in and KeyError",
        "Cleaner error handling, ~20% faster than try/except",
    ),
}

# TIER 2: Code Quality/API Design (Phase 2 - v0.4.0-0.6.0)
TIER2_MESSAGES: dict[str, ErrorInfo] = {
    "EFP216": (
        "Slice assignment pattern, prefer catch-all unpacking",
        "'Effective Python' (3rd Edition), Item 16: "
        "Prefer Catch-All Unpacking over Slicing",
        "More readable, handles variable-length sequences better",
    ),
    "EFP427": (
        "Multiple setdefault() calls, consider collections.defaultdict",
        "'Effective Python' (3rd Edition), Item 27: "
        "Prefer defaultdict over setdefault",
        "Cleaner code, better performance for multiple operations",
    ),
    "EFP12103": (
        "list.pop(0) in loop, use collections.deque.popleft() for queue operations",
        "'Effective Python' (3rd Edition), Item 103: "
        "Prefer deque for Producer-Consumer Queues",
        "O(n) → O(1), ~1000x faster for large queues",
    ),
    "EFP531": (
        "Function returns more than 3 values as tuple, "
        "consider dedicated result object",
        "'Effective Python' (3rd Edition), Item 31: " "Return Dedicated Result Objects",
        "Better API design, clearer variable unpacking",
    ),
    "EFP538": (
        "Decorator function missing functools.wraps, "
        "preserves original function metadata",
        "'Effective Python' (3rd Edition), Item 38: "
        "Define Function Decorators with functools.wraps",
        "Preserves function metadata, better debugging experience",
    ),
    "EFP429": (
        "Deeply nested dictionary/list/tuple structure, " "consider composing classes",
        "'Effective Python' (3rd Edition), Item 29: "
        "Compose Classes Instead of Deeply Nesting",
        "Better maintainability, clearer data access patterns",
    ),
    "EFP537": (
        "Function arguments could benefit from keyword-only or positional-only",
        "'Effective Python' (3rd Edition), Item 37: "
        "Enforce Clarity with Keyword-Only Arguments",
        "Clearer API, prevents argument coupling issues",
    ),
    "EFP748": (
        "Simple class interface, consider using function instead",
        "'Effective Python' (3rd Edition), Item 48: "
        "Accept Functions Instead of Classes",
        "Simpler API, better performance for simple interfaces",
    ),
    "EFP755": (
        "Overuse of private attributes, consider protected or public",
        "'Effective Python' (3rd Edition), Item 55: "
        "Prefer Public Attributes over Private Ones",
        "Better API design, reduces inheritance brittleness",
    ),
    "EFP769": (
        "Shared state access without proper locking in threaded code",
        "'Effective Python' (3rd Edition), Item 69: " "Use Lock to Prevent Data Races",
        "Prevents race conditions and data corruption",
    ),
    "EFP770": (
        "Manual queue implementation, use queue.Queue for thread coordination",
        "'Effective Python' (3rd Edition), Item 70: "
        "Use Queue to Coordinate Work Between Threads",
        "Thread-safe operations, prevents deadlocks",
    ),
    "EFP881": (
        "Incorrect assert/raise usage, assert for internal assumptions, "
        "raise for API validation",
        "'Effective Python' (3rd Edition), Item 81: "
        "assert Internal Assumptions and raise Missed Expectations",
        "Proper error handling, better debugging experience",
    ),
    "EFP12121": (
        "Module raises built-in exceptions, define root exception hierarchy",
        "'Effective Python' (3rd Edition), Item 121: "
        "Define a Root Exception to Insulate Callers",
        "Better API design, easier exception handling for callers",
    ),
    "EFP12122": (
        "Circular import dependency detected, consider refactoring",
        "'Effective Python' (3rd Edition), Item 122: "
        "Know How to Break Circular Dependencies",
        "Better architecture, prevents import errors",
    ),
}

# TIER 3: Nice to Have (Phase 3 - v0.7.0+)
TIER3_MESSAGES: dict[str, ErrorInfo] = {
    "EFP104": (
        "Complex expression, consider extracting helper function",
        "'Effective Python' (3rd Edition), Item 4: "
        "Write Helper Functions Instead of Complex Expressions",
        "Better readability, easier testing and debugging",
    ),
    "EFP108": (
        "Repeated expression, consider assignment expression (walrus operator)",
        "'Effective Python' (3rd Edition), Item 8: "
        "Prevent Repetition with Assignment Expressions",
        "Reduces repetition, Python 3.8+ feature",
    ),
    "EFP215": (
        "Striding and slicing in same expression, split for clarity",
        "'Effective Python' (3rd Edition), Item 15: "
        "Avoid Striding and Slicing in a Single Expression",
        "More readable, easier to understand intent",
    ),
    "EFP317": (
        "Manual counter increment, use enumerate() instead",
        "'Effective Python' (3rd Edition), Item 17: Prefer enumerate over range",
        "More readable, less error-prone, same performance",
    ),
    "EFP641": (
        "Comprehension with too many control subexpressions, " "consider regular loop",
        "'Effective Python' (3rd Edition), Item 41: "
        "Avoid More Than Two Control Subexpressions",
        "Better readability, easier debugging",
    ),
    "EFP645": (
        "Manual generator composition, use yield from",
        "'Effective Python' (3rd Edition), Item 45: "
        "Compose Multiple Generators with yield from",
        "More efficient, cleaner generator composition",
    ),
}

# All messages combined by priority tier
ALL_MESSAGES = {
    **TIER1_MESSAGES,
    **TIER2_MESSAGES,
    **TIER3_MESSAGES,
}


def get_error_message(code: str) -> str:
    """Get the full error message for a given error code."""
    if code not in ALL_MESSAGES:
        return f"Unknown error code: {code}"

    message, book_ref, performance = ALL_MESSAGES[code]
    return f"{message} → {book_ref} → Impact: {performance}"


def get_error_info(code: str) -> ErrorInfo | None:
    """Get the error info tuple for a given error code."""
    return ALL_MESSAGES.get(code)


def get_all_error_codes() -> list[str]:
    """Get all available error codes."""
    return sorted(ALL_MESSAGES.keys())


def get_error_codes_by_priority() -> dict[str, list[str]]:
    """Get error codes organized by implementation priority."""
    return {
        "Tier 1 - High Impact (Phase 1)": list(TIER1_MESSAGES.keys()),
        "Tier 2 - Code Quality (Phase 2)": list(TIER2_MESSAGES.keys()),
        "Tier 3 - Nice to Have (Phase 3)": list(TIER3_MESSAGES.keys()),
    }


def get_error_codes_by_category() -> dict[str, list[str]]:
    """Get error codes organized by traditional category."""
    return {
        "Effective Python Patterns": [k for k in ALL_MESSAGES if k.startswith("EFP")],
        "High Performance Python": [k for k in ALL_MESSAGES if k.startswith("HPP")],
        "Collection Performance": [k for k in ALL_MESSAGES if k.startswith("PC")],
        "Memory Optimization": [k for k in ALL_MESSAGES if k.startswith("MC")],
        "NumPy Performance": [k for k in ALL_MESSAGES if k.startswith("NP")],
    }


def get_tier_for_code(code: str) -> str:
    """Get the priority tier for a given error code."""
    if code in TIER1_MESSAGES:
        return "Tier 1 - High Impact"
    if code in TIER2_MESSAGES:
        return "Tier 2 - Code Quality"
    if code in TIER3_MESSAGES:
        return "Tier 3 - Nice to Have"
    return "Unknown"
