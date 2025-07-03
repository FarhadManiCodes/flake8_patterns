# flake8-patterns

> A comprehensive flake8 plugin that detects performance and readability anti-patterns based on **"Effective Python"** and **"High Performance Python"**.

## 🎯 What Makes This Plugin Special

- **📚 Book-Based Rules**: Every rule references specific chapters from authoritative Python books
- **🎓 Educational Focus**: Learn best practices while you code with detailed explanations
- **📊 Impact Estimates**: Shows performance/readability improvements (e.g., "Prevents tuple confusion", "10x faster")
- **🐍 Modern Python**: Optimized for Python 3.10+ with 3.13 performance features
- **🎯 Objective Patterns**: Focuses on clear, detectable anti-patterns first
- **🚀 Complementary**: Works alongside existing flake8 plugins for comprehensive code quality

## 📖 Supported Books (Equal Focus)

- **"Effective Python" (3rd Edition)** by Brett Slatkin
- **"High Performance Python" (3rd Edition)** by Micha Gorelick and Ian Ozsvald

*Note: We're starting implementation with Effective Python patterns as they tend to be more objective and easier to detect, but both books are equally important to the project's goals.*

## 🚀 Quick Start

```bash
# Install
pip install flake8-patterns

# Use with flake8
flake8 your_code.py

# Example output
your_code.py:3:5: EP201 Single-element tuple missing comma, add trailing comma for clarity
    → 'Effective Python' (3rd Edition), Chapter 2: Strings and Slicing
    → Readability: Prevents confusion with grouping parentheses
    → Example: (item) → (item,)
```

## 🔍 Error Codes & Implementation Roadmap

### Phase 1: Simple & Objective Rules ✅ (v0.1.0-0.3.0)

#### String Operations (Chapter 2)
- **EP201**: Single-element tuple missing comma → `(item,)`
- **EP202**: C-style string formatting → use f-strings
- **EP203**: Implicit string concatenation in collections → explicit concatenation

#### Loop Patterns (Chapter 3)
- **EP301**: `range(len())` pattern → use `enumerate()`
- **EP302**: Manual parallel iteration → use `zip()`
- **EP303**: Loop variable used after loop → avoid scope leakage
- **EP304**: Container modification during iteration → use copies

#### Dictionary Operations (Chapter 4)
- **EP401**: `in` check + `KeyError` handling → use `dict.get()`

### Phase 2: Moderate Complexity (v0.4.0-0.6.0)

#### Comprehensions & Generators (Chapter 6)
- **EP601**: `map`/`filter` with lambda → use comprehensions
- **EP602**: Large list comprehensions → use generators

#### Data Structures (Chapter 12)
- **EP1201**: List as queue → use `collections.deque`
- **EP1202**: `sort()` vs `sorted()` confusion → correct usage

### Phase 3: High Performance Python Integration (v0.7.0+)

#### High Performance Python Patterns
- **HP001**: String concatenation in loops → use `str.join()`
- **PC001**: List membership testing → use `set` for O(1) lookup
- **MC001**: Missing `__slots__` → memory optimization

### Phase 4: Advanced Patterns (v0.8.0+)

#### Advanced Effective Python
- **EP101**: Helper functions over complex expressions
- **EP102**: Conditional expressions for simple logic

#### Advanced High Performance Python
- **HP010-HP020**: Advanced performance optimization patterns
- **NP001-NP010**: NumPy vectorization patterns

### Legacy Rules (Maintained for Compatibility)
- **EP001**: `range(len())` pattern (legacy code from EP301)

## 💡 Before & After Examples

### EP201: Single-Element Tuples

```python
# 🐌 Confusing - looks like grouping parentheses
coordinates = (42)
type(coordinates)  # <class 'int'> - NOT a tuple!

# ⚡ Clear - explicitly a tuple
coordinates = (42,)
type(coordinates)  # <class 'tuple'> - correct!
```

### EP301: Iteration Patterns

```python
# 🐌 Unpythonic
items = ['a', 'b', 'c']
for i in range(len(items)):  # EP301
    print(i, items[i])

# ⚡ Pythonic
for i, item in enumerate(items):
    print(i, item)
```

### EP401: Dictionary Access

