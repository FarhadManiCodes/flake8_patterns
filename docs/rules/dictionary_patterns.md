# Dictionary Patterns

Documentation for dictionary-related patterns from "Effective Python" (3rd Edition).

## Current Rules (Tier 1)

### EFP426: Comprehensive dict.get() Patterns
- **Chapter**: Item 26, Chapter 4: Comprehensions and Generators
- **Status**: Tier 1 (High Priority)
- **Focus**: Use dict.get() over KeyError handling and manual key checking

See [EFP426 detailed documentation](EFP426.md) for complete information.

## Future Dictionary Rules

### Tier 2 Rules (v0.4.0+)
- **EFP427**: defaultdict over setdefault (Item 27) - when setdefault gets repetitive
- **EFP429**: Avoid Deep Nesting → Classes (Item 29) - complex nested dictionaries

## Overview

Dictionaries are fundamental to Python programming, but there are many patterns for accessing and manipulating them safely and efficiently. Our rules focus on the most common and error-prone patterns identified in "Effective Python" by Brett Slatkin.

### Common Anti-Patterns We Detect

1. **Manual KeyError Handling**: Using try/except instead of dict.get()
2. **Check-Then-Access**: Race-prone `if key in dict` followed by `dict[key]`
3. **Repetitive setdefault**: Multiple setdefault calls that should use defaultdict
4. **Over-Nested Dictionaries**: Complex nested structures that should be classes

### Key Principles

- **Safety First**: Avoid KeyError exceptions and race conditions
- **Readability**: Use methods that express intent clearly
- **Performance**: Choose efficient patterns for common operations
- **Maintainability**: Prefer simple patterns over complex nested access

## Quick Reference

| Pattern | Instead of | Use | Rule |
|---------|------------|-----|------|
| KeyError handling | `try: x = d[k]; except KeyError: x = default` | `x = d.get(k, default)` | EFP426 |
| Check-then-access | `if k in d: x = d[k]; else: x = default` | `x = d.get(k, default)` | EFP426 |
| Repeated setdefault | Multiple `d.setdefault(k, []).append(v)` | `from collections import defaultdict` | EFP427* |
| Deep nesting | `d['a']['b']['c']['d'] = value` | Use classes or namedtuples | EFP429* |

*Future rules (Tier 2)

## Examples by Complexity

### Basic Access Patterns (EFP426)
```python
# ❌ Try/except KeyError
try:
    value = config['database']['host']
except KeyError:
    value = 'localhost'

# ✅ Chained get()
value = config.get('database', {}).get('host', 'localhost')
```

### Repeated Operations (EFP427 - Future)
```python
# ❌ Repetitive setdefault
groups = {}
for item in items:
    groups.setdefault(item.category, []).append(item)

# ✅ defaultdict
from collections import defaultdict
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)
```

### Complex Nesting (EFP429 - Future)
```python
# ❌ Deep nested dictionary
user = {
    'profile': {
        'personal': {
            'name': 'Alice',
            'contact': {
                'email': 'alice@example.com',
                'phone': {
                    'home': '555-1234',
                    'work': '555-5678'
                }
            }
        }
    }
}

# ✅ Structured classes
from dataclasses import dataclass

@dataclass
class PhoneNumbers:
    home: str
    work: str

@dataclass
class ContactInfo:
    email: str
    phone: PhoneNumbers

@dataclass
class PersonalInfo:
    name: str
    contact: ContactInfo

@dataclass
class UserProfile:
    personal: PersonalInfo

user = UserProfile(
    personal=PersonalInfo(
        name='Alice',
        contact=ContactInfo(
            email='alice@example.com',
            phone=PhoneNumbers(home='555-1234', work='555-5678')
        )
    )
)
```

## Common Dictionary Operations

### Safe Access Patterns
```python
# ✅ Basic safe access
value = my_dict.get(key, default)

# ✅ Nested safe access
user_name = data.get('user', {}).get('profile', {}).get('name', 'Anonymous')

# ✅ Safe access with callable default
cache = {}
result = cache.get(key) or cache.setdefault(key, expensive_computation())
```

### Initialization Patterns
```python
# ✅ Initialize with defaults
config = {
    'host': 'localhost',
    'port': 5432,
    'debug': False,
    **user_config  # Override with user settings
}

# ✅ defaultdict for grouping
from collections import defaultdict
groups = defaultdict(list)
counters = defaultdict(int)
```

### Update Patterns
```python
# ✅ Safe update
existing_config.update(new_config)

# ✅ Merge dictionaries (Python 3.9+)
merged = config1 | config2

# ✅ Conditional update
if 'new_feature' not in config:
    config['new_feature'] = True
```

## Implementation Status

- ✅ **EFP426**: Tier 1 priority (v0.1.0-0.3.0)
- 🔄 **EFP427, EFP429**: Tier 2 implementation (v0.4.0-0.6.0)

## Book Context

These rules come from Chapter 4: Comprehensions and Generators in "Effective Python", which covers efficient patterns for working with collections including dictionaries. The chapter emphasizes:

- Using appropriate methods for safe dictionary access
- Choosing the right data structure for the task
- Avoiding overly complex nested structures
- Writing defensive code that handles missing keys gracefully

## Performance Considerations

- `dict.get()` is faster than try/except for missing keys
- `defaultdict` eliminates repeated setdefault calls
- Chained `get()` calls create intermediate objects (minor overhead)
- Classes with `__slots__` can be more memory efficient than nested dicts
- Modern dict implementations (Python 3.7+) maintain insertion order

## Best Practices

1. **Use dict.get() for missing keys** instead of try/except or if/in checks
2. **Use defaultdict for grouping operations** instead of repeated setdefault
3. **Limit nesting depth** - consider classes for complex nested data
4. **Use type hints** to make dictionary structure explicit
5. **Consider dataclasses or namedtuples** for structured data instead of dicts
