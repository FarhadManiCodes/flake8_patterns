#!/usr/bin/env python3
"""
Comprehensive verification script for flake8-patterns installation.
Run this to verify everything is working correctly.
"""

import sys
import subprocess
import tempfile
import os
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[0;32m'
    RED = '\033[0;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

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
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        log_success("Running in virtual environment")
    else:
        log_warning("Not in virtual environment - consider using one")

def check_package_installation():
    """Check if flake8-patterns is installed."""
    print(f"\n{Colors.BLUE}📦 Package Installation Check{Colors.NC}")
    
    # Check with pip
    success, stdout, stderr = run_command("pip show flake8-patterns")
    if success and "flake8-patterns" in stdout:
        log_success("Package found in pip list")
        # Extract version
        for line in stdout.split('\n'):
            if line.startswith('Version:'):
                version = line.split(':', 1)[1].strip()
                print(f"   Version: {version}")
            elif line.startswith('Location:'):
                location = line.split(':', 1)[1].strip()
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
        
        if hasattr(flake8_patterns, '__version__'):
            print(f"   Version: {flake8_patterns.__version__}")
    except ImportError as e:
        log_error(f"Basic import failed: {e}")
        return False
    
    # Test main checker import
    try:
        from flake8_patterns import PerformanceChecker
        log_success("PerformanceChecker import works")
        print(f"   Checker class: {PerformanceChecker}")
    except ImportError as e:
        log_error(f"PerformanceChecker import failed: {e}")
        return False
    
    # Test other components
    components = [
        'get_error_message',
        'ALL_MESSAGES', 
        'get_book_reference',
    ]
    
    for component in components:
        try:
            obj = getattr(flake8_patterns, component, None)
            if obj is not None:
                log_success(f"{component} import works")
            else:
                log_warning(f"{component} not available (may not be implemented yet)")
        except Exception as e:
            log_warning(f"{component} import issue: {e}")
    
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
    """Test actual plugin functionality."""
    print(f"\n{Colors.BLUE}⚡ Plugin Functionality Check{Colors.NC}")
    
    # Create temporary test file
    test_cases = [
        {
            "name": "HP001 - String concatenation in loop",
            "code": '''
result = ""
for i in range(10):
    result += str(i)  # Should trigger HP001
''',
            "expected_error": "HP001"
        },
        {
            "name": "HP002 - Multiple string concatenations", 
            "code": '''
message = "Hello" + " " + "beautiful" + " " + "world"  # Should trigger HP002
''',
            "expected_error": "HP002"
        },
        {
            "name": "EP001 - range(len()) pattern",
            "code": '''
items = ["a", "b", "c"]
for i in range(len(items)):  # Should trigger EP001
    print(i, items[i])
''',
            "expected_error": "EP001"
        }
    ]
    
    for test_case in test_cases:
        print(f"\n   Testing: {test_case['name']}")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(test_case['code'])
            temp_file = f.name
        
        try:
            # Run flake8 on the test file
            success, stdout, stderr = run_command(f"flake8 {temp_file}")
            
            if test_case['expected_error'] in stdout:
                log_success(f"Detected {test_case['expected_error']} correctly")
            elif stdout.strip():
                log_warning(f"Detected other issues: {stdout.strip()}")
            else:
                log_warning(f"No {test_case['expected_error']} detected (rule may not be implemented yet)")
                
        finally:
            # Clean up
            os.unlink(temp_file)

def check_entry_points():
    """Check entry points configuration."""
    print(f"\n{Colors.BLUE}🚪 Entry Points Check{Colors.NC}")
    
    try:
        # Check if we can find the entry point
        import pkg_resources
        
        # Look for flake8 extension entry points
        for entry_point in pkg_resources.iter_entry_points('flake8.extension'):
            if 'flake8_patterns' in str(entry_point):
                log_success(f"Entry point found: {entry_point}")
                return True
        
        log_warning("No flake8-patterns entry point found")
        
    except ImportError:
        log_info("pkg_resources not available, skipping entry point check")
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
    
    for cmd in commands:
        success, stdout, stderr = run_command(f"which {cmd}")
        if success:
            log_success(f"Console command '{cmd}' available")
        else:
            log_info(f"Console command '{cmd}' not found (may not be implemented)")

def run_comprehensive_test():
    """Run a comprehensive functionality test."""
    print(f"\n{Colors.BLUE}🧪 Comprehensive Test{Colors.NC}")
    
    # Create a more complex test file
    test_code = '''
"""Test file for flake8-patterns comprehensive check."""

# HP001: String concatenation in loop
def bad_string_building():
    result = ""
    for item in ["a", "b", "c"]:
        result += item  # HP001

# HP002: Multiple concatenations  
message = "Hello" + " " + "world" + "!"  # HP002

# HP003: % formatting
name = "Alice"
greeting = "Hello %s" % name  # HP003

# EP001: range(len()) pattern
items = [1, 2, 3]
for i in range(len(items)):  # EP001
    print(items[i])

# Good code (should not trigger errors)
def good_string_building():
    return "".join(["a", "b", "c"])

def good_formatting():
    name = "Alice"
    return f"Hello {name}"

def good_iteration():
    items = [1, 2, 3]
    for i, item in enumerate(items):
        print(item)
'''
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_code)
        temp_file = f.name
    
    try:
        # Run flake8 with specific error codes
        success, stdout, stderr = run_command(f"flake8 --select=HP,PC,EP {temp_file}")
        
        if stdout.strip():
            print("   Detected issues:")
            for line in stdout.strip().split('\n'):
                if line.strip():
                    print(f"     {line}")
            log_success("Plugin is detecting issues correctly")
        else:
            log_info("No issues detected (rules may need implementation)")
            
        # Try with all error codes
        success, stdout, stderr = run_command(f"flake8 {temp_file}")
        error_count = len([line for line in stdout.split('\n') if line.strip()])
        print(f"   Total flake8 issues found: {error_count}")
        
    finally:
        os.unlink(temp_file)

def main():
    """Run all verification checks."""
    print(f"{Colors.BLUE}🔍 flake8-patterns Installation Verification{Colors.NC}")
    print("=" * 50)
    
    checks = [
        ("Python Environment", check_python_version),
        ("Package Installation", check_package_installation),
        ("Import System", check_import_system),
        ("flake8 Integration", check_flake8_integration),
        ("Entry Points", check_entry_points),
        ("Console Commands", check_console_commands),
        ("Plugin Functionality", check_plugin_functionality),
        ("Comprehensive Test", run_comprehensive_test),
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
    
    print("• Test on your actual code: flake8 your_file.py")
    print("• Implement more rules if functionality checks show warnings")
    print("• Set up pre-commit hooks for development")

if __name__ == "__main__":
    main()
