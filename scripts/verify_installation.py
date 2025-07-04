#!/usr/bin/env python3
"""
Comprehensive verification script for flake8-patterns installation.
Run this to verify everything is working correctly.

Updated for verified Tier 1 rules from "Effective Python" (3rd Edition):
- EFP105: Multiple-Assignment Unpacking over Indexing
- EFP213: Context-Aware String Concatenation
- EFP318: Parallel Iteration with zip()
- EFP320: Loop Variables After Loop Ends
- EFP321: Be Defensive when Iterating over Arguments
- EFP426: Comprehensive dict.get() patterns
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


# Colors for output
class Colors:
    GREEN = "\033[0;32m"
    RED = "\033[0;31m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


def log_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.NC}")


def log_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.NC}")


def log_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.NC}")


def log_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.NC}")


def run_command(cmd, capture_output=True):
    """Run a command and return success, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=capture_output, text=True, timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def check_python_version():
    """Check Python version compatibility."""
    print(f"\n{Colors.BLUE}🐍 Python Environment Check{Colors.NC}")

    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version >= (3, 13):
        log_success("Python 3.13+ - Excellent! Full optimization available")
    elif version >= (3, 10):
        log_success("Python 3.10+ - Good! All features supported")
    else:
        log_warning("Python < 3.10 - Some features may not be available")

    # Check virtual environment
    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        log_success("Running in virtual environment")
    else:
        log_warning("Not in virtual environment - consider using one")

    return True


def check_package_installation():
    """Check if flake8-patterns is installed."""
    print(f"\n{Colors.BLUE}📦 Package Installation Check{Colors.NC}")

    # Check with pip
    success, stdout, stderr = run_command("pip show flake8-patterns")
    if success and "flake8-patterns" in stdout:
        log_success("Package found in pip list")
        # Extract version
        for line in stdout.split("\n"):
            if line.startswith("Version:"):
                version = line.split(":", 1)[1].strip()
                print(f"   Version: {version}")
            elif line.startswith("Location:"):
                location = line.split(":", 1)[1].strip()
                print(f"   Location: {location}")
    else:
        log_error("Package not found in pip list")
        if stderr:
            print(f"   Error: {stderr}")
        return False

    return True


def check_import_system():
    """Check if imports work correctly."""
    print(f"\n{Colors.BLUE}🔧 Import System Check{Colors.NC}")

    # Test basic import
    try:
        import flake8_patterns

        log_success("Basic package import works")
        print(f"   Package file: {flake8_patterns.__file__}")

        if hasattr(flake8_patterns, "__version__"):
            print(f"   Version: {flake8_patterns.__version__}")
    except ImportError as e:
        log_error(f"Basic import failed: {e}")
        return False

    # Test main checker import
    try:
        from flake8_patterns.checker import PatternChecker

        log_success("PatternChecker import works")
        print(f"   Checker class: {PatternChecker}")
    except ImportError as e:
        log_error(f"PatternChecker import failed: {e}")
        return False

    # Test other components
    components = [
        ("messages", "get_error_message"),
        ("messages", "ALL_MESSAGES"),
        ("book_refs", "get_book_reference"),
        ("book_refs", "EFFECTIVE_PYTHON_REFS"),
    ]

    for module, component in components:
        try:
            mod = __import__(f"flake8_patterns.{module}", fromlist=[component])
            obj = getattr(mod, component, None)
            if obj is not None:
                log_success(f"{module}.{component} import works")
            else:
                log_warning(
                    f"{module}.{component} not available (may not be implemented yet)"
                )
        except Exception as e:
            log_warning(f"{module}.{component} import issue: {e}")

    return True


