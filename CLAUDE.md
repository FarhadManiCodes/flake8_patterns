# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a flake8 plugin called `flake8-patterns` (formerly `flake8-performance-patterns`) that detects performance anti-patterns in Python code. The plugin is based on patterns from two authoritative books:
- **"Effective Python" (3rd Edition)** by Brett Slatkin - **PRIMARY FOCUS**
- "High Performance Python" (3rd Edition) by Micha Gorelick and Ian Ozsvald

## Technical Requirements & Compatibility

### Python Version Support
- **Primary Target**: Python 3.10+ (modern syntax and performance features)
- **Fully Supported**: Python 3.10, 3.11, 3.12, 3.13
- **Book Alignment**: Patterns optimized for Python 3.13 features and performance characteristics
- **Legacy Support**: Python 3.8-3.9 supported with feature detection and graceful degradation

### Legacy Control Strategy
```python
# Feature detection for older Python versions
import sys
from typing import TYPE_CHECKING

PYTHON_310_PLUS = sys.version_info >= (3, 10)
PYTHON_311_PLUS = sys.version_info >= (3, 11)
PYTHON_312_PLUS = sys.version_info >= (3, 12)
PYTHON_313_PLUS = sys.version_info >= (3, 13)

# Conditional rule activation
if PYTHON_310_PLUS:
    # Enable pattern matching syntax checks
    enable_match_case_patterns()

if PYTHON_311_PLUS:
    # Enable ExceptionGroup and task group patterns
    enable_exception_group_checks()

if PYTHON_313_PLUS:
    # Enable latest performance optimizations
    enable_latest_performance_patterns()
```

### Plugin Architecture Requirements
- **Entry point**: Standard flake8 plugin registration via setuptools
- **AST-based**: Use Python's `ast` module for code analysis (3.10+ enhanced features)
- **Non-invasive**: Read-only analysis, no code modification
- **Performance**: <15% overhead on typical flake8 runs (educational plugin tolerance)
- **Memory**: <30MB additional memory usage
- **Compatibility**: Graceful degradation on Python 3.8-3.9

## Development Strategy & Priorities

### Implementation Roadmap (Effective Python First)

**Phase 1: Simple & Objective Rules (v0.1.0-0.3.0)**
- EP201: Always Surround Single-Element Tuples with Parentheses (Chapter 2)
- EP202: Prefer F-Strings over C-Style Format Strings (Chapter 2)
- EP203: Prefer Explicit String Concatenation (Chapter 2)
- EP301: Prefer enumerate over range (Chapter 3)
- EP302: Use zip to Process Iterators in Parallel (Chapter 3)
- EP303: Never Use for Loop Variables After Loop Ends (Chapter 3)
- EP304: Never Modify Containers While Iterating (Chapter 3)
- EP401: Prefer get over in and KeyError (Chapter 4)

**Phase 2: Moderate Complexity (v0.4.0-0.6.0)**
- EP601: Use Comprehensions Instead of map and filter (Chapter 6)
- EP602: Consider Generators Instead of Returning Lists (Chapter 6)
- EP1201: Prefer deque for Producer-Consumer Queues (Chapter 12)
- EP1202: Know Difference Between sort and sorted (Chapter 12)

**Phase 3: Subjective Rules (v0.7.0+)**
- EP101: Write Helper Functions Instead of Complex Expressions (Chapter 1)
- EP102: Consider Conditional Expressions for Simple Logic (Chapter 1)

### Competitive Analysis ✅ COMPLETED

**GOOD NEWS**: No existing performance-focused educational plugins found!

**Existing plugins focus on:**
- flake8-comprehensions (19 rules) - Only comprehensions/generators
- flake8-bugbear (50+ rules) - General bugs, minimal performance overlap
- flake8-simplify - Code simplification, not performance-focused
- ruff - Fast replacement, lacks educational book-based approach

