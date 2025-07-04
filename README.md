# flake8-patterns

> An educational flake8 plugin that detects anti-patterns based on **"Effective Python" (3rd Edition)** by Brett Slatkin, with future **"High Performance Python"** integration planned.

## 🎯 What Makes This Plugin Special

- **📚 Book-Based Rules**: Every rule references specific chapters from authoritative Python books
- **🎓 Educational Focus**: Learn best practices while you code with detailed explanations
- **📊 Impact Estimates**: Shows performance/readability improvements (e.g., "Prevents tuple confusion", "10x faster")
- **🐍 Modern Python**: Optimized for Python 3.10+ with 3.13 performance features
- **🎯 Objective Patterns**: Focuses on clear, detectable anti-patterns first
- **🚀 Complementary**: Works alongside existing flake8 plugins for comprehensive code quality

## 📖 Book-Based Learning Approach

### Current Focus: "Effective Python" (3rd Edition)
- **Primary implementation**: 26 verified rules across all chapters
- **Systematic coverage**: Based on comprehensive analysis of all 125 items
- **Educational focus**: Each rule teaches specific Pythonic patterns with book references

### Future Integration: "High Performance Python" (3rd Edition)
- **Planned for v0.8.0+**: After completing Effective Python coverage
- **Performance patterns**: Memory optimization, vectorization, profiling-based improvements
- **Complementary focus**: Performance optimization techniques beyond basic Pythonic patterns

## 🚀 Quick Start

```bash
# Install
pip install flake8-patterns

# Use with flake8
flake8 your_code.py

# Example output
your_code.py:12:5: EP105 Sequential indexing detected, use multiple-assignment unpacking
    → 'Effective Python' (3rd Edition), Item 5, Chapter 1: Pythonic Thinking
    → Readability: Cleaner, less error-prone, same performance
    → Example: x = item[0]; y = item[1] → x, y = item
```

## 🎯 Implementation Roadmap: 26 Verified Rules

*Based on comprehensive analysis of all 125 "Effective Python" items*

### Phase 1: High Impact, Clear Gaps (v0.1.0-0.3.0) - 6 Rules

**Tier 1 rules with maximum educational value and no existing tool coverage:**

- **EP105**: Multiple-Assignment Unpacking over Indexing (Item 5, Chapter 1)
  - Pattern: `x = item[0]; y = item[1]` → `x, y = item`
  - Gap: No existing tool detects sequential indexing patterns

- **EP213**: Context-Aware String Concatenation (Item 13, Chapter 2)
  - Pattern: Implicit concatenation in collections → explicit concatenation
  - Gap: flake8-implicit-str-concat lacks context awareness

- **EP318**: Parallel Iteration with zip() (Item 18, Chapter 3)
  - Pattern: `for i in range(len(names)): name=names[i]` → `zip(names, ages)`
  - Gap: No existing tool detects manual parallel iteration

- **EP320**: Loop Variables After Loop Ends (Item 20, Chapter 3)
  - Pattern: Using loop variables after loop completion
  - Gap: flake8-bugbear B023 covers closures, not direct usage

- **EP321**: Be Defensive when Iterating over Arguments (Item 21, Chapter 3)
  - Pattern: Functions iterating same parameter multiple times
  - Gap: No existing tool detects iterator exhaustion patterns

- **EP426**: Comprehensive dict.get() patterns (Item 26, Chapter 4)
  - Pattern: `try: x = d[key]; except KeyError:` → `x = d.get(key, default)`
  - Gap: flake8-simplify SIM124 covers only ~25% of patterns

### Phase 2: Code Quality/API Design (v0.4.0-0.6.0) - 14 Rules

**Medium-impact rules focusing on code quality and API design:**

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

### Phase 3: Advanced Patterns (v0.7.0+) - 6 Rules

**Lower-priority but valuable patterns:**

- **EP104**: Helper Functions over Complex Expressions (Item 4, Chapter 1)
- **EP108**: Assignment Expressions for Repetition (Item 8, Chapter 1)
- **EP215**: Avoid Striding and Slicing Together (Item 15, Chapter 2)
- **EP317**: Comprehensive enumerate suggestions (Item 17, Chapter 3)
- **EP641**: Complex Comprehension Control (Item 41, Chapter 6)
- **EP645**: yield from for Generator Composition (Item 45, Chapter 6)

