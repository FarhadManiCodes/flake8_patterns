# This code is inspired by examples from Brett Slatkin's
# Effective Python repository, licensed under Apache 2.0.

"""
Bad patterns that should trigger flake8-patterns rules.
These examples demonstrate anti-patterns from "Effective Python" (3rd Edition).

Run with: flake8 --select=EFP examples/bad_patterns.py
"""

# EFP105: Sequential indexing patterns (Item 5, Chapter 1)
def process_user_data():
    """Bad: Using sequential indexing instead of multiple-assignment unpacking."""
    user_tuple = ("Alice", 25, "Engineer")
    name = user_tuple[0]    # EFP105: Sequential indexing
    age = user_tuple[1]     # EFP105: Sequential indexing
    job = user_tuple[2]     # EFP105: Sequential indexing
    return f"{name} ({age}) - {job}"

def extract_coordinates():
    """Bad: Sequential indexing for coordinates."""
    point = (10.5, 20.3, 5.1)
    x = point[0]    # EFP105: Sequential indexing
    y = point[1]    # EFP105: Sequential indexing
    z = point[2]    # EFP105: Sequential indexing
    return x + y + z

# EFP213: Implicit string concatenation in collections (Item 13, Chapter 2)
config_items = [
    "database_host" "database_port",  # EFP213: Missing comma - dangerous!
    "redis_url",
    "api_key",
]

api_endpoints = [
    "users" "profile",    # EFP213: Missing comma creates single string
    "posts/recent",
    "auth/login",
]

# More complex EFP213 cases
settings = {
    "debug": True,
    "allowed_hosts": [
        "localhost" "127.0.0.1",  # EFP213: Missing comma
        "example.com",
    ]
}

# EFP318: Manual parallel iteration (Item 18, Chapter 3)
def calculate_scores():
    """Bad: Manual parallel iteration instead of using zip()."""
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]
    for i in range(len(names)):      # EFP318: Manual parallel iteration
        name = names[i]
        score = scores[i]
        print(f"{name}: {score}")

def process_matched_data():
    """Bad: Using range(len()) for parallel iteration."""
    keys = ["name", "age", "job"]
    values = ["Alice", 25, "Engineer"]
    result = {}
    for i in range(len(keys)):       # EFP318: Manual parallel iteration
        result[keys[i]] = values[i]
    return result

def merge_lists():
    """Bad: Manual indexing for merging."""
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    merged = []
    for i in range(len(list1)):      # EFP318: Manual parallel iteration
        merged.append((list1[i], list2[i]))
    return merged

# EFP320: Loop variable used after loop (Item 20, Chapter 3)
def find_admin(users):
    """Bad: Loop variable used after loop ends."""
    for user in users:
        if user.is_admin:
            break
    
    if user.is_admin:               # EFP320: Loop variable used after loop
        return user

def search_item(items, target):
    """Bad: Relying on loop variable after loop."""
    for item in items:
        if item.value == target:
            break
    
    return item.processed_value     # EFP320: Loop variable used after loop

def process_until_condition(data):
    """Bad: Using loop variable in finally block."""
    try:
        for item in data:
            if item.should_stop:
                break
            process(item)
    finally:
        log_last_item(item)         # EFP320: Loop variable used after loop

# EFP321: Multiple iterations over same parameter (Item 21, Chapter 3)
def normalize_data(numbers):
    """Bad: Multiple iterations over same parameter."""
    total = sum(numbers)            # First iteration
    result = []
    for value in numbers:           # Second iteration - EFP321
        percent = 100 * value / total
        result.append(percent)
    return result

def analyze_metrics(data):
    """Bad: Iterating over parameter multiple times."""
    count = len(data)               # First iteration
    average = sum(data) / count     # Second iteration - EFP321
    variance = sum((x - average) ** 2 for x in data) / count  # Third iteration - EFP321
    return {"count": count, "average": average, "variance": variance}

def process_with_validation(items):
    """Bad: Multiple iterations for validation and processing."""
    # Validation pass
    for item in items:              # First iteration
        if not item.is_valid:
            raise ValueError(f"Invalid item: {item}")
    
    # Processing pass  
    results = []
    for item in items:              # Second iteration - EFP321
        results.append(item.process())
    return results

