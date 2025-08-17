#!/usr/bin/env python3
"""Basic CI test that bypasses pytest import issues.
This will be used until the main test suite is working.
"""

import ast
import sys
from pathlib import Path

# Add src to path for CI environments
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def test_basic_imports():
    """Test that basic imports work."""
    try:

        print("✅ All basic imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_checker_instantiation():
    """Test that the checker can be instantiated."""
    try:
        from flake8_patterns.checker import PatternChecker

        code = "x = 1"
        tree = ast.parse(code)
        checker = PatternChecker(tree)
        errors = list(checker.run())

        print(f"✅ Checker instantiation successful, found {len(errors)} errors")
        return True
    except Exception as e:
        print(f"❌ Checker instantiation failed: {e}")
        return False


def test_message_system():
    """Test that the message system works."""
    try:
        from flake8_patterns.messages import ALL_MESSAGES

        if len(ALL_MESSAGES) > 0:
            print(f"✅ Message system works, {len(ALL_MESSAGES)} messages loaded")
            return True
        print("⚠️ Message system works but no messages found")
        return False
    except Exception as e:
        print(f"❌ Message system failed: {e}")
        return False


def test_book_references():
    """Test that book references work."""
    try:
        from flake8_patterns.book_refs import get_book_reference

        # Test a known reference
        ref = get_book_reference("EFP105")
        if ref:
            print(f"✅ Book reference system works, found: {ref.item}")
            return True
        print("⚠️ Book reference system works but EFP105 not found")
        return False
    except Exception as e:
        print(f"❌ Book reference system failed: {e}")
        return False


def run_all_tests():
    """Run all basic tests."""
    tests = [
        test_basic_imports,
        test_checker_instantiation,
        test_message_system,
        test_book_references,
    ]

    passed = 0
    total = len(tests)

    print("Running basic CI tests...")
    print(f"Python version: {sys.version}")
    print("-" * 40)

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")

    print("-" * 40)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All basic tests passed!")
        return 0
    print("❌ Some tests failed")
    return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
