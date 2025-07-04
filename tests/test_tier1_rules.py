"""Tests for Tier 1 rules - High Priority Implementation.

These tests cover the 6 verified Tier 1 rules that address major gaps
in existing Python linting tools:

- EFP105: Multiple-Assignment Unpacking over Indexing
- EFP213: Context-Aware String Concatenation
- EFP318: Parallel Iteration with zip()
- EFP320: Loop Variables After Loop Ends
- EFP321: Be Defensive when Iterating over Arguments
- EFP426: Comprehensive dict.get() patterns
"""

from .conftest import ErrorCodes, assert_error_code, assert_no_error_code


class TestEFP105MultipleAssignmentUnpacking:
    """Test EFP105: Multiple-Assignment Unpacking over Indexing.

    Book Reference: "Effective Python" Item 5, Chapter 1: Pythonic Thinking
    Pattern: x = item[0]; y = item[1] → x, y = item
    """

    def test_detects_sequential_indexing(self, run_checker, tier1_samples):
        """Should detect sequential indexing patterns."""
        errors = run_checker(tier1_samples["ep105_bad"])
        assert_error_code(errors, ErrorCodes.EFP105)

    def test_allows_good_unpacking(self, run_checker, tier1_samples):
        """Should not flag proper multiple assignment unpacking."""
        errors = run_checker(tier1_samples["ep105_good"])
        assert_no_error_code(errors, ErrorCodes.EFP105)

    def test_coordinate_extraction_pattern(self, run_checker):
        """Should detect coordinate extraction anti-pattern."""
        code = """
point = (10, 20)
x = point[0]    # Sequential indexing
y = point[1]    # Should trigger EFP105
distance = (x**2 + y**2)**0.5
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP105)

    def test_non_sequential_indexing_ignored(self, run_checker):
        """Should not flag non-sequential indexing."""
        code = """
item = (1, 2, 3, 4)
x = item[0]     # First access
z = item[2]     # Non-sequential - should not trigger EFP105
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP105)

    def test_single_indexing_ignored(self, run_checker):
        """Should not flag single indexing access."""
        code = """
item = (1, 2, 3)
x = item[0]     # Single access - should not trigger EFP105
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP105)


class TestEFP213ContextAwareStringConcatenation:
    """Test EFP213: Context-Aware String Concatenation.

    Book Reference: "Effective Python" Item 13, Chapter 2: Lists and Dictionaries
    Pattern: Implicit concatenation in collections → explicit concatenation
    """

    def test_detects_missing_comma_in_list(self, run_checker, tier1_samples):
        """Should detect dangerous implicit concatenation in lists."""
        errors = run_checker(tier1_samples["ep213_bad"])
        assert_error_code(errors, ErrorCodes.EFP213)

    def test_allows_explicit_commas(self, run_checker, tier1_samples):
        """Should not flag explicit comma separation."""
        errors = run_checker(tier1_samples["ep213_good"])
        assert_no_error_code(errors, ErrorCodes.EFP213)

    def test_function_arguments_pattern(self, run_checker):
        """Should detect implicit concatenation in function arguments."""
        code = """
process_items([
    "item1" "item2",  # Missing comma - should trigger EFP213
    "item3"
])
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP213)

    def test_tuple_pattern(self, run_checker):
        """Should detect implicit concatenation in tuples."""
        code = """
config = (
    "host" "port",    # Missing comma - should trigger EFP213
    "database",
)
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP213)

    def test_intentional_concatenation_outside_collections(self, run_checker):
        """Should not flag intentional concatenation outside dangerous contexts."""
        code = """
# Intentional concatenation - should not trigger EFP213
message = "Hello " "World"
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP213)


class TestEFP318ParallelIterationWithZip:
    """Test EFP318: Parallel Iteration with zip().

    Book Reference: "Effective Python" Item 18, Chapter 3: Functions
    Pattern: for i in range(len(a)): x=a[i]; y=b[i] → for x, y in zip(a, b)
    """

    def test_detects_manual_parallel_iteration(self, run_checker, tier1_samples):
        """Should detect manual parallel iteration patterns."""
        errors = run_checker(tier1_samples["ep318_bad"])
        assert_error_code(errors, ErrorCodes.EFP318)

    def test_allows_zip_iteration(self, run_checker, tier1_samples):
        """Should not flag proper zip() usage."""
        errors = run_checker(tier1_samples["ep318_good"])
        assert_no_error_code(errors, ErrorCodes.EFP318)

    def test_matrix_operations_pattern(self, run_checker):
        """Should detect parallel iteration in matrix operations."""
        code = """
matrix1 = [[1, 2], [3, 4]]
matrix2 = [[5, 6], [7, 8]]
result = []
for i in range(len(matrix1)):       # Should trigger EFP318
    row = []
    for j in range(len(matrix1[i])):
        row.append(matrix1[i][j] + matrix2[i][j])
    result.append(row)
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP318)

    def test_index_actually_needed(self, run_checker):
        """Should not flag when index is actually used."""
        code = """
