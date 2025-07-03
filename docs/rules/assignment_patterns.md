# Assignment Patterns

Documentation for assignment-related patterns from "Effective Python" (3rd Edition).

## Current Rules (Tier 1)

### EP105: Multiple-Assignment Unpacking over Indexing
- **Chapter**: Item 5, Chapter 1: Pythonic Thinking
- **Status**: Tier 1 (High Priority)
- **Focus**: Replace sequential indexing with tuple unpacking

See [EP105 detailed documentation](EP105.md) for complete information.

## Future Assignment Rules

### Tier 2 Rules (v0.4.0+)
- **EP216**: Catch-All Unpacking over Slicing (Item 16) - advanced unpacking patterns
- **EP531**: Return Objects vs >3 Tuple Unpacking (Item 31) - when unpacking gets complex

### Tier 3 Rules (v0.7.0+)
- **EP108**: Assignment Expressions for Repetition (Item 8) - walrus operator patterns

## Overview

Assignment patterns in Python offer powerful ways to write more readable and maintainable code. Our rules focus on helping developers use Python's assignment features effectively, particularly unpacking and modern assignment expressions.

### Common Anti-Patterns We Detect

1. **Sequential Indexing**: Using `x = item[0]; y = item[1]` instead of `x, y = item`
2. **Complex Slicing**: Using `head = items[0]; rest = items[1:]` instead of `head, *rest = items`
3. **Repetitive Expressions**: Repeated complex expressions that could use walrus operator
4. **Over-Complex Unpacking**: Functions returning too many values as tuples

### Key Principles

- **Readability**: Assignment should be self-documenting
- **Error Prevention**: Reduce index-related bugs
- **Modern Python**: Use newer features like starred expressions and walrus operator
- **Appropriate Complexity**: Know when unpacking becomes too complex

## Quick Reference

| Pattern | Instead of | Use | Rule |
|---------|------------|-----|------|
| Sequential indexing | `x = item[0]; y = item[1]` | `x, y = item` | EP105 |
| Head/tail slicing | `head = items[0]; rest = items[1:]` | `head, *rest = items` | EP216* |
| Repeated expressions | `if (x := func()) and x > 5: ...` | Use walrus operator | EP108* |
| Complex returns | `return a, b, c, d, e` | Return object or namedtuple | EP531* |

*Future rules (Tier 2/3)

## Examples by Complexity

### Simple Unpacking (EP105)
```python
# ❌ Sequential indexing
point = (10, 20)
x = point[0]
y = point[1]

# ✅ Multiple assignment
x, y = point
```

### Advanced Unpacking (EP216 - Future)
```python
# ❌ Manual slicing
items = [1, 2, 3, 4, 5]
first = items[0]
rest = items[1:]

# ✅ Catch-all unpacking
first, *rest = items
```

### Assignment Expressions (EP108 - Future)
```python
# ❌ Repetitive expression
data = expensive_function()
if data and len(data) > 10:
    process(data)

# ✅ Walrus operator (Python 3.8+)
if (data := expensive_function()) and len(data) > 10:
    process(data)
```

### Complex Returns (EP531 - Future)
```python
# ❌ Too many return values
def get_user_info():
    return name, email, age, phone, address, city, state, zip_code

# ✅ Return object
from dataclasses import dataclass

@dataclass
class UserInfo:
    name: str
    email: str
    age: int
    phone: str
    address: str
    city: str
    state: str
    zip_code: str

def get_user_info():
    return UserInfo(...)
```

## Implementation Status

- ✅ **EP105**: Tier 1 priority (v0.1.0-0.3.0)
- 🔄 **EP216, EP531**: Tier 2 implementation (v0.4.0-0.6.0)
- 📋 **EP108**: Tier 3 implementation (v0.7.0+)

## Book Context

These rules span multiple chapters of "Effective Python":

- **Chapter 1: Pythonic Thinking** - Basic unpacking patterns that make code more readable
- **Chapter 2: Lists and Dictionaries** - Advanced unpacking with starred expressions  
- **Chapter 5: Classes and Inheritance** - When to use objects instead of complex tuples

The common theme is making assignment operations more expressive and less error-prone while maintaining Python's philosophy of "explicit is better than implicit."

## Design Principles

1. **Clarity Over Cleverness**: Assignment should make intent obvious
2. **Reduce Index Errors**: Eliminate manual indexing where possible  
3. **Right Tool for Job**: Use unpacking for small tuples, objects for complex data
4. **Modern Python**: Embrace newer language features when they improve readability