def check_flake8_integration():
    """Check if flake8 recognizes the plugin."""
    print(f"\n{Colors.BLUE}🔌 flake8 Integration Check{Colors.NC}")

    # Check flake8 version
    success, stdout, stderr = run_command("flake8 --version")
    if not success:
        log_error("flake8 not available")
        print(f"   Error: {stderr}")
        return False

    print(f"flake8 version info: {stdout.strip()}")

    # Check if our plugin is listed
    if "flake8-patterns" in stdout:
        log_success("Plugin recognized by flake8")
    else:
        log_warning("Plugin not visible in flake8 --version")
        log_info("This might be normal if flake8 caches plugins")

    return True


def check_plugin_functionality():
    """Test actual plugin functionality with verified Tier 1 rules."""
    print(f"\n{Colors.BLUE}⚡ Plugin Functionality Check{Colors.NC}")

    # Test cases for verified Tier 1 rules
    test_cases = [
        {
            "name": "EFP105 - Sequential indexing patterns",
            "code": """
# Sequential indexing that should trigger EFP105
item = ("Alice", 25, "Engineer")
name = item[0]      # Sequential indexing
age = item[1]       # Should trigger EFP105
job = item[2]       # Continues pattern
""",
            "expected_error": "EFP105",
        },
        {
            "name": "EFP213 - Implicit string concatenation in collections",
            "code": """
# Missing comma - dangerous implicit concatenation
items = [
    "first_item" "second_item",  # Should trigger EFP213
    "third_item",
]
""",
            "expected_error": "EFP213",
        },
        {
            "name": "EFP318 - Manual parallel iteration",
            "code": """
# Manual parallel iteration that should trigger EFP318
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for i in range(len(names)):     # Should trigger EFP318
    name = names[i]
    age = ages[i]
    print(f"{name} is {age}")
""",
            "expected_error": "EFP318",
        },
        {
            "name": "EFP320 - Loop variable used after loop",
            "code": """
# Loop variable used after loop ends
def find_user(users):
    for user in users:
        if user.is_admin:
            break

    if user.is_admin:           # Should trigger EFP320
        return user
""",
            "expected_error": "EFP320",
        },
        {
            "name": "EFP321 - Multiple iterations over same parameter",
            "code": """
# Function iterating over parameter multiple times
def normalize(numbers):
    total = sum(numbers)        # First iteration
    result = []
    for value in numbers:       # Second iteration - should trigger EFP321
        percent = 100 * value / total
        result.append(percent)
    return result
""",
            "expected_error": "EFP321",
        },
        {
            "name": "EFP426 - try/except KeyError patterns",
            "code": """
# try/except KeyError that should use dict.get()
try:
    value = my_dict[key]        # Should trigger EFP426
except KeyError:
    value = default_value
""",
            "expected_error": "EFP426",
        },
    ]

    for test_case in test_cases:
        print(f"\n   Testing: {test_case['name']}")

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_case["code"])
            temp_file = f.name

        try:
            # Run flake8 on the test file
            success, stdout, stderr = run_command(f"flake8 --select=EFP {temp_file}")

            if test_case["expected_error"] in stdout:
                log_success(f"Detected {test_case['expected_error']} correctly")
            elif stdout.strip():
                log_warning(f"Detected other issues: {stdout.strip()}")
            else:
                log_warning(
                    f"No {test_case['expected_error']} detected (rule may not be implemented yet)"
                )

        finally:
            # Clean up
            os.unlink(temp_file)


def check_entry_points():
    """Check entry points configuration."""
    print(f"\n{Colors.BLUE}🚪 Entry Points Check{Colors.NC}")

    try:
        # Check if we can find the entry point
        import importlib.metadata

        # Look for flake8 extension entry points
        found_entry_point = False
        try:
            entry_points = importlib.metadata.entry_points(group="flake8.extension")
            for entry_point in entry_points:
                if "flake8_patterns" in str(entry_point) or entry_point.name == "EFP":
                    log_success(f"Entry point found: {entry_point}")
                    found_entry_point = True
        except TypeError:
            # Fallback for older Python versions
            entry_points = importlib.metadata.entry_points()
            flake8_entries = entry_points.get("flake8.extension", [])
            for entry_point in flake8_entries:
                if "flake8_patterns" in str(entry_point) or entry_point.name == "EFP":
                    log_success(f"Entry point found: {entry_point}")
                    found_entry_point = True

        if not found_entry_point:
            log_warning("No flake8-patterns entry point found")

        return found_entry_point

    except ImportError:
        log_info("importlib.metadata not available, skipping entry point check")
    except Exception as e:
        log_warning(f"Entry point check failed: {e}")

    return False


