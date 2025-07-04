# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a flake8 plugin called `flake8-patterns` that detects anti-patterns in Python code based on patterns from authoritative books:
- **"Effective Python" (3rd Edition)** by Brett Slatkin (PRIMARY FOCUS)
- "High Performance Python" (3rd Edition) by Micha Gorelick and Ian Ozsvald (FUTURE)

**Current Status**: Implementing Effective Python patterns first (26 verified rules across 3 tiers), with High Performance Python integration planned for later phases.

**Licence Requirement**: All example code files and test cases that contain patterns inspired by Effective Python must include the following header at the top:
```python
# This code is inspired by examples from Brett Slatkin’s
# Effective Python repository, licensed under Apache 2.0.
```
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

### Implementation Roadmap (Verified 26 Rules)

*Based on comprehensive analysis of all 125 Effective Python items. Starting with Tier 1 rules that have the highest impact and clearest detection patterns.*

**Phase 1: High Impact, Clear Gaps (v0.1.1-0.3.0) - 6 Rules**
- EP105: Multiple-Assignment Unpacking over Indexing (Item 5, Chapter 1)
- EP213: Context-Aware String Concatenation (Item 13, Chapter 2)
- EP318: Parallel Iteration with zip() (Item 18, Chapter 3)
- EP320: Loop Variables After Loop Ends (Item 20, Chapter 3)
- EP321: Be Defensive when Iterating over Arguments (Item 21, Chapter 3)
- EP426: Comprehensive dict.get() patterns (Item 26, Chapter 4)

**Phase 2: Code Quality/API Design (v0.4.0-0.6.0) - 14 Rules**
- EP216: Catch-All Unpacking over Slicing (Item 16, Chapter 2)
- EP427: defaultdict over setdefault (Item 27, Chapter 4)
- EP12103: deque for Producer-Consumer Queues (Item 103, Chapter 12)
- EP531: Return Objects vs >3 Tuple Unpacking (Item 31, Chapter 5)
- EP538: functools.wraps for Decorators (Item 38, Chapter 5)
- EP429: Avoid Deep Nesting → Classes (Item 29, Chapter 4)
- EP537: Keyword-Only/Positional-Only Arguments (Item 37, Chapter 5)
- EP748: Functions vs Classes for Simple Interfaces (Item 48, Chapter 7)
- EP755: Public vs Private Attributes (Item 55, Chapter 7)
- EP769: Use Lock to Prevent Data Races (Item 69, Chapter 9)
- EP770: Use Queue for Thread Coordination (Item 70, Chapter 9)
- EP881: assert vs raise patterns (Item 81, Chapter 10)
- EP12121: Root Exception Hierarchies (Item 121, Chapter 14)
- EP12122: Circular Dependencies (Item 122, Chapter 14)

**Phase 3: Advanced Patterns (v0.7.0+) - 6 Rules**
- EP104: Helper Functions over Complex Expressions (Item 4, Chapter 1)
- EP108: Assignment Expressions for Repetition (Item 8, Chapter 1)
- EP215: Avoid Striding and Slicing Together (Item 15, Chapter 2)
- EP317: Comprehensive enumerate suggestions (Item 17, Chapter 3)
- EP641: Complex Comprehension Control (Item 41, Chapter 6)
- EP645: yield from for Generator Composition (Item 45, Chapter 6)

**Phase 4: High Performance Python Integration (v0.8.0+)**
- HP001: String concatenation in loops → use `str.join()`
- PC001: List membership testing → use `set` for O(1) lookup
- MC001: Missing `__slots__` → memory optimization
- NP001: Manual loops over arrays → use NumPy vectorization

### Competitive Analysis ✅ VERIFIED COMPLETE

**CONFIRMED**: No existing educational plugins with book-based rules found!

**Existing tools cover different areas:**
- flake8-comprehensions (19 rules) - Only comprehensions/generators
- flake8-bugbear (50+ rules) - General bugs, minimal overlap with our patterns
- flake8-simplify - Code simplification, not book-based education
- ruff - Fast replacement, lacks educational book references

**Our Unique Value:**
1. **Educational focus** - Book references + learning-oriented error messages
2. **Comprehensive book coverage** - Systematic implementation of authoritative patterns
3. **No conflicts** - Verified compatibility with existing flake8 ecosystem
4. **Clear pedagogy** - Each rule teaches specific Pythonic patterns with examples

## Using Gemini CLI for Large Codebase Analysis