items = ["a", "b", "c"]
for i in range(len(items)):     # Index is used - should not trigger EFP318
    print(f"Item {i}: {items[i]}")
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP318)

    def test_single_sequence_access(self, run_checker):
        """Should not flag single sequence access."""
        code = """
items = [1, 2, 3]
for i in range(len(items)):     # Single sequence - should not trigger EFP318
    print(items[i])
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP318)


class TestEFP320LoopVariablesAfterLoopEnds:
    """Test EFP320: Loop Variables After Loop Ends.

    Book Reference: "Effective Python" Item 20, Chapter 3: Functions
    Pattern: Using loop variables after loop completion
    """

    def test_detects_post_loop_variable_usage(self, run_checker, tier1_samples):
        """Should detect loop variable usage after loop ends."""
        errors = run_checker(tier1_samples["ep320_bad"])
        assert_error_code(errors, ErrorCodes.EFP320)

    def test_allows_defensive_patterns(self, run_checker, tier1_samples):
        """Should not flag defensive variable handling."""
        errors = run_checker(tier1_samples["ep320_good"])
        assert_no_error_code(errors, ErrorCodes.EFP320)

    def test_empty_sequence_danger(self, run_checker):
        """Should detect dangerous pattern with potentially empty sequences."""
        code = """
def find_large_number(numbers):
    for num in numbers:
        if num > 100:
            break

    print(f"Found: {num}")      # Should trigger EFP320 - what if numbers is empty?
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP320)

    def test_for_else_pattern_safe(self, run_checker):
        """Should not flag for-else patterns which are safer."""
        code = """
def find_item(items):
    for item in items:
        if item.matches():
            break
    else:
        item = None             # Explicit assignment

    return item                 # Safe usage
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP320)

    def test_intentional_final_value(self, run_checker):
        """Should not flag intentional final value usage."""
        code = """
for i in range(10):
    pass

print(f"Final counter: {i}")    # Intentional - should not trigger EFP320
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP320)


class TestEFP321DefensiveIterationOverArguments:
    """Test EFP321: Be Defensive when Iterating over Arguments.

    Book Reference: "Effective Python" Item 21, Chapter 3: Functions
    Pattern: Functions iterating same parameter multiple times
    """

    def test_detects_multiple_iteration(self, run_checker, tier1_samples):
        """Should detect functions iterating over parameters multiple times."""
        errors = run_checker(tier1_samples["ep321_bad"])
        assert_error_code(errors, ErrorCodes.EFP321)

    def test_allows_defensive_conversion(self, run_checker, tier1_samples):
        """Should not flag defensive iterator conversion."""
        errors = run_checker(tier1_samples["ep321_good"])
        assert_no_error_code(errors, ErrorCodes.EFP321)

    def test_builtin_functions_count_as_iteration(self, run_checker):
        """Should detect built-in functions as iterations."""
        code = """
def analyze_data(values):
    count = len(values)         # First iteration
    maximum = max(values)       # Second iteration - should trigger EFP321
    for val in values:          # Third iteration
        process(val)
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP321)

    def test_comprehensions_count_as_iteration(self, run_checker):
        """Should detect comprehensions as iterations."""
        code = """
