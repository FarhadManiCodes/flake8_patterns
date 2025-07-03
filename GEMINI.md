# GEMINI.md

Guidelines for Gemini when handling simple tasks in the flake8-patterns project.

## 🎯 Your Role

You handle **simple, routine tasks** while Claude focuses on complex architecture and implementation decisions. Think of this as a collaborative workflow where you're the efficient assistant for straightforward operations.

## 📋 Project Context

**flake8-patterns** is an educational flake8 plugin that detects anti-patterns from:
- "Effective Python" (3rd Edition) by Brett Slatkin
- "High Performance Python" (3rd Edition) by Micha Gorelick and Ian Ozsvald

**Current Status:** v0.1.0-dev, implementing EP201 (single-element tuples)

## 🔍 Large Codebase Analysis with Gemini CLI

When the project grows beyond single-file scope, use Gemini CLI's massive context window for project-wide analysis and simple refactoring tasks.

### When to Use Gemini CLI vs Regular Tasks

**Use Gemini CLI (`gemini -p`) for:**
- 🔍 **Simple refactoring** across multiple files
- 📊 **Project-wide consistency** checks
- 🧪 **Quality assurance** verification
- 📚 **Documentation validation**
- 🎯 **Pattern analysis** across codebase

**Stick to regular tasks for:**
- ✏️ **Single file edits** (typos, formatting)
- 🔧 **Simple test additions**
- 📝 **Basic git operations**
- 🎨 **Code formatting** (black, isort)

### Analysis Commands You Should Use

**Check project consistency:**
```bash
gemini -p "@src/ @tests/ Are all error codes consistently formatted and tested?"
```

**Verify documentation accuracy:**
```bash
gemini -p "@README.md @examples/ @src/ Do examples in README match actual implemented rules?"
```

**Quality assurance check:**
```bash
gemini -p "@src/messages.py Are error messages clear and educational for Python learners?"
```

**Simple refactoring identification:**
```bash
gemini -p "@src/ Identify simple refactoring opportunities for better code consistency"
```

**Test coverage verification:**
```bash
gemini -p "@tests/ @examples/ Which rules need more test cases or examples?"
```

**Book reference validation:**
```bash
gemini -p "@src/book_refs.py @src/messages.py Are all book references accurate and properly linked?"
```

### Reporting Results to Claude

After running analysis commands, report findings in this format:

```markdown
## 🔍 Gemini CLI Analysis Results

**Command used:**
`gemini -p "@src/ @tests/ Are all EP### rules consistently implemented?"`

**Key findings:**
- ✅ EP201 fully implemented with tests
- ⚠️ EP202 missing edge case tests
- ❌ EP203 error message format inconsistent

**Suggested actions:**
1. Add edge case tests for EP202
2. Fix EP203 message format to match template
3. Update examples to demonstrate EP203 pattern

**Files that need attention:**
- tests/test_effective_python.py (EP202 tests)
- src/messages.py (EP203 format)
- examples/bad_patterns.py (EP203 example)
```

### Integration with Regular Workflow

**Typical analysis workflow:**
1. 🔍 **Run Gemini CLI analysis** for project-wide insights
2. 📋 **Identify simple tasks** you can handle
3. 🤝 **Flag complex issues** for Claude
4. ✅ **Execute simple fixes**
5. 📝 **Commit with clear messages**
6. 📊 **Report completed work**

**Example workflow:**
```bash
# 1. Analysis
gemini -p "@src/ Check error message consistency"

# 2. Simple fixes you can do
# - Fix typos in error messages
# - Update formatting to match template
# - Add missing docstrings

# 3. Complex issues for Claude
# - Error code conflicts
# - AST detection logic
# - Book reference accuracy

# 4. Commit simple fixes
git commit -m "fix(messages): standardize error message formatting"
```

## ✅ Tasks You Should Handle

### Git Operations
```bash
# Standard commit messages (follow conventional commits)
git commit -m "feat(EP201): implement single-element tuple detection"
git commit -m "test(EP201): add comprehensive test cases"
git commit -m "docs: update README with EP201 examples"
git commit -m "fix(checker): handle edge case in tuple parsing"
git commit -m "refactor(messages): reorganize error code structure"
git commit -m "chore: update dependencies in pyproject.toml"
```

### Simple Code Changes
- Fix typos in comments/docstrings
- Update version numbers in `__init__.py`
- Add simple test cases to existing test files
- Format code with black/isort
- Update import statements
- Add simple utility functions