# EFP426: try/except KeyError patterns (Item 26, Chapter 4)
def get_config_value(config, key):
    """Bad: Using try/except KeyError instead of dict.get()."""
    try:
        value = config[key]         # EFP426: Use dict.get() instead
    except KeyError:
        value = "default"
    return value

def extract_user_info(user_dict):
    """Bad: Multiple try/except blocks for dictionary access."""
    try:
        name = user_dict["name"]    # EFP426: Use dict.get() instead
    except KeyError:
        name = "Unknown"
    
    try:
        age = user_dict["age"]      # EFP426: Use dict.get() instead
    except KeyError:
        age = 0
    
    try:
        email = user_dict["email"]  # EFP426: Use dict.get() instead
    except KeyError:
        email = "no-email@example.com"
    
    return {"name": name, "age": age, "email": email}

def process_optional_fields(data):
    """Bad: try/except for optional dictionary fields."""
    result = {"id": data["id"]}  # Required field
    
    try:
        result["description"] = data["description"]  # EFP426: Use dict.get()
    except KeyError:
        result["description"] = "No description"
    
    try:
        result["tags"] = data["tags"]                # EFP426: Use dict.get()
    except KeyError:
        result["tags"] = []
    
    return result

# Complex combinations - multiple rule violations
def complex_bad_example():
    """Bad: Multiple rule violations in one function."""
    # EFP105 + EFP318 + EFP321
    data_pairs = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
    
    # EFP105: Sequential indexing
    names = []
    ages = []
    for pair in data_pairs:
        name = pair[0]              # EFP105
        age = pair[1]               # EFP105
        names.append(name)
        ages.append(age)
    
    # EFP318: Manual parallel iteration
    results = []
    for i in range(len(names)):     # EFP318
        name = names[i]
        age = ages[i]
        results.append(f"{name}: {age}")
    
    # EFP321: Multiple iterations over same data
    total_age = sum(ages)           # First iteration
    avg_age = total_age / len(ages) # Second iteration - EFP321
    
    return results, avg_age

def config_processor(config_dict):
    """Bad: Multiple EFP426 violations with complex logic."""
    # EFP426: Multiple try/except blocks
    try:
        host = config_dict["database_host"]     # EFP426
    except KeyError:
        host = "localhost"
    
    try:
        port = config_dict["database_port"]     # EFP426
    except KeyError:
        port = 5432
    
    try:
        ssl_enabled = config_dict["ssl_enabled"]  # EFP426
    except KeyError:
        ssl_enabled = False
    
    # EFP213: Implicit string concatenation
    connection_strings = [
        f"postgresql://{host}:{port}/prod" "?sslmode=require",  # EFP213
        f"postgresql://{host}:{port}/test",
    ]
    
    return connection_strings[0] if ssl_enabled else connection_strings[1]

# Future patterns that will be covered in later phases
def future_patterns():
    """Patterns that will be covered in High Performance Python phase."""
    # HPP001: String concatenation in loops (future v0.8.0+)
    result = ""
    for item in ["a", "b", "c"]:
        result += item              # Will be HPP001 in future
    
    # HPP002: List membership testing (future v0.8.0+)
    large_list = list(range(1000))
    for item in range(100):
        if item in large_list:      # Will be HPP002 in future
            print(f"Found: {item}")
    
    # HPP003: Missing __slots__ (future v0.8.0+)
    class DataPoint:                # Will be HPP003 in future
        def __init__(self, x, y):
            self.x = x
            self.y = y

# Edge cases and boundary conditions
def edge_cases():
    """Edge cases that should NOT trigger false positives."""
    # These should NOT trigger EFP105 (non-sequential indexing)
    data = [1, 2, 3, 4, 5]
    first = data[0]
    last = data[-1]
    middle = data[2]
    
    # These should NOT trigger EFP318 (not parallel iteration)
    for i in range(10):
        print(i)
    
    # These should NOT trigger EFP320 (loop variable used correctly)
    for item in [1, 2, 3]:
        if item == 2:
            break
    else:
        print("Not found")
    
    # These should NOT trigger EFP321 (single iteration)
    numbers = [1, 2, 3, 4, 5]
    result = sum(numbers)
    
    # These should NOT trigger EFP426 (appropriate try/except)
    try:
        result = risky_operation()
    except ValueError:  # Not KeyError
        result = "error"