def check_console_commands():
    """Check if console commands are available."""
    print(f"\n{Colors.BLUE}💻 Console Commands Check{Colors.NC}")

    commands = [
        "flake8-patterns-info",
        "flake8-pp-info",
    ]

    found_any = False
    for cmd in commands:
        success, stdout, stderr = run_command(f"which {cmd}")
        if success:
            log_success(f"Console command '{cmd}' available")
            found_any = True
        else:
            log_info(f"Console command '{cmd}' not found (may not be implemented)")

    return found_any


def run_comprehensive_test():
    """Run a comprehensive functionality test with verified patterns."""
    print(f"\n{Colors.BLUE}🧪 Comprehensive Test{Colors.NC}")

    # Create a more complex test file with verified Tier 1 patterns
    test_code = '''
"""Test file for flake8-patterns comprehensive check."""

# EFP105: Sequential indexing patterns
def process_user_data():
    user_tuple = ("Alice", 25, "Engineer")
    name = user_tuple[0]    # EFP105
    age = user_tuple[1]     # EFP105
    job = user_tuple[2]     # EFP105
    return f"{name} ({age}) - {job}"

# EFP213: Implicit string concatenation in collections
config_items = [
    "database_host" "database_port",  # EFP213 - missing comma!
    "redis_url",
    "api_key",
]

# EFP318: Manual parallel iteration
def calculate_scores():
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]
    for i in range(len(names)):      # EFP318
        name = names[i]
        score = scores[i]
        print(f"{name}: {score}")

# EFP320: Loop variable used after loop
def find_admin(users):
    for user in users:
        if user.is_admin:
            break

    if user.is_admin:               # EFP320
        return user

# EFP321: Multiple iterations over same parameter
def analyze_data(items):
    count = len(items)              # First iteration
    total = sum(items)              # Second iteration - EFP321
    return total / count

# EFP426: try/except KeyError patterns
def get_config_value(config, key):
    try:
        value = config[key]         # EFP426
    except KeyError:
        value = "default"
    return value

# Good patterns (should not trigger errors)
def good_unpacking():
    user_tuple = ("Alice", 25, "Engineer")
    name, age, job = user_tuple     # Good!
    return f"{name} ({age}) - {job}"

def good_parallel_iteration():
    names = ["Alice", "Bob", "Charlie"]
    scores = [85, 92, 78]
    for name, score in zip(names, scores):  # Good!
        print(f"{name}: {score}")

def good_dict_access():
    def get_config_value(config, key):
        return config.get(key, "default")   # Good!

# Future High Performance Python patterns (for v0.8.0+)
def future_hp_patterns():
    # HP001: String concatenation in loops (future)
    result = ""
    for item in ["a", "b", "c"]:
        result += item  # Will be HP001 in future

    # PC001: List membership testing (future)
    if "item" in ["a", "b", "c", "d", "e"]:  # Will be PC001 in future
        print("found")
'''

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_code)
        temp_file = f.name

    try:
        # Run flake8 with Effective Python rules
        success, stdout, stderr = run_command(f"flake8 --select=EFP {temp_file}")

        if stdout.strip():
            print("   Detected Effective Python issues:")
            for line in stdout.strip().split("\n"):
                if line.strip():
                    print(f"     {line}")
            log_success("Plugin is detecting EFP patterns correctly")
        else:
            log_info("No EFP issues detected (rules may need implementation)")

        # Count different rule types
        efp_issues = len([line for line in stdout.split("\n") if "EFP" in line])
        print(f"   Effective Python (EFP) issues found: {efp_issues}")

        # Try with all error codes to see what else is detected
        success, stdout, stderr = run_command(f"flake8 {temp_file}")
        total_issues = len([line for line in stdout.split("\n") if line.strip()])
        print(f"   Total flake8 issues found: {total_issues}")

        return efp_issues > 0

    finally:
        os.unlink(temp_file)