When analyzing the entire flake8-patterns codebase or verifying project-wide patterns, use Gemini CLI with its massive context window and structured thinking protocols.

### MCP Sequential Thinking Integration

For complex analysis tasks, structure your thinking process:

```json
{
  "thought": "Analyzing EP105 implementation across all files to ensure consistency",
  "thoughtNumber": 1,
  "totalThoughts": 5,
  "nextThoughtNeeded": true,
  "context": "Reviewing checker.py, messages.py, tests, and examples for EP105"
}
```

**Use Sequential Thinking for:**
- 🧠 **Rule implementation planning** - Multi-step AST visitor design
- 🔍 **Cross-file consistency analysis** - Pattern verification across codebase
- 📚 **Book reference validation** - Ensuring accuracy across all citations
- 🏗️ **Architecture decisions** - Plugin structure and design choices
- ⚡ **Performance impact analysis** - System-wide performance considerations

### When to Use Gemini CLI vs Claude

**Use Gemini CLI (`gemini -p`) for:**
- 🔍 **Project-wide analysis** - Architecture reviews, pattern consistency
- 📊 **Integration verification** - Checking conflicts with other flake8 plugins
- 🧪 **Test coverage analysis** - Comprehensive testing verification
- 📚 **Book reference validation** - Ensuring all rules cite correct chapters
- 🏗️ **Large file analysis** - When multiple files exceed Claude's context
- 🔄 **Refactoring identification** - Simple improvements across multiple files

**Use Claude for:**
- 🎯 **Implementation decisions** - New rules, AST logic, architecture
- 🧠 **Complex reasoning** - Rule prioritization, design choices
- ✍️ **Detailed coding** - Writing visitor methods, error detection logic
- 📖 **Educational content** - Book reference accuracy, example creation
- 🎓 **Strategic planning** - Project roadmap and rule prioritization

### Context Management

The project uses a single GEMINI.md file for project-wide context:

```
flake8-patterns/
├── GEMINI.md                    # Project guidelines (Gemini-specific)
├── CLAUDE.md                    # Development guidance (Claude-specific)
├── README.md                    # User documentation
└── src/flake8_patterns/         # Implementation code
```

**Note**: Unlike some projects that use hierarchical GEMINI.md files in subdirectories, flake8-patterns uses a single root-level GEMINI.md for simplicity. All project context and guidelines are consolidated in this file.

### File Analysis Examples for flake8-patterns

**Project structure overview:**
```bash
gemini -p "@./ Give me an overview of the flake8-patterns project structure and architecture"
```

**Rule consistency check:**
```bash
gemini -p "@src/ @tests/ Are all EP### rules properly implemented with corresponding tests?"
```

**Book reference validation:**
```bash
gemini -p "@src/messages.py @src/book_refs.py Are all error codes properly linked to book chapters?"
```

**Integration conflict check:**
```bash
gemini -p "@src/ Does flake8-patterns have any error code conflicts with flake8-bugbear or flake8-comprehensions?"
```

**Test coverage analysis:**
```bash
gemini -p "@tests/ @examples/ Which rules lack comprehensive test cases or examples?"
```

**Message format consistency:**
```bash
gemini -p "@src/messages.py Are all error messages following the same format template?"
```

### Implementation Verification Commands

**Check EP105 implementation:**
```bash
gemini -p "@src/ @tests/ Is EP105 (multiple-assignment unpacking) fully implemented with tests and examples?"
```

**Verify book accuracy:**
```bash
gemini -p "@src/book_refs.py Do all Effective Python references cite real Item numbers and chapters?"
```

**Pattern detection verification:**
```bash
gemini -p "@src/checker.py @tests/ Are AST visitor methods properly handling edge cases?"
```

**Performance impact verification:**
```bash
gemini -p "@src/messages.py @examples/ Are our readability/performance claims accurate and well-demonstrated?"
```

**Error message quality assessment:**
```bash
gemini -p "@src/messages.py Are our educational explanations clear and helpful for learning Python best practices?"
```

**Documentation consistency check:**
```bash
gemini -p "@README.md @examples/ @src/ Do README examples match actual implemented rules and error codes?"
```

**Code quality and refactoring analysis:**
```bash
gemini -p "@src/ Identify areas for simple refactoring to improve code consistency and readability"
```

### Development Safety & Checkpointing

**Safe Development Protocol:**
1. **Before major changes**: Create manual checkpoint
2. **During implementation**: Enable automatic checkpointing
3. **After completion**: Verify changes and create tagged checkpoint

