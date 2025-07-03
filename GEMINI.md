# GEMINI.md - flake8-patterns Project Guidelines

Guidelines for Gemini when handling tasks in the flake8-patterns educational linting project.

## 🎯 Project Context

**flake8-patterns** is an educational flake8 plugin that detects anti-patterns from:
- **"Effective Python" (3rd Edition)** by Brett Slatkin (PRIMARY FOCUS)
- "High Performance Python" (3rd Edition) by Micha Gorelick and Ian Ozsvald (FUTURE)

*Note: We're starting with Effective Python patterns as they tend to be more objective and easier to implement. Comprehensive analysis identified 26 implementable rules across 3 priority tiers.*

**Current Status:** v0.1.0-dev, implementing EP105 (multiple-assignment unpacking over indexing)

**Your Role:** Handle simple, routine tasks while Claude focuses on complex architecture and implementation decisions.

## 🧠 MCP Sequential Thinking Protocol

For **any complex task** (implementation, analysis, multi-file changes), use structured thinking:

### Required Thought Structure
```json
{
  "thought": "Clear description of current thinking step",
  "thoughtNumber": 1,
  "totalThoughts": 3,
  "nextThoughtNeeded": true,
  "isRevision": false
}
```

### Example: Implementing EP105 Detection
```json
// Thought 1
{
  "thought": "Need to analyze EP105 requirements: detect sequential indexing like x = item[0]; y = item[1] that should use unpacking",
  "thoughtNumber": 1,
  "totalThoughts": 4,
  "nextThoughtNeeded": true
}

// Thought 2
{
  "thought": "Should examine existing AST visitor patterns in checker.py to understand codebase style for assignment detection",
  "thoughtNumber": 2,
  "totalThoughts": 4,
  "nextThoughtNeeded": true
}

// Thought 3
{
  "thought": "Implementation requires: 1) visit_Assign method 2) track sequential indexing patterns 3) detect x=item[0], y=item[1] 4) call self.error()",
  "thoughtNumber": 3,
  "totalThoughts": 4,
  "nextThoughtNeeded": true
}

// Thought 4
{
  "thought": "Ready to implement. Will add visitor method, create tests, and ensure book reference accuracy for Item 5.",
  "thoughtNumber": 4,
  "totalThoughts": 4,
  "nextThoughtNeeded": false
}
```

### When to Use Sequential Thinking
- **Complex rule implementation** (new AST visitors)
- **Multi-file refactoring** (more than 2 files)
- **Book reference validation** (accuracy is critical)
- **Architecture decisions** (impacts other components)
- **Performance analysis** (project-wide changes)

### When NOT to Use (Simple Tasks)
- ✏️ **Single typo fixes**
- 🎨 **Code formatting** (black, isort)
- 📝 **Simple git commits**
- 🔧 **Adding single test cases**

## 🔧 Tool Permissions & Safety

### Allowed Operations
```yaml
allowed_tools:
  - ReadFile         # Analyze project files
  - Edit            # Modify existing files (with approval)
  - TestExecutor    # Run pytest, coverage
  - Linter          # flake8, black, ruff, mypy
  - Shell           # Approved commands only
```

### Restricted Operations
```yaml
restricted_tools:
  - WriteFile       # No new file creation without Claude
  - GitPush        # Prevent accidental pushes
  - WebFetch       # No external dependencies without approval
```

### Safe Commands Only
```bash
# ✅ Allowed shell commands:
pytest tests/test_effective_python.py
black src/ tests/
isort src/ tests/
ruff check src/ tests/ --fix
mypy src/flake8_patterns --strict

# ❌ Blocked commands:
rm -rf *
curl external-api.com
git push origin main
pip install unknown-package
```

## 📋 Project Structure & Conventions