```python
# 🐌 Error-prone
try:
    value = my_dict[key]  # EP401
except KeyError:
    value = default

# ⚡ Clean and efficient
value = my_dict.get(key, default)
```

## ⚙️ Configuration

Add to your `setup.cfg` or `pyproject.toml`:

```ini
[flake8]
# Enable Effective Python rules (recommended)
select = E,W,F,EP

# Focus on specific categories
select = EP201,EP301,EP401  # String, loops, dicts

# High-impact performance rules
select = EP,HP,PC

# Educational mode (all rules with examples)
extend-select = EP,HP,PC,MC
```

## 🤝 Relationship with Existing Tools

**flake8-patterns is designed to complement, not replace, mature linting tools.**

### Established & Battle-Tested Tools (Use These First!)

- **flake8-bugbear** 🐛 - Mature plugin with 50+ rules for catching likely bugs and design problems
- **flake8-comprehensions** ⚡ - Excellent 19 rules for optimizing comprehensions and generators
- **ruff** 🚀 - Lightning-fast modern linter replacing many flake8 plugins with superior performance
- **flake8-simplify** 🧹 - Code simplification patterns with proven track record

### Our Educational Niche 📚

**flake8-patterns** fills a specific gap: **book-based learning while coding**

| Aspect | flake8-patterns | Mature Tools |
|--------|-----------------|--------------|
| **Primary purpose** | 📖 Educational (learning tool) | ⚙️ Production (bug prevention) |
| **Rule maturity** | 🌱 Early development | 🎯 Battle-tested, stable |
| **Performance focus** | 📚 Book-referenced patterns | 🚀 Comprehensive coverage |
| **Target audience** | 🎓 Developers learning best practices | 👨‍💻 Production codebases |
| **Usage recommendation** | 🧂 With grain of salt, alongside others | ✅ Core linting foundation |

### No Conflicts by Design ✅

I **intentionally avoided** overlapping with existing tools:
- **flake8-bugbear**: Focuses on bugs/design problems → We focus on book patterns
- **flake8-comprehensions**: Covers comprehensions/generators → We focus on broader patterns
- **ruff**: Speed & comprehensive coverage → We focus on educational explanations
- **Different error codes**: EP/HP prefixes vs. B/C/etc to avoid conflicts

### Recommended Usage 🎯

```bash
# Recommended: Use flake8-patterns WITH mature tools
pip install flake8-bugbear flake8-comprehensions  # Core foundation
pip install flake8-patterns                       # Educational layer

# Your .flake8 config:
[flake8]
extend-select = B,C4,EP  # Bugbear + Comprehensions + Educational patterns
```

**Think of flake8-patterns as:** A study guide that points you to book chapters while you code, not a replacement for proven production linters.

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
- ✅ **Project structure** established
- ✅ **Book reference system** implemented
- ✅ **Testing framework** with manual validation
- ✅ **Competitive analysis** completed (no conflicts found)
- 🔄 **EP201 implementation** in progress

### Upcoming Releases

**v0.1.0** (Next) - Foundation
- EP201: Single-element tuples
- EP202: F-strings over C-style formatting
- EP203: Explicit string concatenation

**v0.2.0** - Loop Patterns
- EP301: enumerate over range(len)
- EP302: zip for parallel iteration
- EP303: Loop variable scope
- EP304: Safe container iteration

**v0.3.0** - Dictionary Patterns
- EP401: dict.get() over KeyError
- Enhanced book reference integration

**v0.7.0** - High Performance Python Integration
- HP001: String concatenation patterns
- PC001: Collection performance patterns
- Book balance: Equal coverage of both sources

**v0.8.0** - PyPI Auto-publish Ready
- 20+ rules from both books
- Comprehensive documentation
- Performance benchmarking
- CI/CD pipeline complete

**v1.0.0** - Stable Release
- Comprehensive coverage of both books
- Production-ready performance
- IDE integrations

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
def test_ep201_book_reference():
    """Ensure EP201 cites correct book section."""
    ref = get_book_reference("EP201")
    assert ref.book == "Effective Python"
    assert ref.chapter == "Chapter 2: Strings and Slicing"
    assert "Single-Element Tuples" in ref.section
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

*Both books are equally valuable to this project - we're just starting with one for practical implementation reasons.*

## 📚 Educational Resources

- [Rule Documentation](docs/rules/) - Detailed explanations with examples
