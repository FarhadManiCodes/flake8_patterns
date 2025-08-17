# This code is inspired by examples from Brett Slatkin's
# Effective Python repository, licensed under Apache 2.0.

"""Good patterns that follow "Effective Python" (3rd Edition) recommendations.
These examples demonstrate proper Pythonic patterns.

Run with: flake8 --select=EFP examples/good_patterns.py
Should produce no EFP### violations.
"""

import itertools
from dataclasses import dataclass


# EFP105: Multiple-assignment unpacking (Item 5, Chapter 1)
def process_user_data():
    """Good: Using multiple-assignment unpacking."""
    user_tuple = ("Alice", 25, "Engineer")
    name, age, job = user_tuple  # Good: Multiple-assignment unpacking
    return f"{name} ({age}) - {job}"


def extract_coordinates():
    """Good: Unpacking coordinates."""
    point = (10.5, 20.3, 5.1)
    x, y, z = point  # Good: Multiple-assignment unpacking
    return x + y + z


def process_first_last():
    """Good: Using unpacking with catch-all."""
    data = [1, 2, 3, 4, 5]
    first, *middle, last = data  # Good: Catch-all unpacking
    return first, middle, last


# EFP213: Explicit string handling (Item 13, Chapter 2)
config_items = [
    "database_host",  # Good: Explicit separation
    "database_port",
    "redis_url",
    "api_key",
]

api_endpoints = [
    "users/profile",  # Good: Explicit string
    "posts/recent",
    "auth/login",
]

# Good: Explicit string concatenation when needed
settings = {
    "debug": True,
    "allowed_hosts": [
        "localhost",  # Good: Explicit separation
        "127.0.0.1",
        "example.com",
    ],
}


# Good: Using f-strings for concatenation
def build_url(host, port, path):
    """Good: Using f-strings for string formatting."""
    return f"https://{host}:{port}/{path}"


# EFP318: Parallel iteration with zip() (Item 18, Chapter 3)
def calculate_scores():
    """Good: Using zip() for parallel iteration."""
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]
    for name, score in zip(
        names, scores, strict=False
    ):  # Good: zip() for parallel iter
        print(f"{name}: {score}")


def process_matched_data():
    """Good: Using zip() for parallel processing."""
    keys = ["name", "age", "job"]
    values = ["Alice", 25, "Engineer"]
    result = dict(zip(keys, values, strict=False))  # Good: zip() for dict
    return result


def merge_lists():
    """Good: Using zip() for merging lists."""
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    merged = list(zip(list1, list2, strict=False))  # Good: zip() for merging
    return merged


def process_with_index():
    """Good: Using enumerate() when index is needed."""
    items = ["a", "b", "c"]
    for i, item in enumerate(items):  # Good: enumerate() for index
        print(f"{i}: {item}")


# EFP320: Proper loop variable handling (Item 20, Chapter 3)
def find_admin(users):
    """Good: Not relying on loop variable after loop."""
    for user in users:
        if user.is_admin:
            return user  # Good: Return immediately
    return None  # Good: Explicit None return


def search_item(items, target):
    """Good: Using proper search pattern."""
    for item in items:
        if item.value == target:
            return item.processed_value  # Good: Return immediately
    return None  # Good: Explicit None return


def process_until_condition(data):
    """Good: Using proper exception handling."""
    last_item = None
    try:
        for item in data:
            last_item = item  # Good: Track explicitly
            if item.should_stop:
                break
            process(item)
    finally:
        if last_item:
            log_last_item(last_item)  # Good: Use explicit variable


def find_with_default(items, predicate, default=None):
    """Good: Using next() with default."""
    return next((item for item in items if predicate(item)), default)


# EFP321: Single iteration over parameters (Item 21, Chapter 3)
def normalize_data(numbers):
    """Good: Single iteration with generator expression."""
    numbers_list = list(numbers)  # Good: Convert to list once
    total = sum(numbers_list)  # Use list
    return [100 * value / total for value in numbers_list]  # Use same list


def analyze_metrics(data):
    """Good: Single pass with statistics module."""
    import statistics

    data_list = list(data)  # Good: Convert once
    return {
        "count": len(data_list),
        "average": statistics.mean(data_list),
        "variance": statistics.variance(data_list),
    }


def process_with_validation(items):
    """Good: Combine validation and processing."""
    results = []
    for item in items:  # Good: Single iteration
        if not item.is_valid:
            raise ValueError(f"Invalid item: {item}")
        results.append(item.process())
    return results


def defensive_iteration(items):
    """Good: Defensive iteration pattern."""
    items_iter = iter(items)  # Good: Create iterator once
    return [item.process() for item in items_iter]


# EFP426: Using dict.get() (Item 26, Chapter 4)
def get_config_value(config, key):
    """Good: Using dict.get() with default."""
    return config.get(key, "default")  # Good: dict.get() with default


def extract_user_info(user_dict):
    """Good: Using dict.get() for optional fields."""
    return {
        "name": user_dict.get("name", "Unknown"),
        "age": user_dict.get("age", 0),
        "email": user_dict.get("email", "no-email@example.com"),
    }


def process_optional_fields(data):
    """Good: Using dict.get() for optional fields."""
    return {
        "id": data["id"],  # Required field - can use []
        "description": data.get("description", "No description"),
        "tags": data.get("tags", []),
    }


