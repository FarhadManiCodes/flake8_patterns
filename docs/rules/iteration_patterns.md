# Iteration Patterns

Documentation for iteration-related patterns from "Effective Python" (3rd Edition).

## Current Rules (Tier 1)

### EP318: Parallel Iteration with zip()
- **Chapter**: Item 18, Chapter 3: Functions
- **Status**: Tier 1 (High Priority)
- **Focus**: Replace manual parallel iteration with zip()

See [EP318 detailed documentation](EP318.md) for complete information.

### EP320: Loop Variables After Loop Ends
- **Chapter**: Item 20, Chapter 3: Functions  
- **Status**: Tier 1 (High Priority)
- **Focus**: Prevent bugs from post-loop variable usage

See [EP320 detailed documentation](EP320.md) for complete information.

### EP321: Be Defensive when Iterating over Arguments
- **Chapter**: Item 21, Chapter 3: Functions
- **Status**: Tier 1 (High Priority)  
- **Focus**: Handle iterator exhaustion in functions

See [EP321 detailed documentation](EP321.md) for complete information.

## Future Iteration Rules

### Tier 3 Rules (v0.7.0+)
- **EP317**: Comprehensive enumerate suggestions (Item 17) - when you need indices too
- **EP645**: yield from for Generator Composition (Item 45) - generator patterns

### Tier 2 Rules (v0.4.0+)
- **EP12103**: deque for Producer-Consumer Queues (Item 103) - efficient queue operations

## Overview

Iteration is fundamental to Python programming, but there are many subtle patterns that can lead to bugs or suboptimal code. Our rules focus on the most common and dangerous patterns identified in "Effective Python" by Brett Slatkin.

### Common Anti-Patterns We Detect

1. **Manual Parallel Iteration**: Using `range(len())` instead of `zip()`
2. **Iterator Exhaustion**: Functions that fail silently with iterators
3. **Post-Loop Variable Usage**: Dangerous reliance on loop variable values
4. **Inefficient Queue Operations**: Using lists instead of deque for queues

### Key Principles

- **Safety First**: Prevent silent failures and unexpected behavior
- **Pythonic Patterns**: Use built-in functions designed for iteration
- **Performance Awareness**: Choose the right data structure for iteration patterns
- **Defensive Programming**: Handle edge cases like empty sequences and iterators

## Quick Reference

| Pattern | Instead of | Use | Rule |
|---------|------------|-----|------|
| Parallel iteration | `for i in range(len(a)): x=a[i]; y=b[i]` | `for x, y in zip(a, b):` | EP318 |
| Post-loop usage | `for x in items: ...; use(x)` | `result = None; for x in items: result = x; use(result)` | EP320 |
| Multiple iterations | `sum(items); for x in items: ...` | `items = list(items); sum(items); for x in items: ...` | EP321 |
| Index + value | `for i in range(len(items)): print(i, items[i])` | `for i, item in enumerate(items): print(i, item)` | EP317* |
| Queue operations | `items.pop(0)` in loop | `from collections import deque; queue.popleft()` | EP12103* |

*Future rules (Tier 2/3)

## Implementation Status

- ✅ **EP318, EP320, EP321**: Tier 1 priority (v0.1.0-0.3.0)
- 🔄 **EP317, EP12103**: Tier 2 implementation (v0.4.0-0.6.0)  
- 📋 **EP645**: Tier 3 implementation (v0.7.0+)

## Book Context

These rules come from Chapter 3: Functions in "Effective Python", which focuses on how to write functions that work correctly with Python's iteration protocols. The chapter emphasizes:

- Understanding the difference between iterators and containers
- Using built-in functions designed for iteration
- Avoiding common pitfalls with loop variables and iterator exhaustion
- Writing defensive code that handles edge cases gracefully