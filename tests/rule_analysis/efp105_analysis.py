"""
EFP105 Analysis: Sequential indexing patterns.

This module contains test samples for EFP105 rule validation.
EFP105 detects sequential indexing patterns that should be replaced with
multiple-assignment unpacking for better readability and performance.
"""

from __future__ import annotations

try:
    from . import CodeSample, TestCategory, create_code_sample
except ImportError:
    from __init__ import CodeSample, TestCategory, create_code_sample

# Rule metadata
RULE_CODE = "EFP105"
RULE_DESCRIPTION = (
    "Sequential indexing pattern detected. "
    "Prefer multiple-assignment unpacking over indexing."
)
BOOK_REFERENCE = (
    "Effective Python Item 5: "
    "Prefer Multiple Assignment Unpacking Over Indexing"
)

# Positive test cases - patterns that SHOULD trigger EFP105
POSITIVE_SAMPLES = [
    create_code_sample(
        name="basic_sequential_three_items",
        code='''"""Module demonstrating sequential indexing pattern."""

from __future__ import annotations


def process_data(items: list[str]) -> tuple[str, str, str]:
    """Process data using sequential indexing pattern."""
    first = items[0]
    second = items[1]
    third = items[2]
    return first, second, third

''',
        should_trigger=True,
        description="Basic sequential indexing of three consecutive items",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="basic_sequential_two_items",
        code='''"""Module demonstrating sequential indexing pattern."""

from __future__ import annotations


def get_pair(data: list[float]) -> tuple[float, float]:
    """Get pair of values using sequential indexing."""
    x = data[0]
    y = data[1]
    return x, y

''',
        should_trigger=True,
        description="Basic sequential indexing of two consecutive items",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="basic_sequential_four_items",
        code='''"""Module demonstrating sequential indexing pattern."""

from __future__ import annotations


def parse_rgba(values: list[int]) -> tuple[int, int, int, int]:
    """Parse RGBA values using sequential indexing."""
    r = values[0]
    g = values[1]
    b = values[2]
    a = values[3]
    return r, g, b, a

''',
        should_trigger=True,
        description="Basic sequential indexing of four consecutive items",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="multiline_with_processing",
        code='''"""Module demonstrating sequential indexing pattern."""

from __future__ import annotations


def calculate_stats(data: list[float]) -> float:
    """Calculate statistics using sequential indexing."""
    first = data[0]
    second = data[1]
    third = data[2]

    return (first + second + third) / 3

''',
        should_trigger=True,
        description="Sequential indexing with intermediate processing",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="assignment_to_instance_vars",
        code='''"""Module demonstrating sequential indexing pattern."""

from __future__ import annotations


class Point:
    """Point class using sequential indexing in constructor."""

    def __init__(self, coords: list[float]) -> None:
        """Initialize point with coordinates."""
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]

''',
        should_trigger=True,
        description="Sequential indexing in instance variable assignment",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="function_call_arguments",
        code='''"""Module demonstrating sequential indexing pattern."""

from __future__ import annotations


def process_user(data: list[str]) -> str:
    """Process user data using sequential indexing."""
    first_name = data[0]
    last_name = data[1]
    email = data[2]
    return create_user(first_name, last_name, email)


def create_user(first: str, last: str, email: str) -> str:
    """Create user string representation."""
    return f"{first} {last} <{email}>"

''',
        should_trigger=True,
        description="Sequential indexing used in function call arguments",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="string_formatting",
        code='''"""Module demonstrating sequential indexing pattern."""

from __future__ import annotations


def format_address(parts: list[str]) -> str:
    """Format address using sequential indexing."""
    street = parts[0]
    city = parts[1]
    state = parts[2]
    return f"{street}, {city}, {state}"

''',
        should_trigger=True,
        description="Sequential indexing in string formatting",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="arithmetic_expression",
        code='''"""Module demonstrating sequential indexing pattern."""

from __future__ import annotations


def calculate_area(vertices: list[float]) -> float:
    """Calculate area using sequential indexing."""
    x1 = vertices[0]
    y1 = vertices[1]
    x2 = vertices[2]
    y2 = vertices[3]
    return abs((x1 * y2) - (x2 * y1)) / 2

''',
        should_trigger=True,
        description="Sequential indexing in arithmetic expressions",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="mixed_sequential_with_gaps",
        code='''"""Module demonstrating mixed sequential pattern with gaps."""

from __future__ import annotations


def process_mixed(items: list[int]) -> tuple[int, int, int, int]:
    """Process data with mixed sequential and gap patterns."""
    first = items[0]   # Sequential part 1
    second = items[1]  # Sequential part 1 (should trigger)

    fourth = items[3]  # Gap here
    fifth = items[4]   # Sequential part 2 (should trigger)

    return first, second, fourth, fifth

''',
        should_trigger=True,
        description="Mixed sequential indexing with gaps - partial triggers",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="loop_sequential_indexing",
        code='''"""Module demonstrating sequential indexing in loop."""

from __future__ import annotations


def process_batches(batches: list[list[float]]) -> list[float]:
    """Process batches using sequential indexing in loop."""
    results = []
    for batch in batches:
        x = batch[0]   # Sequential pattern
        y = batch[1]   # in each iteration
        z = batch[2]   # (should trigger)
        results.append(x + y + z)
    return results

''',
        should_trigger=True,
        description="Sequential indexing pattern inside loop iteration",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="nested_same_object",
        code='''"""Module demonstrating sequential access to nested object."""

from __future__ import annotations


def extract_coordinates(
    matrix: list[list[float]]
) -> tuple[float, float, float]:
    """Extract coordinates from nested structure."""
    row = matrix[0]  # Get the row first
    x = row[0]       # Then sequential access
    y = row[1]       # to same row object
    z = row[2]       # (should trigger)
    return x, y, z

''',
        should_trigger=True,
        description="Sequential indexing of same nested object",
        category=TestCategory.POSITIVE,
    ),
    create_code_sample(
        name="intermediate_variable_indices",
        code='''"""Module demonstrating intermediate variable index access."""

from __future__ import annotations


def get_by_indices(
    data: list[str], indices: list[int]
) -> tuple[str, str, str]:
    """Get elements using intermediate variables from sequential indexing."""
    first_idx = indices[0]   # Sequential indexing pattern
    second_idx = indices[1]  # that should use unpacking:
    third_idx = indices[2]   # first_idx, second_idx, third_idx = indices

    a = data[first_idx]      # Subsequent usage doesn't change
    b = data[second_idx]     # the initial anti-pattern
    c = data[third_idx]
    return a, b, c

''',
        should_trigger=True,
        description="Sequential indexing for intermediate variables should trigger",
        category=TestCategory.POSITIVE,
    ),
]