def get_nested_value(data, path, default=None):
    """Good: Safe nested dictionary access."""
    result = data
    for key in path:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return default
    return result


# Advanced good patterns
def complex_good_example():
    """Good: Proper patterns combined."""
    data_pairs = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]

    # Good: Direct unpacking in loop
    names, ages = zip(*data_pairs, strict=False)  # Good: zip unpacking

    # Good: zip() for parallel processing
    results = [f"{name}: {age}" for name, age in data_pairs]

    # Good: Single calculation
    avg_age = sum(ages) / len(ages)

    return results, avg_age


def config_processor(config_dict):
    """Good: Using dict.get() throughout."""
    host = config_dict.get("database_host", "localhost")
    port = config_dict.get("database_port", 5432)
    ssl_enabled = config_dict.get("ssl_enabled", False)

    # Good: Explicit string formatting
    base_url = f"postgresql://{host}:{port}"
    prod_url = f"{base_url}/prod?sslmode=require"
    test_url = f"{base_url}/test"

    return prod_url if ssl_enabled else test_url


# Pattern variations and edge cases
def pattern_variations():
    """Good: Various correct patterns."""
    # Good: Non-sequential indexing (not EFP105)
    data = [1, 2, 3, 4, 5]
    first = data[0]
    last = data[-1]
    middle = data[len(data) // 2]

    # Good: Single iteration patterns
    for i in range(10):
        print(i)

    # Good: Loop with else clause
    for item in [1, 2, 3]:
        if item == 2:
            break
    else:
        print("Not found")

    # Good: Try/except for non-KeyError exceptions
    try:
        result = risky_operation()
    except ValueError:
        result = "error"

    return first, last, middle, result


# Modern Python patterns (3.10+)
def modern_patterns():
    """Good: Modern Python patterns."""

    # Good: Match statement (Python 3.10+)
    def process_value(value):
        match value:
            case int() if value > 0:
                return f"Positive: {value}"
            case int() if value < 0:
                return f"Negative: {value}"
            case 0:
                return "Zero"
            case _:
                return "Unknown"

    # Good: Walrus operator for efficiency
    data = [1, 2, 3, 4, 5]
    if (n := len(data)) > 3:
        print(f"Large dataset: {n}")

    # Good: Type hints
    def typed_function(items: list[str]) -> dict[str, int]:
        return {item: len(item) for item in items}

    return process_value, typed_function


# Context managers and resource handling
def good_resource_handling():
    """Good: Proper resource handling patterns."""
    # Good: Context manager
    with open("file.txt") as f:
        content = f.read()

    # Good: Multiple context managers
    with open("input.txt") as infile, open("output.txt", "w") as outfile:
        outfile.write(infile.read())

    return content


# Generator patterns
def good_generator_patterns():
    """Good: Generator and iterator patterns."""

    # Good: Generator expression
    def squares(n):
        return (x**2 for x in range(n))

    # Good: Generator function
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    # Good: Using itertools

    def batched(iterable, n):
        """Good: Batching pattern."""
        iterator = iter(iterable)
        while batch := list(itertools.islice(iterator, n)):
            yield batch

    return squares, fibonacci, batched


# Class patterns
class GoodClass:
    """Good: Proper class design patterns."""

    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__
        return f"{cls_name}(name={self.name!r}, value={self.value})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.name == other.name and self.value == other.value

    @property
    def display_name(self) -> str:
        """Good: Property for computed attribute."""
        return f"{self.name.title()} ({self.value})"


# Data class pattern (Python 3.7+)


@dataclass
class GoodDataClass:
    """Good: Using dataclass for data containers."""

    name: str
    age: int
    email: str | None = None

    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")


# Testing patterns
def good_testing_patterns():
    """Good: Patterns that work well with testing."""

    # Good: Pure functions
    def add(a, b):
        return a + b

    # Good: Dependency injection
    def process_data(data, processor=None):
        if processor is None:
            processor = default_processor
        return processor(data)

    # Good: Explicit error handling
    def safe_divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    return add, process_data, safe_divide


# Performance-conscious patterns
def performance_patterns(user_id=1):
    """Good: Performance-conscious patterns."""
    # Good: List comprehension over map/filter
    data = range(100)
    squares = [x**2 for x in data if x % 2 == 0]

    # Good: Set for membership testing
    valid_ids = {1, 2, 3, 4, 5}
    if user_id in valid_ids:
        return True

    # Good: str.join() for string concatenation
    parts = ["hello", "world", "python"]
    result = " ".join(parts)

    # Good: Using collections.defaultdict
    from collections import defaultdict

    groups = defaultdict(list)
    for item in data:
        groups[item % 3].append(item)

    return squares, result, dict(groups)


# Helper functions for examples
def risky_operation():
    """Placeholder for risky operation."""
    return "success"


def default_processor(data):
    """Placeholder for default processor."""
    return data


def process(item):
    """Placeholder for processing function."""
    return item


def log_last_item(item):
    """Placeholder for logging function."""


# Main demonstration
if __name__ == "__main__":
    print("Good patterns demonstration")
    print("Run: flake8 --select=EFP examples/good_patterns.py")
    print("Should produce no EFP### violations")