### Phase 4: High Performance Python Integration (v0.8.0+)

**Future integration with "High Performance Python" patterns:**

- **HP001**: String concatenation in loops → use `str.join()`
- **PC001**: List membership testing → use `set` for O(1) lookup
- **MC001**: Missing `__slots__` → memory optimization
- **NP001**: NumPy vectorization patterns

## 💡 Before & After Examples

### EP105: Multiple-Assignment Unpacking

```python
# 🐌 Unpythonic - sequential indexing
item = (1, 2, 3)
first = item[0]
second = item[1]

# ⚡ Pythonic - multiple-assignment unpacking
first, second, third = item
```

## ⚙️ Configuration

Add to your `setup.cfg` or `pyproject.toml`:

```ini
[flake8]
# Enable Effective Python rules (recommended)
select = E,W,F,EP

# Focus on Tier 1 high-impact rules
select = EP105,EP213,EP318,EP320,EP321,EP426

# Educational mode (all implemented rules)
extend-select = EP

# Combine with existing tools (recommended)
extend-select = B,C4,EP  # bugbear + comprehensions + educational
```

## 🤝 Competitive Analysis: No Conflicts Found

**flake8-patterns fills genuine gaps in the Python linting ecosystem.**

### Comprehensive Analysis Against Existing Tools

**We systematically analyzed our 26 rules against all major linting tools:**
- `flake8-bugbear` (50+ rules) - Focuses on bugs/design problems
- `flake8-comprehensions` (19 rules) - Optimizes comprehensions/generators
- `flake8-simplify` (100+ rules) - Code simplification patterns
- `ruff` (500+ rules) - Comprehensive fast linter
- `pylint`, `perflint`, and others

### ✅ Verified No Conflicts

**Our Tier 1 rules address genuine gaps:**
- **EP105**: No existing tool detects sequential indexing patterns
- **EP213**: flake8-implicit-str-concat lacks context awareness
- **EP318**: No tool detects manual parallel iteration
- **EP320**: flake8-bugbear B023 covers closures, not direct usage
- **EP321**: No tool detects iterator exhaustion patterns
- **EP426**: flake8-simplify SIM124 covers only ~25% of dict.get patterns

### Our Educational Niche: Book-Based Learning

| **Aspect** | **flake8-patterns** | **Existing Tools** |
|------------|---------------------|--------------------|
| **Focus** | 📚 Educational patterns from authoritative books | ⚙️ Production bug prevention |
| **Error Messages** | 📚 Book references + impact + examples | 🚀 Concise problem descriptions |
| **Coverage** | 🎯 26 verified gaps in mature ecosystem | 🔧 500+ comprehensive rules |
| **Audience** | 🎓 Developers learning Pythonic patterns | 👨‍💻 Production codebases |
| **Purpose** | 📚 Study guide with book chapters | ✅ Core linting foundation |

### Perfect Complement, Not Replacement

```bash
# Recommended: Use flake8-patterns WITH mature tools
pip install flake8-bugbear flake8-comprehensions  # Core foundation
pip install flake8-patterns                       # Educational layer

# Your .flake8 config:
[flake8]
extend-select = B,C4,EP  # Bugbear + Comprehensions + Educational patterns
```

**Think of flake8-patterns as:** A study guide that points you to "Effective Python" chapters while you code.

## 🔧 Development Setup

```bash
# Clone and setup
git clone https://github.com/FarhadManiCodes/flake8-patterns.git
cd flake8-patterns

# Create virtual environment (Python 3.10+ recommended)
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install in development mode
pip install -e ".[dev]"

# Verify installation
flake8 --version  # Should show flake8-patterns
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Test with coverage
pytest --cov=flake8_patterns

# Test specific rule category
pytest tests/test_effective_python.py

# Manual testing
flake8 examples/bad_patterns.py

# Book reference validation
python scripts/validate_book_references.py
```

## 📊 Performance & Compatibility

