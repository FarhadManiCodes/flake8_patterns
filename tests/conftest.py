"""Pytest configuration and fixtures for flake8_patterns tests."""

import ast

import pytest

from flake8_patterns.checker import PatternChecker


@pytest.fixture
def checker():
    """Create a PatternChecker instance."""

    def _checker(code: str):
        tree = ast.parse(code)
        return PatternChecker(tree, filename="test.py")

    return _checker


@pytest.fixture
def run_checker():
    """Run checker on code and return errors."""

    def _run_checker(code: str) -> list[tuple[int, int, str]]:
        tree = ast.parse(code)
        checker = PatternChecker(tree, filename="test.py")
        return list(checker.run())

    return _run_checker


# Tier 1 Rule Test Patterns (Verified Implementation Priority)

# EFP105: Multiple-Assignment Unpacking over Indexing
EFP105_BAD_SEQUENTIAL_INDEXING = """
item = ("Alice", 25, "Engineer")
name = item[0]      # Sequential indexing
age = item[1]       # Should trigger EFP105
job = item[2]       # Continues pattern
"""

EFP105_GOOD_UNPACKING = """
item = ("Alice", 25, "Engineer")
name, age, job = item  # Good multiple assignment
"""

# EFP213: Context-Aware String Concatenation
EFP213_BAD_IMPLICIT_CONCAT = """
items = [
    "first_item" "second_item",  # Missing comma - should trigger EFP213
    "third_item",
]
"""

EFP213_GOOD_EXPLICIT = """
items = [
    "first_item",     # Explicit comma
    "second_item",    # Clear separation
    "third_item",
]
"""

# EFP318: Parallel Iteration with zip()
EFP318_BAD_MANUAL_PARALLEL = """
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for i in range(len(names)):     # Should trigger EFP318
    name = names[i]
    age = ages[i]
    print(f"{name} is {age}")
"""

EFP318_GOOD_ZIP = """
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):  # Good parallel iteration
    print(f"{name} is {age}")
"""

# EFP320: Loop Variables After Loop Ends
EFP320_BAD_POST_LOOP_USAGE = """
def find_user(users):
    for user in users:
        if user.is_admin:
            break

    if user.is_admin:           # Should trigger EFP320
        return user
"""

EFP320_GOOD_DEFENSIVE = """
def find_user(users):
    admin_user = None
    for user in users:
        if user.is_admin:
            admin_user = user
            break

    if admin_user:              # Safe usage
        return admin_user
"""

# EFP321: Be Defensive when Iterating over Arguments
EFP321_BAD_MULTIPLE_ITERATION = """
def normalize(numbers):
    total = sum(numbers)        # First iteration
    result = []
    for value in numbers:       # Second iteration - should trigger EFP321
        percent = 100 * value / total
        result.append(percent)
    return result
"""

EFP321_GOOD_DEFENSIVE = """
def normalize(numbers):
    numbers = list(numbers)     # Defensive conversion
    total = sum(numbers)        # Now safe to iterate multiple times
    result = []
    for value in numbers:
        percent = 100 * value / total
        result.append(percent)
    return result
"""

# EFP426: Comprehensive dict.get() Patterns
EFP426_BAD_TRY_EXCEFPT = """
try:
    value = my_dict[key]        # Should trigger EFP426
except KeyError:
    value = default_value
"""

EFP426_GOOD_DICT_GET = """
value = my_dict.get(key, default_value)  # Clean and efficient
"""

# Future High Performance Python patterns (for v0.8.0+ testing)
HP001_FUTURE_STRING_CONCAT = """
# Future HP001: String concatenation in loops
result = ""
for item in ["a", "b", "c"]:
    result += item  # Will be HP001 in future
"""

PC001_FUTURE_LIST_MEMBERSHIP = """
# Future PC001: List membership testing
if "item" in ["a", "b", "c", "d", "e"]:  # Will be PC001 in future
    print("found")
"""


@pytest.fixture
def tier1_samples():
    """Provide Tier 1 rule test samples."""
    return {
        # EFP105: Multiple-Assignment Unpacking
        "ep105_bad": EFP105_BAD_SEQUENTIAL_INDEXING,
        "ep105_good": EFP105_GOOD_UNPACKING,
        # EFP213: Context-Aware String Concatenation
        "ep213_bad": EFP213_BAD_IMPLICIT_CONCAT,
        "ep213_good": EFP213_GOOD_EXPLICIT,
        # EFP318: Parallel Iteration with zip()
        "ep318_bad": EFP318_BAD_MANUAL_PARALLEL,
        "ep318_good": EFP318_GOOD_ZIP,
        # EFP320: Loop Variables After Loop Ends
        "ep320_bad": EFP320_BAD_POST_LOOP_USAGE,
        "ep320_good": EFP320_GOOD_DEFENSIVE,
        # EFP321: Be Defensive when Iterating over Arguments
        "ep321_bad": EFP321_BAD_MULTIPLE_ITERATION,
        "ep321_good": EFP321_GOOD_DEFENSIVE,
        # EFP426: Comprehensive dict.get() Patterns
        "ep426_bad": EFP426_BAD_TRY_EXCEFPT,
        "ep426_good": EFP426_GOOD_DICT_GET,
    }


