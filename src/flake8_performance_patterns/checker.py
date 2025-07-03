"""
Main checker module for flake8-performance-patterns.

Based on patterns from "High Performance Python" (3rd Edition) and "Effective Python" (3rd Edition).
Follows the successful flake8-bugbear plugin architecture.
"""

import ast
import sys
from typing import Any, Generator, List, Optional, Tuple, Type

from .messages import ALL_MESSAGES, get_error_message
from .utils import (
    PYTHON_310_PLUS,
    PYTHON_313_PLUS,
    NodeVisitorWithParents,
    find_parent_loop,
    get_function_name,
    is_string_literal,
)

# Plugin metadata
__version__ = "0.1.0"

# Error type: (line, column, message, type)
Error = Tuple[int, int, str, Type[Any]]


class PerformanceChecker(NodeVisitorWithParents):
    """
    Main checker class for performance patterns.

    Detects performance anti-patterns from "High Performance Python" (3rd Edition)
    and "Effective Python" (3rd Edition) books.
    """

    name = "flake8-performance-patterns"
    version = __version__

    def __init__(self, tree: ast.AST, filename: str = "(none)"):
        """Initialize the checker with an AST tree."""
        super().__init__()
        self.tree = tree
        self.filename = filename
        self.errors: List[Error] = []

    def run(self) -> Generator[Error, None, None]:
        """Run the checker and yield errors."""
        self.errors = []
        self.visit(self.tree)

        for error in self.errors:
            yield error

    def error(self, node: ast.AST, code: str, vars: Optional[dict] = None) -> None:
        """Record an error for the given node and code."""
        message = get_error_message(code)
        if vars:
            message = message.format(**vars)

        self.errors.append(
            (node.lineno, node.col_offset, f"{code} {message}", type(self))
        )

    # String operation checks (HP001-HP020)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        """Check for string concatenation with += in loops."""
        # HP001: String concatenation using += in loop
        if (
            isinstance(node.op, ast.Add)
            and self._is_string_concatenation(node)
            and self._is_in_loop()
        ):
            self.error(node, "HP001")

        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        """Check binary operations for various patterns."""
        # HP002: Multiple string concatenations
        if (
            isinstance(node.op, ast.Add)
            and self._count_string_concatenations(node) >= 3
        ):
            self.error(node, "HP002")

        # HP003: % string formatting
        if isinstance(node.op, ast.Mod) and is_string_literal(node.left):
            self.error(node, "HP003")

        self.generic_visit(node)

    # Collection performance checks (PC001-PC020)

    def visit_Compare(self, node: ast.Compare) -> None:
        """Check for list membership testing."""
        # PC001: List membership testing
        if (
            len(node.ops) == 1
            and isinstance(node.ops[0], ast.In)
            and self._is_list_literal_or_comprehension(node.comparators[0])
        ):
            self.error(node, "PC001")

        self.generic_visit(node)

    # Iteration pattern checks (EP001-EP020)

    def visit_For(self, node: ast.For) -> None:
        """Check for iteration anti-patterns."""
        # EP001: range(len()) pattern
        if self._is_range_len_pattern(node):
            self.error(node, "EP001")

        self.generic_visit(node)

    # Helper methods

    def _is_string_concatenation(self, node: ast.AugAssign) -> bool:
        """Check if this is a string concatenation operation."""
        # This is a simplified check - in production we'd want more sophisticated
        # type inference or heuristics
        return True  # For now, assume all += in loops could be string concat

    def _is_in_loop(self) -> bool:
        """Check if we're currently inside a loop."""
        return any(isinstance(parent, (ast.For, ast.While)) for parent in self.parents)

    def _count_string_concatenations(self, node: ast.BinOp) -> int:
        """Count consecutive string concatenations."""
        count = 0
        current = node

        while isinstance(current, ast.BinOp) and isinstance(current.op, ast.Add):
            count += 1
            if hasattr(current, "left") and isinstance(current.left, ast.BinOp):
                current = current.left
            else:
                break

        return count

    def _is_list_literal_or_comprehension(self, node: ast.AST) -> bool:
        """Check if node is a list literal or list comprehension."""
        return isinstance(node, (ast.List, ast.ListComp))

    def _is_range_len_pattern(self, node: ast.For) -> bool:
        """Check for range(len(iterable)) pattern."""
        if not isinstance(node.iter, ast.Call):
            return False

        # Check if it's range(len(...))
        if (
            get_function_name(node.iter) == "range"
            and len(node.iter.args) == 1
            and isinstance(node.iter.args[0], ast.Call)
            and get_function_name(node.iter.args[0]) == "len"
        ):
            return True

        return False

    # Python version specific features

    def _check_modern_patterns(self, node: ast.AST) -> None:
        """Check patterns that benefit from Python 3.10+ features."""
        if PYTHON_310_PLUS:
            # Could use match statements for complex pattern detection
            pass

    def _check_latest_optimizations(self, node: ast.AST) -> None:
        """Check patterns optimized in Python 3.13+."""
        if PYTHON_313_PLUS:
            # Latest performance optimizations
            pass


# Entry point for flake8
def checker_from_ast(tree: ast.AST, filename: str) -> PerformanceChecker:
    """Create a checker instance from an AST tree (flake8 entry point)."""
    return PerformanceChecker(tree, filename)


# Compatibility function names
PerformancePatternChecker = PerformanceChecker  # Alternative name
checker = checker_from_ast  # Simple function name
