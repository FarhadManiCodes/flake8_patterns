# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a flake8 plugin called `flake8-performance-patterns` that detects performance anti-patterns in Python code. The plugin is based on patterns from two authoritative books:
- "High Performance Python" (3rd Edition) by Micha Gorelick and Ian Ozsvald
- "Effective Python" (3rd Edition) by Brett Slatkin

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
flake8 --version  # Should show flake8-performance-patterns
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=flake8_performance_patterns

# Test specific module
pytest tests/test_string_operations.py

# Test the plugin on sample code
flake8 examples/bad_patterns.py
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
mypy src/flake8_performance_patterns --strict

# Run pre-commit hooks
pre-commit run --all-files
```

### Plugin Development
```bash
# Test plugin manually
python -c "
import ast
from flake8_performance_patterns.checker import PerformanceChecker
code = '''
result = \"\"
for item in items:
    result += str(item)  # Should trigger HP001
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
   - Error categories: HP (High Performance Python), PC (Collections), EP (Effective Python), MC (Memory), NP (NumPy)

3. **utils.py**: AST analysis utilities
   - `NodeVisitorWithParents`: Base class for tracking parent nodes
   - Helper functions for AST node analysis and Python version compatibility

4. **book_refs.py**: Book reference system for educational context

### Error Code Categories

- **HP001-HP020**: String operations (from "High Performance Python")
- **PC001-PC020**: Collection performance patterns
- **EP001-EP020**: Iteration patterns (from "Effective Python")
- **MC001-MC020**: Memory optimization patterns
- **NP001-NP020**: NumPy performance patterns

### Project Structure
```
src/flake8_performance_patterns/
├── __init__.py          # Main exports and plugin metadata
├── checker.py           # Core checker implementation
├── messages.py          # Error messages and book references
├── utils.py             # AST analysis utilities
├── book_refs.py         # Book reference system
└── rules/               # Rule implementations (expandable)
    └── __init__.py
```

## Adding New Rules

1. **Add message to messages.py**: Include in appropriate category (HP, PC, EP, MC, NP)
2. **Implement detection in checker.py**: Add visitor method for the AST pattern
3. **Add tests**: Create test cases in `tests/test_*.py`
4. **Include book reference**: Every rule must reference specific book chapter/page

## Testing Strategy

- Use pytest fixtures in `conftest.py` for common test patterns
- Test both positive (should trigger) and negative (should not trigger) cases
- Include book reference validation in tests
- Test error message formatting and performance impact descriptions

## Python Version Support

- **Minimum**: Python 3.10+
- **Target**: Python 3.13 (optimized performance tier)
- **Compatibility**: Uses `sys.version_info` checks for feature detection

## Development Notes

- The plugin extends flake8's architecture following the flake8-bugbear pattern
- AST analysis uses custom `NodeVisitorWithParents` for context-aware checking
- Each rule includes educational context with book references and performance impact estimates
- Pre-commit hooks ensure code quality with black, isort, ruff, and mypy