**Checkpointing Commands:**
```bash
# Enable checkpointing for session
gemini --checkpointing

# Manual checkpoint before major changes
/checkpoint save "before-EP105-implementation"

# Restore if needed
/restore <checkpoint-id>

# List available checkpoints
/restore
```

**Git Integration:**
- **Shadow repository**: Checkpoints stored in ~/.gemini/history/flake8-patterns_hash
- **No interference**: Main git repository remains clean
- **Full context**: Conversation history + file state + tool calls preserved
- **Easy rollback**: Complete state restoration with one command

### Most Valuable Analysis Types for flake8-patterns

**Priority 1 (Critical for Educational Plugin):**
- 📚 **Book reference validation** - Accuracy is essential for credibility
- 🎓 **Error message quality** - Core to our educational mission
- 📋 **Rule consistency** - Professional appearance and user trust

**Priority 2 (Quality Assurance):**
- 🧪 **Test coverage analysis** - Ensures reliable rule detection
- 📊 **Documentation consistency** - User experience and adoption
- ⚡ **Impact claims verification** - Backing up our readability/performance estimates

**Priority 3 (Development Efficiency):**
- 🔍 **Integration conflict detection** - Prevents ecosystem problems
- 🏗️ **Refactoring opportunities** - Code maintainability
- 📐 **Architecture consistency** - Long-term project health

## MCP Sequential Thinking for Implementation

For complex rule implementation and architectural decisions, use structured thinking protocols.

### When to Use Sequential Thinking

**Always use for:**
- 🧠 **New rule implementation** (EP105, EP213, etc.)
- 🏗️ **AST visitor design** (complex pattern detection)
- 📚 **Book reference validation** (accuracy critical)
- ⚡ **Performance optimization** (system-wide impact)
- 🔧 **Plugin architecture changes** (affects multiple components)

### Structured Implementation Protocol

```json
// Example: Implementing EP105 (Multiple-Assignment Unpacking)
{
  "thought": "Analyzing EP105 requirements: detect x = item[0]; y = item[1] patterns",
  "thoughtNumber": 1,
  "totalThoughts": 6,
  "nextThoughtNeeded": true,
  "context": "Effective Python Item 5, Chapter 1, AST assignment analysis needed"
}

{
  "thought": "Need to examine existing AST visitor patterns in checker.py for consistency",
  "thoughtNumber": 2,
  "totalThoughts": 6,
  "nextThoughtNeeded": true,
  "context": "visit_For, visit_BinOp patterns as reference"
}

{
  "thought": "Implementation plan: 1) Add visit_Assign method 2) Track sequential indexing 3) Detect patterns like x=item[0], y=item[1] 4) Add EP105 to messages.py",
  "thoughtNumber": 3,
  "totalThoughts": 6,
  "nextThoughtNeeded": true
}

{
  "thought": "Book reference verification: Effective Python Item 5, Chapter 1 discusses unpacking benefits",
  "thoughtNumber": 4,
  "totalThoughts": 6,
  "nextThoughtNeeded": true,
  "context": "Must cite exact Item and chapter"
}

{
  "thought": "Test strategy: positive cases (sequential indexing), negative cases (non-sequential), edge cases (different variables)",
  "thoughtNumber": 5,
  "totalThoughts": 6,
  "nextThoughtNeeded": true
}

{
  "thought": "Ready to implement with clear plan, book reference verified, test strategy defined",
  "thoughtNumber": 6,
  "totalThoughts": 6,
  "nextThoughtNeeded": false
}
```

### Implementation Quality Gates

**Before coding:**
- ✅ Book reference verified (manual check)
- ✅ AST pattern understood (examine similar rules)
- ✅ Test cases planned (positive/negative/edge)
- ✅ Error message format consistent
- ✅ No conflicts with existing plugins

**During implementation:**
- ✅ Sequential thinking documented
- ✅ Code follows existing patterns
- ✅ Type hints comprehensive
- ✅ Docstrings include book references
- ✅ Tests written before/during coding

**After implementation:**
- ✅ All tests pass
- ✅ Book reference accurate
- ✅ Error message educational
- ✅ Integration with flake8 verified
- ✅ Performance impact acceptable

## Configuration Management & Tool Integration

### Environment Configuration Hierarchy

**Precedence Order (highest to lowest):**
1. **Command-line arguments** - Immediate overrides
2. **Project environment** - `.gemini/.env` in project root
3. **Global environment** - `~/.env` in home directory
4. **Default values** - Hardcoded fallbacks

