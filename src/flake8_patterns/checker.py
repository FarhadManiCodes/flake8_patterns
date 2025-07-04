"""Main checker module for flake8_patterns.

Based on patterns from "Effective Python" (3rd Edition) by Brett Slatkin.
Implements 26 verified rules across 3 tiers, starting with Tier 1 high-impact patterns.
Follows the successful flake8-bugbear plugin architecture.
"""

import ast
from collections.abc import Generator
from typing import Any

from .messages import get_error_message
from .utils import PYTHON_310_PLUS, PYTHON_313_PLUS, NodeVisitorWithParents

# Plugin metadata
__version__ = "0.1.0"

# Error type: (line, column, message, type)
Error = tuple[int, int, str, type[Any]]


class PerformanceChecker(NodeVisitorWithParents):
    """Main checker class for Effective Python patterns.

    Detects anti-patterns from "Effective Python" (3rd Edition) by Brett Slatkin.
    Educational focus with book references for learning Pythonic patterns.

    Current implementation focuses on Tier 1 rules:
    - EP105: Multiple-Assignment Unpacking over Indexing
    - EP213: Context-Aware String Concatenation
    - EP318: Parallel Iteration with zip()
    - EP320: Loop Variables After Loop Ends
    - EP321: Be Defensive when Iterating over Arguments
    - EP426: Comprehensive dict.get() patterns
    """

    name = "flake8-patterns"
    version = __version__

    def __init__(self, tree: ast.AST, filename: str = "(none)") -> None:
        """Initialize the checker with an AST tree."""
        super().__init__()
        self.tree = tree
        self.filename = filename
        self.errors: list[Error] = []

    def run(self) -> Generator[Error, None, None]:
        """Run the checker and yield errors."""
        self.errors = []
        self.visit(self.tree)

        yield from self.errors

    def error(
        self, node: ast.AST, code: str, format_vars: dict[str, str] | None = None
    ) -> None:
        """Record an error for the given node and code."""
        message = get_error_message(code)
        if format_vars:
            message = message.format(**format_vars)

        self.errors.append(
            (node.lineno, node.col_offset, f"{code} {message}", type(self))
        )

    # Tier 1: High Impact Effective Python Rules (EP105, EP213, EP318, EP320,
    # EP321, EP426)

    def visit_assign(self, node: ast.Assign) -> None:
        """Check assignment patterns.

        Detects:
        - EP105: Sequential indexing patterns (x = item[0]; y = item[1])
        """
        # EP105: Multiple-Assignment Unpacking over Indexing
        # TODO: Implement detection of sequential indexing assignments
        # Pattern: x = item[0] followed by y = item[1] etc.
        # Suggest: x, y = item

        self.generic_visit(node)

    def visit_for(self, node: ast.For) -> None:
        """Check for loop patterns.

        Detects:
        - EP318: Manual parallel iteration with range(len())
        - EP320: Loop variable usage after loop ends
        - EP321: Functions iterating over arguments multiple times
        """
        # EP318: Parallel Iteration with zip()
        # TODO: Implement detection of range(len()) + manual indexing
        # Pattern: for i in range(len(items)): x = items[i]; y = other[i]
        # Suggest: for x, y in zip(items, other)

        # EP320: Loop Variables After Loop Ends
        # TODO: Track loop variable usage in post-loop scope
        # Pattern: for item in items: ...; if item.condition: ...
        # Suggest: Defensive assignment patterns

        self.generic_visit(node)

    def visit_function_def(self, node: ast.FunctionDef) -> None:
        """Check function definition patterns.

        Detects:
        - EP321: Be Defensive when Iterating over Arguments
        """
        # EP321: Be Defensive when Iterating over Arguments
        # TODO: Detect functions that iterate over same parameter multiple times
        # Pattern: Multiple for loops over same argument without iterator check
        # Suggest: Convert to list or check if iterator

        self.generic_visit(node)

    def visit_try(self, node: ast.Try) -> None:
        """Check try/except patterns.

        Detects:
        - EP426: try/except KeyError patterns that should use dict.get()
        """
        # EP426: Comprehensive dict.get() patterns

        self.generic_visit(node)

    def visit_list(self, node: ast.List) -> None:
        """Check list literal patterns.

        Detects:
        - EP213: Context-aware string concatenation in collections
        """
        # EP213: Context-Aware String Concatenation
        # TODO: Detect implicit string concatenation in list/tuple contexts
        # Pattern: ["string1" "string2", other_item] (missing comma)
        # Suggest: Explicit concatenation or fix missing comma

        self.generic_visit(node)

    # Helper methods for Tier 1 rule detection

    def _is_sequential_indexing_pattern(self, _assignments: list[ast.Assign]) -> bool:
        """Check if assignments follow sequential indexing pattern.

        Detects patterns like:
        x = item[0]
        y = item[1]
        z = item[2]
        """
        # TODO: Implement sequential indexing detection
        # 1. Track consecutive assignments in same scope
        # 2. Check if they access same variable with incrementing indices
        # 3. Suggest multiple assignment unpacking
        return False

    def _is_parallel_iteration_pattern(self, _node: ast.For) -> bool:
        """Check for manual parallel iteration patterns.

        Detects patterns like:
        for i in range(len(items)):
            x = items[i]
            y = other[i]
        """
        # TODO: Implement parallel iteration detection
        # 1. Check for range(len()) pattern
        # 2. Look for multiple indexing operations in loop body
        # 3. Suggest zip() usage
        return False

    def _has_post_loop_variable_usage(self, _node: ast.For) -> bool:
        """Check if loop variable is used after loop ends.

        Detects patterns like:
        for item in items:
            if condition: break
        if item.some_property:  # Dangerous!
            ...
        """
        # TODO: Implement post-loop variable usage detection
        # 1. Track loop variable name
        # 2. Scan following statements in same scope
        # 3. Check if loop variable is referenced
        return False

    def _has_multiple_iteration_over_parameter(self, _node: ast.FunctionDef) -> bool:
        """Check if function iterates over same parameter multiple times.

        Detects patterns like:
        def func(items):
            total = sum(items)      # First iteration
            for item in items:      # Second iteration - fails if iterator!
                process(item)
        """
        # TODO: Implement multiple iteration detection
        # 1. Track parameter names
        # 2. Count iteration usages (for loops, sum(), etc.)
        # 3. Suggest defensive iterator handling
        return False

    def _is_dict_keyerror_pattern(self, _node: ast.Try) -> bool:
        """Check if try/except handles KeyError that should use dict.get().

        Detects patterns like:
        try:
            value = my_dict[key]
        except KeyError:
            value = default
        """
        # TODO: Implement KeyError pattern detection
        # 1. Check if try body has dict access
        # 2. Check if except catches KeyError
        # 3. Check if same variable assigned in both blocks
        # 4. Suggest dict.get() usage
        return False

    def _has_implicit_string_concatenation_in_collection(self, _node: ast.List) -> bool:
        """Check for dangerous implicit string concatenation in collections.

        Detects patterns like:
        items = [
            "string1" "string2",  # Missing comma - becomes one string!
            "string3",
        ]
        """
        # TODO: Implement implicit concatenation detection
        # 1. Check for string literals without commas between them
        # 2. Particularly dangerous in list/tuple contexts
        # 3. Suggest explicit concatenation or fix missing comma
        return False

    # Future implementation notes for remaining tiers

    # Tier 2 rules (Phase 2: v0.4.0-0.6.0) - 14 rules:
    # EP216, EP427, EP12103, EP531, EP538, EP429, EP537, EP748, EP755, EP769,
    # EP770, EP881, EP12121, EP12122

    # Tier 3 rules (Phase 3: v0.7.0+) - 6 rules:
    # EP104, EP108, EP215, EP317, EP641, EP645

    # High Performance Python integration (Phase 4: v0.8.0+):
    # HP001, PC001, MC001, NP001 patterns

    def _check_modern_python_features(self, _node: ast.AST) -> None:
        """Leverage Python 3.10+ features for enhanced pattern detection."""
        if PYTHON_310_PLUS:
            # Could use match statements for complex AST pattern matching
            # Enhanced union types for better type checking
            pass

    def _check_python313_optimizations(self, _node: ast.AST) -> None:
        """Check patterns that benefit from Python 3.13+ optimizations."""
        if PYTHON_313_PLUS:
            # Performance improvements in string operations, generators, etc.
            # Enhanced error messages and debugging features
            pass


# Entry point for flake8
def checker_from_ast(tree: ast.AST, filename: str) -> PerformanceChecker:
    """Create a checker instance from an AST tree (flake8 entry point)."""
    return PerformanceChecker(tree, filename)


# Compatibility function names
PerformancePatternChecker = PerformanceChecker  # Alternative name
checker = checker_from_ast  # Simple function name
