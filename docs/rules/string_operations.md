# String Operations

Documentation for verified string-related patterns from "Effective Python" (3rd Edition).

## Current Rules

### EP213: Context-Aware String Concatenation
- **Chapter**: Item 13, Chapter 2: Lists and Dictionaries
- **Status**: Tier 1 (High Priority)
- **Focus**: Implicit string concatenation in dangerous contexts

See [EP213 detailed documentation](EP213.md) for complete information.

## Future String Rules

### Tier 2 Rules (v0.4.0+)
- **EP216**: Catch-All Unpacking over Slicing (Item 16) - involves string slicing patterns
- **EP215**: Avoid Striding and Slicing Together (Item 15) - string slicing complexity

### High Performance Python Integration (v0.8.0+)
- **HP001**: String concatenation in loops → use `str.join()`
- **HP002**: Multiple string concatenations → optimize patterns
- **HP003**: String formatting optimization patterns

## Overview

String operations in Python have many subtleties that can lead to bugs or performance issues. Our rules focus on the most common and dangerous patterns identified in "Effective Python" by Brett Slatkin.