**Our Unique Value:**
1. **Educational focus** - Book references + performance impact estimates
2. **Performance-specific** - Not just style or bugs
3. **Comprehensive coverage** - Both authoritative Python books
4. **Beginner-friendly** - Clear explanations with examples

## Essential Commands

### Development Setup
```bash
# Setup development environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
pip install -e ".[dev]"

# Verify installation
python scripts/verify_migration.py
flake8 --version  # Should show flake8-patterns
```

### Testing Strategy
```bash
# Run all tests (Book reference validation: Manual test cases)
pytest

# Test specific rule implementation
pytest tests/test_effective_python.py::test_ep201_single_element_tuples

# Run tests with coverage
pytest --cov=flake8_patterns

# Test the plugin on sample code
flake8 examples/bad_patterns.py

# Manual book reference validation
python scripts/validate_book_references.py
```

### Code Quality
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Run linter
ruff check src/ tests/ --fix

# Type checking
mypy src/flake8_patterns --strict

# Run pre-commit hooks
pre-commit run --all-files
```

### Plugin Development Workflow
```bash
# Test specific rule manually
python -c "
import ast
from flake8_patterns.checker import PerformanceChecker
code = '''
# EP201: Single element tuple without comma
coordinates = (42)  # Should trigger EP201
good_tuple = (42,)  # Should not trigger
'''
tree = ast.parse(code)
checker = PerformanceChecker(tree)
for error in checker.run():
    print(error)
"
```

## Architecture

### Core Components

1. **checker.py**: Main `PerformanceChecker` class that inherits from `NodeVisitorWithParents`
   - Entry point for flake8 via `flake8.extension` in pyproject.toml
   - Implements AST visitors for each rule category

2. **messages.py**: Centralized error messages with book references
   - `ALL_MESSAGES`: Dict mapping error codes to (message, book_ref, performance_impact)
   - Error categories: EP (Effective Python), HP (High Performance Python), PC (Collections), MC (Memory), NP (NumPy)

3. **utils.py**: AST analysis utilities
   - `NodeVisitorWithParents`: Base class for tracking parent nodes
   - Helper functions for AST node analysis and Python version compatibility

4. **book_refs.py**: Book reference system for educational context

### Error Code Categories & Versioning

**Semantic Versioning Strategy:**
- **0.1.0**: Initial release (EP201-EP203: String operations)
- **0.2.0**: Add loops (EP301-EP304)
- **0.3.0**: Add dictionaries (EP401)
- **0.4.0**: Add comprehensions (EP601-EP602)
- **0.8.0**: PyPI auto-publish ready
- **1.0.0**: Stable release

### Error Code Categories & Versioning

**Semantic Versioning Strategy:**
- **0.1.0**: Initial release (EP201-EP203: String operations)
- **0.2.0**: Add loops (EP301-EP304)
- **0.3.0**: Add dictionaries (EP401)
- **0.4.0**: Add comprehensions (EP601-EP602)
- **0.8.0**: PyPI auto-publish ready
- **1.0.0**: Stable release

**Error Code Format & Ranges:**
```python
# Error code format: [EP|HP|PC|MC|NP][001-999]
# EP = Effective Python patterns (PRIORITY)
# HP = High Performance Python patterns
# PC = Collection performance patterns
# MC = Memory optimization patterns
# NP = NumPy performance patterns

# Specific ranges:
EP001-EP020:  Iteration patterns (Chapter 3)
EP201-EP220:  String operations (Chapter 2)
EP301-EP320:  Loop patterns (Chapter 3)
EP401-EP420:  Dictionary patterns (Chapter 4)
EP601-EP620:  Comprehension patterns (Chapter 6)
EP1201-EP1220: Data structure patterns (Chapter 12)

HP001-HP020:  String operations (High Performance Python)
PC001-PC020:  Collection performance patterns
MC001-MC020:  Memory optimization patterns
NP001-NP020:  NumPy performance patterns
```

### Core Dependencies & Setup
```txt
# Production Dependencies
flake8 >= 7.0.0          # Latest flake8 with Python 3.13 support
typing_extensions >= 4.8.0  # Latest typing features, 3.8+ compatibility

