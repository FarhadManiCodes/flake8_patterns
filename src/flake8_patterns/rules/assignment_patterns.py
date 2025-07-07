"""Assignment and unpacking pattern rules.

Rules for detecting anti-patterns in variable assignments and unpacking operations.
Based on "Effective Python" (3rd Edition) by Brett Slatkin.
"""

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flake8_patterns.checker import PatternChecker


class AssignmentPatternRules:
    """Rules for assignment and unpacking patterns."""

    def check_efp105_sequential_indexing(
        self, node: ast.Assign, checker: "PatternChecker"
    ) -> None:
        """Check EFP105: Multiple-Assignment Unpacking over Indexing.

        Detects patterns like:
        x = item[0]
        y = item[1]
        z = item[2]

        Suggests: x, y, z = item
        """
        if self._is_sequential_indexing_assignment(node, checker):
            checker.error(node, "EFP105")

    def check_efp216_catch_all_unpacking(
        self, node: ast.Assign, checker: "PatternChecker"
    ) -> None:
        """Check EFP216: Catch-All Unpacking over Slicing.

        Future implementation for Phase 2.
        Detects slice assignment patterns that could use catch-all unpacking.
        """
        # TODO: Implement in Phase 2

    def _is_sequential_indexing_assignment(
        self, node: ast.Assign, checker: "PatternChecker"
    ) -> bool:
        """Check if assignment is part of sequential indexing pattern."""
        # Check if this is a simple assignment (not tuple unpacking)
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            return False

        # Check if value is a subscript (indexing)
        if not isinstance(node.value, ast.Subscript):
            return False

        # Check if subscript is accessing with a numeric index
        subscript = node.value
        if not isinstance(subscript.slice, ast.Constant) or not isinstance(
            subscript.slice.value, int
        ):
            return False

        # Get the variable being indexed and the index value
        if not isinstance(subscript.value, ast.Name):
            return False

        indexed_var = subscript.value.id
        index_value = subscript.slice.value

        # Look for other assignments in the same scope that form a pattern
        return self._check_for_sequential_pattern(
            indexed_var, index_value, node, checker
        )

    def _check_for_sequential_pattern(
        self,
        indexed_var: str,
        _index_value: int,
        _current_node: ast.Assign,
        checker: "PatternChecker",
    ) -> bool:
        """Check if there are other assignments that form a sequential pattern."""
        # Get the parent node (should be a statement list)
        parent = checker.get_parent()
        if not parent or not hasattr(parent, "body"):
            return False

        # Find all assignments in the same scope
        assignments = [
            stmt
            for stmt in parent.body
            if isinstance(stmt, ast.Assign)
            and self._is_indexing_assignment(stmt, indexed_var)
        ]

        # Need at least 2 assignments to form a pattern
        if len(assignments) < 2:
            return False

        # Check if we have sequential indices
        indices = [
            assignment.value.slice.value
            for assignment in assignments
            if isinstance(assignment.value, ast.Subscript)
            and isinstance(assignment.value.slice, ast.Constant)
        ]

        # Check if indices are consecutive starting from 0
        indices.sort()
        return indices == list(range(len(indices))) and len(indices) >= 2

    def _is_indexing_assignment(self, node: ast.Assign, target_var: str) -> bool:
        """Check if assignment is indexing the target variable."""
        if (
            len(node.targets) != 1
            or not isinstance(node.targets[0], ast.Name)
            or not isinstance(node.value, ast.Subscript)
            or not isinstance(node.value.value, ast.Name)
        ):
            return False

        return node.value.value.id == target_var