def process_items(items):
    filtered = [x for x in items if x > 0]      # First iteration
    mapped = [x*2 for x in items]               # Second iteration - should
    # trigger EFP321
    return filtered, mapped
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP321)

    def test_single_iteration_allowed(self, run_checker):
        """Should not flag functions with single iteration."""
        code = """
def process_all(items):
    return [process(item) for item in items]    # Single iteration - OK
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP321)


class TestEFP426ComprehensiveDictGetPatterns:
    """Test EFP426: Comprehensive dict.get() Patterns.

    Book Reference: "Effective Python" Item 26, Chapter 4: Comprehensions and Generators
    Pattern: try: x = d[key]; except KeyError: x = default → x = d.get(key, default)
    """

    def test_detects_try_except_keyerror(self, run_checker, tier1_samples):
        """Should detect try/except KeyError patterns."""
        errors = run_checker(tier1_samples["ep426_bad"])
        assert_error_code(errors, ErrorCodes.EFP426)

    def test_allows_dict_get(self, run_checker, tier1_samples):
        """Should not flag proper dict.get() usage."""
        errors = run_checker(tier1_samples["ep426_good"])
        assert_no_error_code(errors, ErrorCodes.EFP426)

    def test_if_in_dict_pattern(self, run_checker):
        """Should detect if-in-dict patterns."""
        code = """
if key in my_dict:
    value = my_dict[key]        # Should trigger EFP426
else:
    value = default_value
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP426)

    def test_setdefault_candidates(self, run_checker):
        """Should detect manual setdefault patterns."""
        code = """
if key not in my_dict:
    my_dict[key] = []           # Should trigger EFP426 - use setdefault
my_dict[key].append(item)
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP426)

    def test_complex_exception_handling_allowed(self, run_checker):
        """Should not flag complex exception handling."""
        code = """
try:
    value = complex_dict[key]
except KeyError:
    log_missing_key(key)        # Additional processing - should not trigger EFP426
    notify_admin(key)
    value = fallback_value
"""
        errors = run_checker(code)
        assert_no_error_code(errors, ErrorCodes.EFP426)

    def test_nested_dict_access(self, run_checker):
        """Should detect nested dictionary access patterns."""
        code = """
try:
    host = config['database']['host']       # Should trigger EFP426
except KeyError:
    host = 'localhost'
"""
        errors = run_checker(code)
        assert_error_code(errors, ErrorCodes.EFP426)


class TestTier1Integration:
    """Integration tests for multiple Tier 1 rules working together."""

    def test_comprehensive_bad_code_detection(
        self, run_checker, comprehensive_bad_code
    ):
        """Should detect multiple Tier 1 violations in comprehensive test."""
        errors = run_checker(comprehensive_bad_code)

        # Should detect at least one instance of each Tier 1 rule
        expected_codes = [
            ErrorCodes.EFP105,
            ErrorCodes.EFP213,
            ErrorCodes.EFP318,
            ErrorCodes.EFP320,
            ErrorCodes.EFP321,
            ErrorCodes.EFP426,
        ]

        error_messages = [error[2] for error in errors]
        for expected_code in expected_codes:
            found = any(expected_code in msg for msg in error_messages)
            assert found, f"Expected {expected_code} not found in comprehensive test"

    def test_comprehensive_good_code_clean(self, run_checker, comprehensive_good_code):
        """Should not flag any Tier 1 violations in good code."""
        errors = run_checker(comprehensive_good_code)

        # Should not flag any Tier 1 rules
        tier1_codes = [
            ErrorCodes.EFP105,
            ErrorCodes.EFP213,
            ErrorCodes.EFP318,
            ErrorCodes.EFP320,
            ErrorCodes.EFP321,
            ErrorCodes.EFP426,
        ]

        error_messages = [error[2] for error in errors]
        for code in tier1_codes:
            found = any(code in msg for msg in error_messages)
            assert not found, f"Unexpected {code} found in good code: {error_messages}"

    def test_no_false_positives_on_standard_patterns(self, run_checker):
        """Should not flag common standard Python patterns."""
        code = """
# Standard patterns that should NOT trigger any Tier 1 rules
def standard_patterns():
    # Standard iteration
    for item in items:
        process(item)

    # Standard dictionary access
    value = my_dict[known_key]  # When key is known to exist

    # Standard list operations
    items = ["a", "b", "c"]
    first = items[0]            # Single access is OK

    # Standard string operations
    message = "Hello World"     # Single string, no concatenation

    # Standard function patterns
    def single_pass(data):
        return sum(data)        # Single iteration is fine
"""
        errors = run_checker(code)

        # Should not trigger any Tier 1 rules
        tier1_codes = [
            ErrorCodes.EFP105,
            ErrorCodes.EFP213,
            ErrorCodes.EFP318,
            ErrorCodes.EFP320,
            ErrorCodes.EFP321,
            ErrorCodes.EFP426,
        ]

        for code in tier1_codes:
            assert_no_error_code(errors, code)