### Documentation Updates
- Fix markdown formatting
- Update example code snippets
- Add simple sections to existing docs
- Update dependency lists
- Fix broken links

### File Operations
- Create simple example files
- Move/rename files as directed
- Update file headers with correct imports
- Clean up temporary files

## ❌ Tasks to Defer to Claude

### Complex Implementation
- New AST visitor methods
- Error detection logic
- Book reference validation
- Performance optimization
- Architecture decisions

### Strategic Decisions
- New error code assignments
- Rule prioritization changes
- API design choices
- Testing strategy changes
- Plugin architecture modifications

## 📝 Git Commit Guidelines

### Conventional Commit Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types
- **feat**: New feature (new rule, new functionality)
- **fix**: Bug fix
- **docs**: Documentation changes
- **test**: Adding/updating tests
- **refactor**: Code refactoring without feature changes
- **chore**: Maintenance tasks (dependencies, build)
- **style**: Code style changes (formatting, missing semicolons)

### Scopes (Rule-Related)
- **EP201**: Single-element tuples
- **EP301**: enumerate patterns
- **checker**: Main checker logic
- **messages**: Error messages
- **utils**: Utility functions
- **tests**: Test-related changes
- **deps**: Dependencies

### Examples
```bash
# Good commit messages:
git commit -m "feat(EP201): add tuple comma detection"
git commit -m "test(EP201): cover edge cases for nested tuples"
git commit -m "docs: fix typo in README examples"
git commit -m "chore(deps): bump pytest to 8.0.1"
git commit -m "fix(utils): handle None values in get_variable_name"

# Avoid vague messages:
git commit -m "update code"
git commit -m "fix stuff"
git commit -m "changes"
```

## 🔧 Simple Development Tasks

### Running Tests
```bash
# Run specific test file
pytest tests/test_effective_python.py

# Run with coverage
pytest --cov=flake8_patterns

# Run specific test
pytest tests/test_effective_python.py::test_ep201_detection
```

### Code Formatting
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Check with ruff
ruff check src/ tests/
```

### File Structure Maintenance
```
src/flake8_patterns/
├── __init__.py          # Version updates
├── checker.py           # Simple fixes only
├── messages.py          # Add simple messages as directed
├── utils.py            # Simple helper functions
└── book_refs.py        # Add references as directed

tests/
├── test_effective_python.py  # Add simple test cases
├── test_messages.py          # Test message formatting
└── conftest.py              # Test fixtures
```

## 🚦 When to Ask Claude

### Before Making Changes
- **New error codes**: Always defer to Claude
- **AST logic**: Complex pattern detection
- **Architecture**: Changes to core structure
- **Book references**: Accuracy is critical

### For Guidance
- **Unclear requirements**: Ask for clarification
- **Multiple approaches**: Let Claude decide strategy
- **Breaking changes**: Always coordinate first

### Example Questions
```
"Should I add this simple test case for EP201?"
"Can I fix this typo in the docstring?"
"The pre-commit hook failed - should I run black?"
"Version number needs updating - change to 0.1.1?"
```

## 📋 Quick Reference

### Current Implementation Priority
1. **EP201**: Single-element tuple detection
2. **EP202**: F-string patterns (next)
3. **EP203**: String concatenation (after)

### Key Files You'll Work With
- `examples/bad_patterns.py` - Add example code
- `tests/test_effective_python.py` - Add test cases
- `README.md` - Fix typos, update examples
- `pyproject.toml` - Dependency updates

### Don't Touch Without Claude
- `src/flake8_patterns/checker.py` - Core logic
- `src/flake8_patterns/messages.py` - Error definitions
- `CLAUDE.md` - Architectural guidance
- `pyproject.toml` - Version/dependency strategy

## 🤝 Collaboration Protocol

1. **Simple tasks**: Just do them efficiently
2. **Uncertain tasks**: Ask Claude first
3. **Complex tasks**: Always defer to Claude
4. **Documentation**: Keep Claude informed of what you did

### Handoff Format
When reporting completed tasks:
```
✅ Completed:
- Fixed typos in README.md (3 locations)
- Added test case for EP201 edge case
- Formatted code with black
- Committed with: "test(EP201): add edge case for empty tuples"

📋 Next suggested tasks:
- Update version in __init__.py to 0.1.1?
- Add more examples to bad_patterns.py?
```

---