```bash
# Project-specific settings (.gemini/.env)
PYTHON_VERSION=3.13
COVERAGE_TARGET=95
BOOK_VALIDATION=strict
PERFORMANCE_THRESHOLD=0.15

# Global development settings (~/.env)
GEMINI_API_KEY=your_api_key_here
DEVELOPMENT_MODE=true
LOG_LEVEL=INFO
```

### Tool Integration Configuration

```json
// .gemini/settings.json - Project configuration
{
  "checkpointing": true,
  "contextFileName": "GEMINI.md",
  "mcpServers": {
    "flake8-analyzer": {
      "command": "python",
      "args": ["scripts/analyze_rules.py"],
      "cwd": "./tools",
      "timeout": 10000,
      "trust": false
    },
    "book-validator": {
      "command": "python",
      "args": ["scripts/validate_references.py"],
      "cwd": "./tools",
      "timeout": 5000,
      "trust": true
    }
  },
  "allowedTools": ["ReadFile", "Edit", "TestExecutor", "Linter"],
  "restrictedTools": ["WriteFile", "GitPush", "WebFetch"]
}
```

### Development Workflow Integration

**Session Management:**
```bash
# Start development session with checkpointing
gemini --checkpointing

# Load project context automatically
# (GEMINI.md files are loaded hierarchically)

# Create checkpoint before major changes
/checkpoint save "before-EP105-visitor-implementation"

# Use MCP tools for analysis
/tools show  # List available analysis tools
```

**Safe Development Protocol:**
1. **Project analysis** - Use Gemini CLI for codebase review
2. **Planning** - Apply sequential thinking for complex tasks
3. **Implementation** - Use checkpointing for safety
4. **Verification** - Run comprehensive tests and validation
5. **Documentation** - Update context files and examples

## Essential Commands

### Development Setup
```bash
# Setup development environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
pip install -e ".[dev]"

# Verify installation
python scripts/verify_installation.py
flake8 --version  # Should show flake8-patterns
```

### Testing Strategy
```bash
# Run all tests (Book reference validation: Manual test cases)
pytest

# Test specific rule implementation
pytest tests/test_effective_python.py::test_ep105_multiple_assignment_unpacking

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
from flake8_patterns.checker import PatternChecker
code = '''
# EP105: Sequential indexing pattern
item = (1, 2, 3)
first = item[0]   # Should trigger EP105
second = item[1]  # Part of pattern

# Good: Multiple assignment unpacking
first, second, third = item
'''
tree = ast.parse(code)
checker = PatternChecker(tree)
for error in checker.run():
    print(error)
"
```

## Architecture

### Core Components

1. **checker.py**: Main `PatternChecker` class that inherits from `NodeVisitorWithParents`
   - Entry point for flake8 via `flake8.extension` in pyproject.toml
   - Implements AST visitors for each rule category

2. **messages.py**: Centralized error messages with book references
   - `ALL_MESSAGES`: Dict mapping error codes to (message, book_ref, impact)
   - Error categories: EP (Effective Python), HP (High Performance Python - future)

3. **utils.py**: AST analysis utilities
   - `NodeVisitorWithParents`: Base class for tracking parent nodes
   - Helper functions for AST node analysis and Python version compatibility

4. **book_refs.py**: Book reference system for educational context

### Error Code System

**Error Code Format:**
```python
# Format: EP{ItemNumber} (based on actual Effective Python Item numbers)
EP105   # Item 5: Multiple-Assignment Unpacking over Indexing
EP213   # Item 13: Prefer Explicit String Concatenation
EP318   # Item 18: Use zip to Process Iterators in Parallel
EP320   # Item 20: Never Use for Loop Variables After the Loop Ends
EP321   # Item 21: Be Defensive when Iterating over Arguments
EP426   # Item 26: Prefer get over in and KeyError

# Future High Performance Python rules will use HP prefix:
HP001-HP999   # High Performance Python patterns
PC001-PC999   # Collection performance patterns
MC001-MC999   # Memory optimization patterns
NP001-NP999   # NumPy performance patterns
```

### Semantic Versioning Strategy
- **0.1.1**: Consistency and compatibility fixes (PatternChecker naming, pre-commit fixes)
- **0.1.0**: Initial release (6 Tier 1 rules: EP105, EP213, EP318, EP320, EP321, EP426)
- **0.2.0**: Add Tier 2 rules (code quality/API design patterns)
- **0.3.0**: Complete Effective Python coverage (all 26 verified rules)
- **0.7.0**: High Performance Python integration begins
- **1.0.0**: Stable release with comprehensive book coverage

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
    ├── effective_python.py    # EP### rules (current focus)
    └── high_performance.py    # HP### rules (future)