### File Organization
```
src/flake8_patterns/
├── __init__.py          # Version updates only
├── checker.py           # ⚠️ Complex - defer to Claude
├── messages.py          # ⚠️ Error codes - defer to Claude
├── utils.py            # ✅ Simple helpers OK
├── book_refs.py        # ⚠️ Accuracy critical - defer to Claude
└── rules/              # ✅ Example additions OK
    ├── __init__.py
    ├── effective_python.py    # ⚠️ New rules - defer to Claude
    └── examples/              # ✅ Code examples OK

tests/
├── test_effective_python.py  # ✅ Simple test additions OK
├── test_messages.py          # ✅ Message format tests OK
├── conftest.py              # ⚠️ Test infrastructure - defer to Claude
└── fixtures/                # ✅ Example code OK

examples/
├── bad_patterns.py          # ✅ Example additions OK
└── good_patterns.py         # ✅ Example additions OK
```

### Python Code Standards
```python
# Type hints REQUIRED (Python 3.10+)
def visit_Assign(self, node: ast.Assign) -> None:
    """Check assignment patterns for unpacking opportunities.

    Detects EP105: Sequential indexing that should use unpacking.
    Reference: "Effective Python" (3rd Edition), Item 5, Chapter 1.
    """
    if self._is_sequential_indexing(node):
        self.error(node, "EP105")
    self.generic_visit(node)

# Error message format (CRITICAL - get approval for changes)
EP105_MESSAGE = (
    "Sequential indexing detected, use multiple-assignment unpacking",
    "'Effective Python' (3rd Edition), Item 5, Chapter 1: Pythonic Thinking",
    "Readability: Cleaner, less error-prone, same performance"
)

# Git commit format (use conventional commits)
git commit -m "feat(EP105): implement multiple-assignment unpacking detection"
git commit -m "test(EP105): add edge cases for nested indexing"
git commit -m "fix(utils): handle None values in get_variable_name"
git commit -m "docs: update README with EP105 examples"
```

## 🔍 Large Codebase Analysis Commands

### Project-Wide Analysis
```bash
# Check all rules for consistency
gemini -p "@src/ @tests/ Are all EP### rules properly implemented and tested?"

# Verify book reference accuracy
gemini -p "@src/book_refs.py @src/messages.py Do all error codes cite correct Item numbers and chapters?"

# Documentation consistency
gemini -p "@README.md @examples/ @src/ Do README examples match implemented rules?"

# Integration conflict check
gemini -p "@src/ Are there any error code conflicts with flake8-bugbear or flake8-comprehensions?"
```

### Quality Assurance
```bash
# Message quality assessment
gemini -p "@src/messages.py Are error messages clear and educational for Python learners?"

# Impact claims verification
gemini -p "@src/messages.py @examples/ Are readability/performance estimates accurate and well-demonstrated?"

# Test coverage analysis
gemini -p "@tests/ @examples/ Which rules lack comprehensive test coverage?"

# Simple refactoring opportunities
gemini -p "@src/ Identify areas for simple refactoring to improve consistency"
```

## ✅ Tasks You Handle (Simple & Safe)

### Git Operations
```bash
# Standard commits (use conventional format)
git commit -m "fix(docs): correct typo in README examples"
git commit -m "test(EP105): add edge case for different variable names"
git commit -m "style: format code with black and isort"
git commit -m "chore(deps): update pytest to latest version"
```

### Code Quality Tasks
```bash
# Format and check code
black src/ tests/
isort src/ tests/
ruff check src/ tests/ --fix

# Run specific tests
pytest tests/test_effective_python.py::test_ep105_detection
pytest --cov=flake8_patterns --cov-report=html
```

### Documentation Updates
- ✅ Fix typos in docstrings
- ✅ Update example code snippets
- ✅ Add simple sections to existing docs
- ✅ Update dependency versions in pyproject.toml
- ✅ Fix broken links in README

### Simple Code Changes
- ✅ Add straightforward test cases (with examples provided)
- ✅ Update version numbers in `__init__.py`
- ✅ Fix import statement organization
- ✅ Add type hints to existing functions
- ✅ Update file headers with correct licenses

## ❌ Tasks to Defer to Claude (Complex & Critical)

### Implementation Work
- 🧠 **New AST visitor methods** (rule detection logic)
- 🧠 **Error code assignments** (strategic decisions)
- 🧠 **Book reference validation** (accuracy critical)
- 🧠 **Performance optimization** (complex analysis)
- 🧠 **Plugin architecture** (design decisions)