# Negative test cases - patterns that should NOT trigger EFP105
NEGATIVE_SAMPLES = [
    create_code_sample(
        name="single_index_access",
        code='''"""Module demonstrating single index access."""

from __future__ import annotations


def get_first(items: list[str]) -> str:
    """Get first item from list."""
    return items[0]

''',
        should_trigger=False,
        description="Single index access should not trigger",
        category=TestCategory.NEGATIVE,
    ),
    create_code_sample(
        name="non_consecutive_indices",
        code='''"""Module demonstrating non-consecutive index access."""

from __future__ import annotations


def get_sparse(data: list[float]) -> tuple[float, float, float]:
    """Get sparse data elements."""
    first = data[0]
    fifth = data[4]
    tenth = data[9]
    return first, fifth, tenth

''',
        should_trigger=False,
        description="Non-consecutive indices should not trigger",
        category=TestCategory.NEGATIVE,
    ),
    create_code_sample(
        name="negative_indices",
        code='''"""Module demonstrating negative index access."""

from __future__ import annotations


def get_tail(data: list[str]) -> tuple[str, str, str]:
    """Get tail elements using negative indices."""
    last = data[-1]
    second_last = data[-2]
    third_last = data[-3]
    return last, second_last, third_last

''',
        should_trigger=False,
        description="Negative indices should not trigger",
        category=TestCategory.NEGATIVE,
    ),
    create_code_sample(
        name="repeated_same_index",
        code='''"""Module demonstrating repeated index access."""

from __future__ import annotations


def process_first(items: list[str]) -> tuple[str, str, str]:
    """Process first item in multiple ways."""
    raw = items[0]
    upper = items[0].upper()
    lower = items[0].lower()
    return raw, upper, lower

''',
        should_trigger=False,
        description="Repeated access to same index should not trigger",
        category=TestCategory.NEGATIVE,
    ),
    create_code_sample(
        name="different_variables",
        code='''"""Module demonstrating different variable index access."""

from __future__ import annotations


def process_lists(
    list_a: list[int],
    list_b: list[int],
    list_c: list[int],
) -> int:
    """Process multiple lists with different indices."""
    a = list_a[0]
    b = list_b[1]
    c = list_c[2]
    return a + b + c

''',
        should_trigger=False,
        description="Different variables being indexed should not trigger",
        category=TestCategory.NEGATIVE,
    ),
    create_code_sample(
        name="already_using_unpacking",
        code='''"""Module demonstrating proper unpacking."""

from __future__ import annotations


def process_coords(coords: tuple[float, float, float]) -> float:
    """Process coordinates using proper unpacking."""
    x, y, z = coords
    return x + y + z

''',
        should_trigger=False,
        description="Code already using unpacking should not trigger",
        category=TestCategory.NEGATIVE,
    ),
    create_code_sample(
        name="conditional_access",
        code='''"""Module demonstrating conditional index access."""

from __future__ import annotations


def get_conditional(data: list[int], *, use_condition: bool) -> list[int]:
    """Get elements based on condition."""
    result = []
    if use_condition:
        first = data[0]
        result.append(first)
    if len(data) > 1:
        second = data[1]
        result.append(second)
    return result

''',
        should_trigger=False,
        description="Conditional index access should not trigger",
        category=TestCategory.NEGATIVE,
    ),
    create_code_sample(
        name="cross_function_indexing",
        code='''"""Module demonstrating cross-function index access."""

from __future__ import annotations


def get_first(items: list[str]) -> str:
    """Get first item from list."""
    return items[0]


def get_second(items: list[str]) -> str:
    """Get second item from list."""
    return items[1]


def process_data(data: list[str]) -> tuple[str, str]:
    """Process data using separate functions."""
    first = get_first(data)
    second = get_second(data)
    return first, second

''',
        should_trigger=False,
        description=(
            "Sequential indices in different functions should not trigger"
        ),
        category=TestCategory.NEGATIVE,
    ),
]

