# GEMINI.md - flake8-patterns Project Guidelines

Guidelines for Gemini when handling tasks in the flake8-patterns educational linting project.

## 🎯 Project Context

**flake8-patterns** is an educational flake8 plugin that detects anti-patterns from:
- "Effective Python" (3rd Edition) by Brett Slatkin
- "High Performance Python" (3rd Edition) by Micha Gorelick and Ian Ozsvald

*Note: We're starting with Effective Python patterns as they tend to be more objective and easier to implement, but both books are equally important to the project.*

**Current Status:** v0.1.0-dev, implementing EP201 (single-element tuples)

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

### Example: Implementing EP201 Detection
```json
// Thought 1
{
  "thought": "Need to analyze EP201 requirements: detect single-element tuples missing commas like (item) vs (item,)",
  "thoughtNumber": 1,
  "totalThoughts": 4,
  "nextThoughtNeeded": true
}

// Thought 2
{
  "thought": "Should examine existing AST visitor patterns in checker.py to understand the codebase style for tuple detection",
  "thoughtNumber": 2,
  "totalThoughts": 4,
  "nextThoughtNeeded": true
}

// Thought 3
{
  "thought": "Implementation requires: 1) visit_Tuple method 2) check len(node.elts)==1 3) detect missing comma 4) call self.error()",
  "thoughtNumber": 3,
  "totalThoughts": 4,
  "nextThoughtNeeded": true
}

// Thought 4
{
  "thought": "Ready to implement. Will add visitor method, create tests, and ensure book reference accuracy.",
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
def visit_Tuple(self, node: ast.Tuple) -> None:
    """Check single-element tuple patterns.

    Detects EP201: Missing comma in single-element tuples.
    Reference: "Effective Python" (3rd Edition), Chapter 2.
    """
    if len(node.elts) == 1 and not self._has_trailing_comma(node):
        self.error(node, "EP201")
    self.generic_visit(node)

# Error message format (CRITICAL - get approval for changes)
EP201_MESSAGE = (
    "Single-element tuple missing comma, add trailing comma for clarity",
    "'Effective Python' (3rd Edition), Chapter 2: Strings and Slicing",
    "Readability: Prevents confusion with grouping parentheses"
)

# Git commit format (use conventional commits)
git commit -m "feat(EP201): implement single-element tuple detection"
git commit -m "test(EP201): add edge cases for nested tuples"
git commit -m "fix(utils): handle None values in get_variable_name"
git commit -m "docs: update README with EP201 examples"
```

## 🔍 Large Codebase Analysis Commands

### Project-Wide Analysis
```bash
# Check all rules for consistency
gemini -p "@src/ @tests/ Are all EP### rules properly implemented and tested?"

# Verify book reference accuracy
gemini -p "@src/book_refs.py @src/messages.py Do all error codes cite correct book chapters?"

# Documentation consistency
gemini -p "@README.md @examples/ @src/ Do README examples match implemented rules?"

# Integration conflict check
gemini -p "@src/ Are there any error code conflicts with flake8-bugbear or flake8-comprehensions?"
```

### Quality Assurance
```bash
# Message quality assessment
gemini -p "@src/messages.py Are error messages clear and educational for Python learners?"

# Performance claims verification
gemini -p "@src/messages.py @examples/ Are performance estimates accurate and well-demonstrated?"

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
git commit -m "test(EP201): add edge case for empty parentheses"
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
pytest tests/test_effective_python.py::test_ep201_detection
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
- tests/test_effective_python.py (added EP201 edge case)

**Issues found:**
- EP201 test coverage missing for nested tuples
- README example shows outdated syntax

**Recommended next steps:**
1. Claude review: EP201 nested tuple handling
2. Update README examples for current implementation
3. Add performance benchmarks for EP201 detection

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

### Phase 1: Starting with Effective Python (Practical Reasons)
*Note: Both books are equally valuable - starting with EP because patterns are more objective and easier to implement first.*

#### EP201 (Single-Element Tuples)
```python
# Pattern to detect:
coordinates = (42)     # Missing comma - should trigger EP201
good_tuple = (42,)     # Correct - should not trigger

# Files involved:
- src/flake8_patterns/checker.py     # Core detection (Claude)
- src/flake8_patterns/messages.py   # Error definition (Claude)
- tests/test_effective_python.py    # Test cases (You + Claude)
- examples/bad_patterns.py          # Examples (You)
```

### Future: High Performance Python Integration
- **HP001**: String concatenation in loops → str.join()
- **PC001**: List membership testing → set for O(1) lookup
- **MC001**: Missing __slots__ → memory optimization

### Next Effective Python Rules in Pipeline
- **EP202**: F-strings over C-style formatting
- **EP203**: Explicit string concatenation
- **EP301**: enumerate() over range(len())

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