```

## Current Development Focus

### Immediate Priority: EP105 Implementation
**Rule**: Multiple-Assignment Unpacking over Indexing
**Pattern**: `x = item[0]; y = item[1]` → `x, y = item`
**Book Reference**: "Effective Python" (3rd Edition), Item 5, Chapter 1
**Detection**: AST pattern matching for sequential indexing assignments

**Why EP105 First:**
- Clearest, most detectable pattern (high confidence implementation)
- Common anti-pattern that beginners often use
- Clear educational value with obvious improvement
- No complex AST analysis required (good starting point)

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
def test_ep105_book_reference():
    """EP105 should reference Item 5, Chapter 1 correctly."""
    ref = get_book_reference("EP105")
    assert ref.item == "Item 5"
    assert ref.chapter == "Chapter 1: Pythonic Thinking"
    assert "Multiple-Assignment Unpacking" in ref.section

def test_ep105_detection():
    """EP105 should detect sequential indexing patterns."""
    code = '''
item = (1, 2, 3)
first = item[0]   # Should trigger EP105
second = item[1]  # Part of pattern
'''
    errors = run_checker(code)
    assert len(errors) == 1
    assert "EP105" in errors[0][2]

def test_ep105_no_false_positives():
    """EP105 should not trigger on correct unpacking."""
    code = "first, second, third = item"
    errors = run_checker(code)
    assert len(errors) == 0
```

**Error Message Format:**
```python
# Template: Brief description + Book reference + Impact + Example
ERROR_TEMPLATE = (
    "{brief_description}"
    " → '{book_title}', {item_reference}, {chapter_reference}"
    " → Impact: {impact_description}"
    " → Example: {before_example} → {after_example}"
)

# Example usage:
"Sequential indexing detected, use multiple-assignment unpacking"
" → 'Effective Python' (3rd Edition), Item 5, Chapter 1: Pythonic Thinking"
" → Readability: Cleaner, less error-prone, same performance"
" → Example: x = item[0]; y = item[1] → x, y = item"
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
try {
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
# EP105: Sequential indexing pattern
item = (1, 2, 3)
first = item[0]   # Should trigger EP105
second = item[1]  # Part of pattern

# EP318: Manual parallel iteration
names = ["Alice", "Bob"]
ages = [25, 30]
for i in range(len(names)):  # Should trigger EP318
    name = names[i]
    age = ages[i]
    print(f"{name} is {age}")

# Good patterns:
first, second, third = item
for name, age in zip(names, ages):
    print(f"{name} is {age}")
'''

# Test the plugin
tree = ast.parse(code_example)
checker = PatternChecker(tree)
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

## Adding New Rules

### Rule Implementation Process
1. **Choose next rule** from verified 26-rule roadmap (follow 3-tier priority)
2. **Add message to messages.py**: Include with book reference and impact
3. **Implement detection in checker.py**: Add visitor method for AST pattern
4. **Add comprehensive tests**: Positive, negative, edge cases, book reference validation
5. **Validate book reference accuracy**: Manual test case verifying Item/chapter
6. **Include educational context**: Impact estimate + before/after examples
7. **Test integration**: Ensure no conflicts with existing flake8 plugins

### Book Reference Requirements (CRITICAL)
All rules must include:
- Exact book title and edition
- Item number and title (e.g., "Item 5: Multiple-Assignment Unpacking")
- Chapter number and title
- Specific section reference
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
- Focus on **verified, detectable patterns** from our comprehensive analysis
- **26 total rules** across 3 tiers, starting with 6 high-impact Tier 1 rules

**License Requirement**:
All example code files and test cases that contain patterns inspired by either *Effective Python* or *High Performance Python (3rd Edition)* must include the appropriate header at the top.

### For examples inspired by *Effective Python*:
```python
# This code is inspired by examples from Brett Slatkin’s
# Effective Python repository, licensed under Apache 2.0.
```


### For examples inspired by *High Performance Python*:
```python
# This code is inspired by concepts from "High Performance Python, 3rd ed."
# by Micha Gorelick and Ian Ozsvald (O'Reilly). Copyright 2025 Micha Gorelick and Ian Ozsvald, 978-1-098-16596-3.
```