# Development Dependencies
pytest >= 8.0.0          # Latest testing framework
pytest-cov >= 4.0.0      # Coverage reporting
mypy >= 1.8.0            # Type checking with 3.13 support
black >= 24.0.0          # Code formatting with 3.13 compatibility
isort >= 5.13.0          # Import sorting
pre-commit >= 3.6.0      # Git hooks
ruff >= 0.2.0            # Additional linting for our own code
```

### Project Structure
```
src/flake8_patterns/
├── __init__.py          # Main exports and plugin metadata
├── checker.py           # Core checker implementation
├── messages.py          # Error messages and book references
├── utils.py             # AST analysis utilities
├── book_refs.py         # Book reference system
└── rules/               # Rule implementations (expandable)
    ├── __init__.py
    ├── effective_python.py    # EP### rules (primary focus)
    └── high_performance.py    # HP### rules (secondary)
```

## Current Development Focus

### Immediate Priority: EP201 Implementation
**Rule**: Always Surround Single-Element Tuples with Parentheses
**Pattern**: `(item)` → `(item,)`
**Book Reference**: "Effective Python" (3rd Edition), Chapter 2
**Detection**: AST pattern matching for `ast.Tuple` with single element missing comma

### Testing Strategy: Manual Book Reference Validation
### Testing Strategy: Manual Book Reference Validation

**Coverage Requirements:**
- **Minimum**: 90% line coverage
- **Target**: 95% line coverage
- **Critical paths**: 100% coverage for error detection logic

**Test Categories:**
1. **Unit tests**: Individual checker methods
2. **Integration tests**: Full plugin functionality with flake8
3. **Performance tests**: Plugin overhead measurement
4. **Regression tests**: Previously fixed false positives/negatives
5. **Book reference validation**: Manual test cases for accuracy

```python
def test_ep201_book_reference():
    """EP201 should reference Chapter 2 correctly."""
    ref = get_book_reference("EP201")
    assert ref.chapter == "Chapter 2: Strings and Slicing"
    assert "Single-Element Tuples" in ref.section

def test_ep201_detection():
    """EP201 should detect single-element tuples without commas."""
    code = "coordinates = (42)"  # Missing comma
    errors = run_checker(code)
    assert len(errors) == 1
    assert "EP201" in errors[0][2]

def test_ep201_no_false_positives():
    """EP201 should not trigger on correct tuples."""
    code = "coordinates = (42,)"  # Correct comma
    errors = run_checker(code)
    assert len(errors) == 0
```

**Error Message Format:**
```python
# Template: Brief description + Book reference + Performance impact + Example
ERROR_TEMPLATE = (
    "{brief_description}"
    " → '{book_title}', {chapter_reference}"
    " → Performance: {performance_impact}"
    " → Example: {before_example} → {after_example}"
)

# Example usage:
"Single-element tuple missing comma, add trailing comma for clarity"
" → 'Effective Python' (3rd Edition), Chapter 2: Strings and Slicing"
" → Readability: Prevents confusion with grouping parentheses"
" → Example: (item) → (item,)"
```

### Performance & CI/CD

### Performance Targets by Python Version
```python
# Performance benchmarks by Python version
PERFORMANCE_TARGETS = {
    (3, 13): {"overhead": 0.05, "memory_mb": 25, "accuracy": 0.97},  # Optimized
    (3, 12): {"overhead": 0.08, "memory_mb": 28, "accuracy": 0.96},  # Good
    (3, 11): {"overhead": 0.10, "memory_mb": 30, "accuracy": 0.96},  # Good
    (3, 10): {"overhead": 0.12, "memory_mb": 30, "accuracy": 0.95},  # Acceptable
    (3, 9):  {"overhead": 0.15, "memory_mb": 35, "accuracy": 0.94},  # Legacy
    (3, 8):  {"overhead": 0.15, "memory_mb": 35, "accuracy": 0.94},  # Legacy
}
```

### Plugin Performance Requirements
- **Performance**: <15% overhead on typical flake8 runs (educational plugin tolerance)
- **Memory**: <30MB additional memory usage across all versions
- **Accuracy**: False positive rate <3% for core rules (improved with modern AST)

## File Reading & Data Analysis (Claude Code Integration)

### Reading Files
When working with uploaded files, use the `window.fs.readFile` API:
```python
# Read files programmatically
const fileContent = await window.fs.readFile('filename.py', { encoding: 'utf8' });