### Python Version Support
- **Minimum**: Python 3.10+
- **Recommended**: Python 3.13 (optimized performance)
- **Legacy**: Python 3.8-3.9 with graceful degradation

### Performance Targets
- **Plugin overhead**: <15% of flake8 runtime (educational plugin tolerance)
- **Memory usage**: <30MB additional
- **False positive rate**: <3% for core rules

## 🗺️ Roadmap

### Current Status: v0.1.0-dev
- ✅ **Comprehensive analysis** of all 125 "Effective Python" items completed
- ✅ **26 verified rules** identified across 3 implementation tiers
- ✅ **Book reference system** implemented with correct Item/Chapter mappings
- ✅ **Testing framework** with manual validation
- ✅ **Competitive analysis** completed (no conflicts found)
- 🔄 **EP105 implementation** in progress (current priority)

### Upcoming Releases

**v0.1.0-0.3.0** - Tier 1: High Impact Rules (6 rules)
- EP105: Multiple-Assignment Unpacking over Indexing
- EP213: Context-Aware String Concatenation
- EP318: Parallel Iteration with zip()
- EP320: Loop Variables After Loop Ends
- EP321: Be Defensive when Iterating over Arguments
- EP426: Comprehensive dict.get() patterns

**v0.4.0-0.6.0** - Tier 2: Code Quality/API Design (14 rules)
- EP216, EP427, EP12103, EP531, EP538, EP429, EP537, EP748, EP755, EP769, EP770, EP881, EP12121, EP12122
- Focus on API design and code quality patterns

**v0.7.0+** - Tier 3: Advanced Patterns (6 rules)
- EP104, EP108, EP215, EP317, EP641, EP645
- Complete "Effective Python" coverage (26 total rules)

**v0.8.0+** - High Performance Python Integration
- HP001: String concatenation patterns
- PC001: Collection performance patterns
- MC001: Memory optimization patterns
- NP001: NumPy vectorization patterns

**v1.0.0** - Stable Release
- All 26 "Effective Python" rules implemented
- Initial "High Performance Python" coverage
- Production-ready performance
- Comprehensive documentation

## 🤝 Contributing

We welcome contributions! Here's how to help:

### Adding New Rules
1. **Choose from roadmap** - Priority: simple → complex, early chapters first
2. **Verify book reference** - Must cite actual chapter/page/item
3. **Implement AST detection** - Follow existing patterns
4. **Write comprehensive tests** - Positive, negative, edge cases
5. **Add educational context** - Before/after examples + impact

### Book Reference Validation
```python
def test_ep105_book_reference():
    """Ensure EP105 cites correct book section."""
    ref = get_book_reference("EP105")
    assert ref.book == "Effective Python"
    assert ref.chapter == "Chapter 1: Pythonic Thinking"
    assert "Multiple-Assignment Unpacking" in ref.section
```

### Development Guidelines
- **Manual book validation** - No automated book scraping
- **No false positives** - Better to miss than incorrectly flag
- **Educational first** - Clear explanations over clever detection
- **Test coverage** - 90% minimum, 95% target

## 📄 License

This project is licensed under the MIT License.

Copyright (c) 2025 Farhad Mani (frhdmani@gmail.com - GitHub: FarhadManiCodes)

See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Brett Slatkin** for "Effective Python" (3rd Edition) - authoritative guide to Pythonic patterns
- **Micha Gorelick & Ian Ozsvald** for "High Performance Python" (3rd Edition) - essential performance reference
- The **flake8** community for creating an extensible linting framework
- **Python community** for continuous language improvements and best practices

## 📘 Book References Disclaimer

This project includes optional references to well-known programming books —
_Effective Python (3rd Edition)_, _High Performance Python (3rd Edition)_, and _Fluent Python_ —
within code comments to encourage best practices and support educational use.
These references are provided solely for informational purposes and do **not** imply any affiliation, endorsement, or sponsorship by the authors or publishers of these books.
*"Effective Python" provides the foundation with 26 verified rules, with "High Performance Python" integration planned for v0.8.0+.*

## 📚 Educational Resources

- [Rule Documentation](docs/rules/) - Detailed explanations with examples