def check_book_references():
    """Check if book reference system is working."""
    print(f"\n{Colors.BLUE}📚 Book Reference System Check{Colors.NC}")

    try:
        from flake8_patterns.book_refs import EFFECTIVE_PYTHON_REFS, get_book_reference

        # Check Tier 1 rule references
        tier1_rules = ["EFP105", "EFP213", "EFP318", "EFP320", "EFP321", "EFP426"]

        for rule in tier1_rules:
            ref = get_book_reference(rule)
            if ref:
                log_success(f"{rule} book reference found: {ref.item}")
            else:
                log_warning(f"{rule} book reference missing")

        # Check total reference count
        total_refs = len(EFFECTIVE_PYTHON_REFS)
        print(f"   Total Effective Python references: {total_refs}")

        if total_refs >= 26:
            log_success("Complete reference coverage (26+ rules)")
        elif total_refs >= 6:
            log_success("Tier 1 reference coverage (6+ rules)")
        else:
            log_warning("Limited reference coverage")

        return True

    except Exception as e:
        log_warning(f"Book reference check failed: {e}")
        return False


def main():
    """Run all verification checks."""
    print(f"{Colors.BLUE}🔍 flake8-patterns Installation Verification{Colors.NC}")
    print(f"{Colors.BLUE}Educational Effective Python Plugin (v0.1.1){Colors.NC}")
    print("=" * 60)

    checks = [
        ("Python Environment", check_python_version),
        ("Package Installation", check_package_installation),
        ("Import System", check_import_system),
        ("flake8 Integration", check_flake8_integration),
        ("Entry Points", check_entry_points),
        ("Book Reference System", check_book_references),
        ("Plugin Functionality", check_plugin_functionality),
        ("Comprehensive Test", run_comprehensive_test),
        ("Console Commands", check_console_commands),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            log_error(f"{name} check failed with exception: {e}")
            results.append((name, False))

    # Summary
    print(f"\n{Colors.BLUE}📊 Summary{Colors.NC}")
    print("=" * 30)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")

    print(f"\nOverall: {passed}/{total} checks passed")

    if passed == total:
        log_success("🎉 All checks passed! flake8-patterns is installed correctly.")
    elif passed >= total * 0.7:
        log_warning("⚠️ Most checks passed. Some features may need implementation.")
    else:
        log_error("❌ Many checks failed. Installation may have issues.")

    # Recommendations
    print(f"\n{Colors.BLUE}💡 Next Steps{Colors.NC}")
    if passed < total:
        print("• Fix any failed checks above")
        print("• Try reinstalling: pip uninstall flake8-patterns && pip install -e .")
        print("• Check that you're in the right virtual environment")

    print("• Test on your actual code: flake8 --select=EFP your_file.py")
    print("• Start with EFP105 implementation (current priority)")
    print("• Check docs/rules/ for detailed rule documentation")
    print("• Implement Tier 1 rules: EFP105, EFP213, EFP318, EFP320, EFP321, EFP426")

    print(f"\n{Colors.BLUE}📚 Educational Resources{Colors.NC}")
    print("• Rule documentation: docs/rules/")
    print("• Implementation roadmap: docs/index.md")
    print("• Book reference: 'Effective Python' (3rd Edition) by Brett Slatkin")


if __name__ == "__main__":
    main()
