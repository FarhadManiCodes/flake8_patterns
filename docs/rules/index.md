# Rule Documentation Index

Comprehensive documentation for all flake8-patterns rules based on "Effective Python" (3rd Edition) by Brett Slatkin.

## Tier 1 Rules (v0.1.0-0.3.0) - High Impact Priority

These 6 rules address the most common and dangerous anti-patterns with no existing tool coverage:

### [EP105: Multiple-Assignment Unpacking over Indexing](EP105.md)
- **Pattern**: `x = item[0]; y = item[1]` → `x, y = item`
- **Impact**: Readability, error prevention
- **Gap**: No existing tool detects sequential indexing patterns

### [EP213: Context-Aware String Concatenation](EP213.md)
- **Pattern**: Implicit concatenation in collections → explicit concatenation
- **Impact**: Bug prevention (missing commas)
- **Gap**: flake8-implicit-str-concat lacks context awareness

### [EP318: Parallel Iteration with zip()](EP318.md)
- **Pattern**: `for i in range(len(a)): x=a[i]; y=b[i]` → `for x, y in zip(a, b)`
- **Impact**: Readability, safety, handles length differences
- **Gap**: No tool detects manual parallel iteration

### [EP320: Loop Variables After Loop Ends](EP320.md)
- **Pattern**: Using loop variables after loop completion
- **Impact**: Bug prevention (undefined/unexpected values)
- **Gap**: flake8-bugbear B023 covers closures, not direct usage

### [EP321: Be Defensive when Iterating over Arguments](EP321.md)
- **Pattern**: Functions iterating same parameter multiple times
- **Impact**: Bug prevention (iterator exhaustion)
- **Gap**: No tool detects iterator exhaustion patterns

### [EP426: Comprehensive dict.get() Patterns](EP426.md)
- **Pattern**: `try: x = d[k]; except KeyError: x = default` → `x = d.get(k, default)`
- **Impact**: Readability, safety, performance
- **Gap**: flake8-simplify SIM124 covers only ~25% of patterns

## Rules by Category

### [Assignment Patterns](assignment_patterns.md)
- **EP105**: Multiple-Assignment Unpacking over Indexing ✅ Tier 1
- **EP216**: Catch-All Unpacking over Slicing (Tier 2)
- **EP531**: Return Objects vs >3 Tuple Unpacking (Tier 2)
- **EP108**: Assignment Expressions for Repetition (Tier 3)

### [String Operations](string_operations.md)
- **EP213**: Context-Aware String Concatenation ✅ Tier 1
- **EP215**: Avoid Striding and Slicing Together (Tier 3)
- **EP216**: Catch-All Unpacking over Slicing (Tier 2)

### [Iteration Patterns](iteration_patterns.md)
- **EP318**: Parallel Iteration with zip() ✅ Tier 1
- **EP320**: Loop Variables After Loop Ends ✅ Tier 1
- **EP321**: Be Defensive when Iterating over Arguments ✅ Tier 1
- **EP317**: Comprehensive enumerate suggestions (Tier 3)
- **EP645**: yield from for Generator Composition (Tier 3)

### [Dictionary Patterns](dictionary_patterns.md)
- **EP426**: Comprehensive dict.get() patterns ✅ Tier 1
- **EP427**: defaultdict over setdefault (Tier 2)
- **EP429**: Avoid Deep Nesting → Classes (Tier 2)

## Future Rules

### Tier 2: Code Quality/API Design (v0.4.0-0.6.0) - 14 Rules
- **EP216**: Catch-All Unpacking over Slicing (Item 16, Chapter 2)
- **EP427**: defaultdict over setdefault (Item 27, Chapter 4)
- **EP12103**: deque for Producer-Consumer Queues (Item 103, Chapter 12)
- **EP531**: Return Objects vs >3 Tuple Unpacking (Item 31, Chapter 5)
- **EP538**: functools.wraps for Decorators (Item 38, Chapter 5)
- **EP429**: Avoid Deep Nesting → Classes (Item 29, Chapter 4)
- **EP537**: Keyword-Only/Positional-Only Arguments (Item 37, Chapter 5)
- **EP748**: Functions vs Classes for Simple Interfaces (Item 48, Chapter 7)
- **EP755**: Public vs Private Attributes (Item 55, Chapter 7)
- **EP769**: Use Lock to Prevent Data Races (Item 69, Chapter 9)
- **EP770**: Use Queue for Thread Coordination (Item 70, Chapter 9)
- **EP881**: assert vs raise patterns (Item 81, Chapter 10)
- **EP12121**: Root Exception Hierarchies (Item 121, Chapter 14)
- **EP12122**: Circular Dependencies (Item 122, Chapter 14)

### Tier 3: Advanced Patterns (v0.7.0+) - 6 Rules
- **EP104**: Helper Functions over Complex Expressions (Item 4, Chapter 1)
- **EP108**: Assignment Expressions for Repetition (Item 8, Chapter 1)
- **EP215**: Avoid Striding and Slicing Together (Item 15, Chapter 2)
- **EP317**: Comprehensive enumerate suggestions (Item 17, Chapter 3)
- **EP641**: Complex Comprehension Control (Item 41, Chapter 6)
- **EP645**: yield from for Generator Composition (Item 45, Chapter 6)

### Phase 4: High Performance Python Integration (v0.8.0+)
- **HP001**: String concatenation in loops → use `str.join()`
- **PC001**: List membership testing → use `set` for O(1) lookup
- **MC001**: Missing `__slots__` → memory optimization
- **NP001**: NumPy vectorization patterns

## Error Message Format

All rules follow a consistent educational format:

```
EP### Brief description of the issue
→ 'Effective Python' (3rd Edition), Item X, Chapter Y: Chapter Name
→ Impact: Specific benefit (readability/performance/bug prevention)
→ Example: before_code → after_code
```

## Book Coverage

Our 26 verified rules systematically cover:

- **Chapter 1**: Pythonic Thinking (4 rules)
- **Chapter 2**: Lists and Dictionaries (3 rules)
- **Chapter 3**: Functions (5 rules)
- **Chapter 4**: Comprehensions and Generators (4 rules)
- **Chapter 5**: Classes and Inheritance (3 rules)
- **Chapter 7**: Concurrency and Parallelism (3 rules)
- **Chapter 9**: Testing and Debugging (1 rule)
- **Chapter 10**: Collaboration (1 rule)
- **Chapter 12**: Built-in Modules (1 rule)
- **Chapter 14**: Collaboration (1 rule)

**Total: 26 implementable rules from comprehensive analysis of all 125 "Effective Python" items**

## Implementation Status

- ✅ **Documentation Complete**: All Tier 1 rules documented
- 🔄 **Implementation In Progress**: Starting with EP105
- 📋 **Planned**: Tier 2 and 3 rules for future releases

## Contributing

When documenting new rules:

1. **Follow the established format** with book references, examples, and detection criteria
2. **Include gap analysis** showing why existing tools don't cover the pattern
3. **Provide comprehensive examples** from real-world code
4. **Explain when NOT to apply** the rule (important edge cases)
5. **Link to related rules** in the same category