# Export all samples for testing
ALL_SAMPLES = POSITIVE_SAMPLES + NEGATIVE_SAMPLES

# Summary information
TOTAL_POSITIVE_SAMPLES = len(POSITIVE_SAMPLES)
TOTAL_NEGATIVE_SAMPLES = len(NEGATIVE_SAMPLES)
TOTAL_SAMPLES = len(ALL_SAMPLES)


def get_samples_by_category(category: TestCategory) -> list[CodeSample]:
    """Get all samples for a specific category."""
    return [sample for sample in ALL_SAMPLES if sample.category == category]


def get_positive_samples() -> list[CodeSample]:
    """Get all positive test samples."""
    return POSITIVE_SAMPLES


def get_negative_samples() -> list[CodeSample]:
    """Get all negative test samples."""
    return NEGATIVE_SAMPLES


def get_sample_by_name(name: str) -> CodeSample | None:
    """Get a specific sample by name."""
    for sample in ALL_SAMPLES:
        if sample.name == name:
            return sample
    return None


if __name__ == "__main__":
    # Display sample summary for development testing
    print(  # noqa: T201
        f"EFP105 Test Samples: {TOTAL_SAMPLES} total "
        f"({TOTAL_POSITIVE_SAMPLES} positive, "
        f"{TOTAL_NEGATIVE_SAMPLES} negative)"
    )
