# flake8-patterns

> A comprehensive flake8 plugin that detects performance anti-patterns based on **"High Performance Python"** and **"Effective Python"**.

## 🎯 What Makes This Plugin Special

- **📚 Book-Based Rules**: Every rule references specific chapters/items from authoritative Python performance books
- **📊 Performance Impact**: Shows estimated performance improvements (e.g., "10x faster", "O(n²) → O(n)")
- **🔄 Educational**: Learn performance patterns while you code
- **🐍 Modern Python**: Optimized for Python 3.10+ with 3.13 performance features
- **🚀 Complementary**: Works alongside existing flake8 plugins for comprehensive code quality

## 📖 Supported Books

- **"High Performance Python"** by Micha Gorelick and Ian Ozsvald (3rd Edition)
- **"Effective Python"** by Brett Slatkin (3rd Edition)

## 🚀 Quick Start

```bash
# Install
pip install flake8-patterns

# Use with flake8
flake8 your_code.py

# Example output
your_code.py:3:5: HP001 String concatenation using += in loop, consider str.join()
    → 'High Performance Python', Chapter 2, p.45
    → Performance: O(n²) → O(n), ~10x faster for 100+ items
```

## 🔍 Error Codes

### String Operations (HP001-HP020)
- **HP001**: String concatenation using `+=` in loop → use `str.join()`
- **HP002**: Multiple string concatenations → use `str.join()` or f-strings
- **HP003**: String formatting using `%` operator → use f-strings

### Collection Performance (PC001-PC020)
- **PC001**: List membership testing → use `set` for O(1) lookup

### Iteration Patterns (EP001-EP020)
- **EP001**: `range(len())` pattern → use `enumerate()`

### Memory Optimization (MC001-MC020)
*Coming soon...*

## 💡 Before & After Examples

### HP001: String Concatenation in Loops

```python
# 🐌 Slow - O(n²) complexity
result = ""
for item in items:
    result += str(item)  # HP001

# ⚡ Fast - O(n) complexity
result = "".join(str(item) for item in items)
```

### PC001: Collection Membership

```python
# 🐌 Slow - O(n) lookup
large_list = list(range(10000))
if item in large_list:  # PC001
    pass

# ⚡ Fast - O(1) lookup
large_set = set(range(10000))
if item in large_set:
    pass
```

### EP001: Pythonic Iteration

```python
# 🐌 Unpythonic
items = ['a', 'b', 'c']
for i in range(len(items)):  # EP001
    print(i, items[i])

# ⚡ Pythonic
for i, item in enumerate(items):
    print(i, item)
```

## ⚙️ Configuration

Add to your `setup.cfg` or `pyproject.toml`:

```ini
[flake8]
# Enable specific rule categories
select = E,W,F,HP,PC,EP

# Focus on high-impact rules
select = HP001,HP002,PC001,EP001

# Disable specific rules
ignore = HP003

# Performance patterns only
select = HP,PC,EP,MC
```

## 🔧 Development Setup

```bash
# Clone and setup
git clone https://github.com/your-username/flake8-patterns.git
cd flake8-patterns

# Create a virtual environment and activate it
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install the package in editable mode with development dependencies
pip install -e ".[dev]"

# Verify the installation
flake8 --version  # Should show flake8-patterns
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Test specific rules
pytest tests/test_string_operations.py

# Test with coverage
pytest --cov=flake8_patterns

# Test integration
flake8 examples/bad_patterns.py
```

## 📊 Performance Benchmarks

Plugin overhead on large codebases:
- **Python 3.13**: <5% overhead (optimized target)
- **Python 3.10-3.12**: <8% overhead
- **Python 3.8-3.9**: <10% overhead (legacy support)

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md).

### Adding New Rules

1. **Identify Pattern**: Find a performance pattern from the supported books
2. **Check Coverage**: Ensure it's not covered by existing plugins
3. **Implement Rule**: Add to appropriate `rules/` module
4. **Add Tests**: Comprehensive test coverage required
5. **Document**: Include book references and performance impact

### Book References

All rules must include:
- Exact book title and edition
- Chapter/item number
- Page number
- Performance impact estimate

## 📚 Educational Resources

- [Rule Documentation](docs/rules/) - Detailed rule explanations
- [Book References](docs/book_references/) - Chapter mappings
- [Performance Impact Guide](docs/performance_impact.md) - Understanding the numbers
- [Migration Guide](docs/migration.md) - Upgrading from other tools

## 🎯 Roadmap

### Phase 1 (v0.1) - Foundation ✅
- [x] Project structure
- [x] HP001-HP003 (String operations)
- [x] PC001 (Collection membership)
- [x] EP001 (Iteration patterns)
- [x] Book reference system

### Phase 2 (v0.2) - High Impact Rules
- [ ] HP004-HP010 (Advanced string patterns)
- [ ] PC002-PC010 (Collection performance)
- [ ] EP002-EP010 (Advanced iteration)
- [ ] MC001-MC005 (Memory patterns)

### Phase 3 (v0.3) - NumPy/Pandas
- [ ] NP001-NP020 (NumPy patterns)
- [ ] PD001-PD020 (Pandas patterns)
- [ ] Performance benchmarking

### Phase 4 (v1.0) - Production Ready
- [ ] 50+ rules total
- [ ] Comprehensive documentation
- [ ] IDE integrations
- [ ] Performance regression testing

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

## 🙏 Acknowledgments

- **Micha Gorelick & Ian Ozsvald** for "High Performance Python" (3rd Edition)
- **Brett Slatkin** for "Effective Python" (3rd Edition)
- The **flake8** community for creating an extensible linting framework
- **Python community** for continuous performance improvements

---

*Made with ❤️ for Python performance enthusiasts*