@pytest.fixture
def future_samples():
    """Provide samples for future High Performance Python rules."""
    return {
        "hp001_future": HP001_FUTURE_STRING_CONCAT,
        "pc001_future": PC001_FUTURE_LIST_MEMBERSHIP,
    }


@pytest.fixture
def comprehensive_bad_code():
    """Comprehensive test file with multiple Tier 1 violations."""
    return '''
"""Test file with multiple Tier 1 rule violations."""

def process_data():
    # EFP105: Sequential indexing
    user_tuple = ("Alice", 25, "Engineer")
    name = user_tuple[0]    # Sequential indexing
    age = user_tuple[1]     # Should trigger EFP105
    job = user_tuple[2]     # Continues pattern

    # EFP213: Implicit string concatenation in collections
    config_items = [
        "database_host" "database_port",  # Missing comma - EFP213
        "redis_url",
    ]

    # EFP318: Manual parallel iteration
    names = ["Alice", "Bob"]
    scores = [85, 92]
    for i in range(len(names)):      # EFP318
        name = names[i]
        score = scores[i]
        print(f"{name}: {score}")

    # EFP320: Loop variable used after loop
    for user in users:
        if user.is_admin:
            break

    if user.is_admin:               # EFP320
        return user

    # EFP321: Multiple iterations over same parameter
    def analyze(items):
        count = len(items)              # First iteration
        total = sum(items)              # Second iteration - EFP321
        return total / count

    # EFP426: try/except KeyError patterns
    try:
        value = config[key]         # EFP426
    except KeyError:
        value = "default"

    return value
'''


@pytest.fixture
def comprehensive_good_code():
    """Comprehensive test file with good patterns (should not trigger errors)."""
    return '''
"""Test file with good patterns - should not trigger any errors."""

def process_data():
    # Good: Multiple assignment unpacking
    user_tuple = ("Alice", 25, "Engineer")
    name, age, job = user_tuple     # Good unpacking

    # Good: Explicit separation in collections
    config_items = [
        "database_host",            # Explicit comma
        "database_port",            # Clear separation
        "redis_url",
    ]

    # Good: Parallel iteration with zip()
    names = ["Alice", "Bob"]
    scores = [85, 92]
    for name, score in zip(names, scores):  # Good parallel iteration
        print(f"{name}: {score}")

    # Good: Defensive variable handling
    admin_user = None
    for user in users:
        if user.is_admin:
            admin_user = user
            break

    if admin_user:                  # Safe usage
        return admin_user

    # Good: Single iteration or defensive conversion
    def analyze(items):
        items = list(items)         # Defensive conversion
        count = len(items)
        total = sum(items)
        return total / count

    # Good: dict.get() usage
    value = config.get(key, "default")  # Clean and safe

    return value
'''


# Error code constants for testing
class ErrorCodes:
    """Expected error codes for testing."""

    # Tier 1 rules
    EFP105 = "EFP105"  # Multiple-Assignment Unpacking over Indexing
    EFP213 = "EFP213"  # Context-Aware String Concatenation
    EFP318 = "EFP318"  # Parallel Iteration with zip()
    EFP320 = "EFP320"  # Loop Variables After Loop Ends
    EFP321 = "EFP321"  # Be Defensive when Iterating over Arguments
    EFP426 = "EFP426"  # Comprehensive dict.get() patterns

    # Future rules (for preparation)
    HP001 = "HP001"  # String concatenation in loops (future)
    PC001 = "PC001"  # List membership testing (future)


def assert_error_code(errors, expected_code):
    """Helper to assert that a specific error code is present."""
    error_codes = [error[2] for error in errors]
    found_codes = [code for code in error_codes if expected_code in code]
    assert found_codes, f"Expected {expected_code} not found in {error_codes}"


def assert_no_errors(errors):
    """Helper to assert that no errors were found."""
    assert not errors, f"Expected no errors but found: {[error[2] for error in errors]}"


def assert_no_error_code(errors, unwanted_code):
    """Helper to assert that a specific error code is NOT present."""
    error_codes = [error[2] for error in errors]
    found_codes = [code for code in error_codes if unwanted_code in code]
    assert not found_codes, f"Unwanted {unwanted_code} found in {error_codes}"