# Always include error handling when reading files
try:
    const content = await window.fs.readFile('test_patterns.py', { encoding: 'utf8' });
    console.log('File content:', content);
} catch (error) {
    console.error('Failed to read file:', error);
}
```

### Testing with Real Code Examples
```python
# When creating test examples or analyzing patterns
code_example = '''
# EP201: Single element tuple without comma
coordinates = (42)  # Should trigger EP201
good_tuple = (42,)  # Should not trigger

# EP301: range(len()) pattern
items = ["a", "b", "c"]
for i in range(len(items)):  # Should trigger EP301
    print(i, items[i])
'''

# Test the plugin
tree = ast.parse(code_example)
checker = PerformanceChecker(tree)
errors = list(checker.run())
```

## Performance & CI/CD

### Performance Targets
- **Plugin overhead**: <15% of flake8 runtime (educational plugin tolerance)
- **Python 3.10+**: Primary target (3.13 optimized)
- **Legacy support**: Python 3.8-3.9 with graceful degradation

### CI/CD Strategy
- **Testing**: Python 3.10, 3.11, 3.12, 3.13
- **Pre-commit**: black, isort, ruff, mypy validation
- **Integration**: Test with other flake8 plugins for conflicts
- **PyPI**: Auto-publish starting at v0.8.0 (manual until then)

### tmux Development Workflow (Max 4 panes)
```bash
# Window 1: Development
tmux new-session -d -s "flake8-dev"
tmux split-window -h    # Pane 1: vim editing
tmux split-window -v    # Pane 2: pytest --watch
tmux select-pane -t 0
tmux split-window -v    # Pane 3: flake8 testing
                        # Pane 0: git/general commands
```

## Adding New Rules

### Rule Implementation Process
1. **Choose next rule** from priority roadmap (Effective Python first, simple → complex)
2. **Add message to messages.py**: Include in appropriate category with book reference
3. **Implement detection in checker.py**: Add visitor method for AST pattern
4. **Add comprehensive tests**: Positive, negative, edge cases, book reference validation
5. **Validate book reference accuracy**: Manual test case verifying chapter/section
6. **Include educational context**: Performance/readability impact + before/after examples
7. **Test integration**: Ensure no conflicts with existing flake8 plugins

### Book Reference Requirements (CRITICAL)
All rules must include:
- Exact book title and edition
- Chapter number and title
- Specific section/item reference
- Page number (when available)
- Performance/readability impact estimate
- Before/after code examples

### Quality Standards
- **Clarity over cleverness** - Code should be self-documenting
- **Educational focus** - Comments explain the "why" behind patterns
- **Performance consciousness** - Practice what we preach
- **Type safety** - Comprehensive type hints throughout
- **No false positives** - Better to miss an issue than flag correct code
- **Book accuracy** - All references must be manually verified

## Python Version Support

- **Minimum**: Python 3.10+
- **Target**: Python 3.13 (optimized performance tier)
- **Compatibility**: Uses `sys.version_info` checks for feature detection

## Development Notes

- The plugin extends flake8's architecture following the flake8-bugbear pattern
- AST analysis uses custom `NodeVisitorWithParents` for context-aware checking
- Each rule includes educational context with book references and impact estimates
- Pre-commit hooks ensure code quality with black, isort, ruff, and mypy
- Focus on **objective, detectable patterns** first, then subjective improvements