### Quality-Critical Work
- 📚 **Error message content** (educational accuracy)
- 📚 **Rule prioritization** (strategic choices)
- 📚 **API design** (public interfaces)
- 📚 **Testing strategy** (coverage decisions)

## 🤝 Collaboration Protocol

### Before Acting (Always Ask)
- **New error codes**: Always defer to Claude
- **Book reference changes**: Accuracy is critical
- **AST logic**: Complex pattern detection
- **Multi-file changes**: Coordinate first
- **Breaking changes**: Always discuss

### Reporting Completed Work
```markdown
## ✅ Completed Tasks

**Sequential Thinking Used:** Yes/No
**Commands executed:**
- `black src/ tests/` (formatted 15 files)
- `pytest tests/test_effective_python.py` (12 tests passed)
- `git commit -m "style: format code with black"`

**Files modified:**
- src/flake8_patterns/utils.py (minor typo fix)
- tests/test_effective_python.py (added EP105 edge case)

**Issues found:**
- EP105 test coverage missing for nested indexing
- README example shows outdated syntax

**Recommended next steps:**
1. Claude review: EP105 nested indexing handling
2. Update README examples for current implementation
3. Add performance benchmarks for EP105 detection

**Status:** Ready for Claude review of complex issues
```

### Error Handling & Recovery
```bash
# If a task fails:
1. Document the error clearly
2. Don't attempt complex fixes
3. Revert simple changes if needed:
   git checkout -- filename.py
4. Report to Claude with full error details
```

## 🎯 Current Implementation Priorities

### Phase 1: Tier 1 Rules (Highest Impact, Clear Gaps)
*Based on comprehensive analysis of all 125 Effective Python items*

#### EP105 (Multiple-Assignment Unpacking) - CURRENT PRIORITY
```python
# Pattern to detect:
item = (1, 2, 3)
first = item[0]     # Should trigger EP105
second = item[1]    # Part of sequential pattern

# Good pattern:
first, second, third = item

# Files involved:
- src/flake8_patterns/checker.py     # Core detection (Claude)
- src/flake8_patterns/messages.py   # Error definition (Claude)
- tests/test_effective_python.py    # Test cases (You + Claude)
- examples/bad_patterns.py          # Examples (You)
```

#### Next Tier 1 Rules in Pipeline (6 total)
- **EP213**: Context-Aware String Concatenation (Item 13, Chapter 2)
- **EP318**: Parallel Iteration with zip() (Item 18, Chapter 3)
- **EP320**: Loop Variables After Loop Ends (Item 20, Chapter 3)
- **EP321**: Be Defensive when Iterating over Arguments (Item 21, Chapter 3)
- **EP426**: Comprehensive dict.get() patterns (Item 26, Chapter 4)

### Future: High Performance Python Integration
- **HP001**: String concatenation in loops → str.join()
- **PC001**: List membership testing → set for O(1) lookup
- **MC001**: Missing __slots__ → memory optimization

### Total Verified Rules: 26 across 3 tiers
- **Tier 1**: 6 rules (highest impact, clear detection)
- **Tier 2**: 14 rules (code quality, API design)
- **Tier 3**: 6 rules (advanced patterns, nice to have)

## 🔄 Environment & Configuration

### Development Environment
```bash
# Virtual environment setup
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"

# Verify plugin installation
flake8 --version  # Should show flake8-patterns

# Test plugin functionality
flake8 examples/bad_patterns.py  # Should show EP### errors
```

### Configuration Files
```yaml
# Project settings: .gemini/settings.json (if needed)
{
  "checkpointing": true,        # Enable safe file snapshots
  "contextFileName": "GEMINI.md"  # This file provides context
}

# Environment variables: .env
PYTHON_VERSION=3.13
COVERAGE_TARGET=90
BOOK_VALIDATION=strict
```

**Context Management:**
- **Single GEMINI.md**: All project guidelines in root-level file
- **CLAUDE.md**: Separate file for Claude-specific development guidance
- **README.md**: User-facing documentation and examples

---
