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
        if len(node.targets) != 1:
            return False

        # Support both regular variables and instance variables (self.x)
        target = node.targets[0]
        if not isinstance(target, (ast.Name, ast.Attribute)):
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

        # Index must be non-negative
        index_value = subscript.slice.value
        if index_value < 0:
            return False

        # Get the variable being indexed
        if not isinstance(subscript.value, ast.Name):
            return False

        indexed_var = subscript.value.id

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

        # Look for any consecutive subsequence of length >= 2
        if not self._has_consecutive_subsequence(indices):
            return False
            
        # Additional heuristic: Don't trigger if all assigned variables 
        # are subsequently used as indices (intermediate pattern)
        # This reduces false positives for cases like:
        # idx1 = indices[0]; idx2 = indices[1]; data[idx1]; data[idx2]
        return self._is_final_usage_pattern(assignments, parent)

    def _has_consecutive_subsequence(self, indices: list[int]) -> bool:
        """Check if there's a consecutive subsequence of length >= 2."""
        if len(indices) < 2:
            return False
            
        indices_set = set(indices)
        
        # Look for consecutive sequences
        for start_idx in indices_set:
            consecutive_count = 0
            current_idx = start_idx
            
            # Count consecutive indices starting from start_idx
            while current_idx in indices_set:
                consecutive_count += 1
                current_idx += 1
                
            # If we found a consecutive sequence of 2 or more
            if consecutive_count >= 2:
                return True
                
        return False

    def _is_final_usage_pattern(self, assignments: list[ast.Assign], parent: ast.AST) -> bool:
        """Check if this is a final usage pattern (not intermediate variables)."""
        # Get all variable names that are assigned in the sequential pattern
        assigned_vars = []
        for assignment in assignments:
            if len(assignment.targets) == 1:
                target = assignment.targets[0]
                if isinstance(target, ast.Name):
                    assigned_vars.append(target.id)
                elif isinstance(target, ast.Attribute):
                    # For self.x patterns, this is likely final usage
                    return True
        
        if not assigned_vars:
            return True
            
        # Check if all these variables are primarily used as subscript indices
        # in subsequent statements (which would suggest they're intermediate)
        subsequent_statements = []
        if hasattr(parent, "body"):
            # Find statements after the assignments
            assignment_lines = {assign.lineno for assign in assignments}
            max_assignment_line = max(assignment_lines)
            
            subsequent_statements = [
                stmt for stmt in parent.body 
                if hasattr(stmt, "lineno") and stmt.lineno > max_assignment_line
            ]
        
        if not subsequent_statements:
            # If no subsequent statements, it's likely final usage
            return True
            
        # Count how many assigned variables are used as indices vs other uses
        index_usage_count = 0
        other_usage_count = 0
        
        for stmt in subsequent_statements:
            for node in ast.walk(stmt):
                if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Name):
                    if node.slice.id in assigned_vars:
                        index_usage_count += 1
                elif isinstance(node, ast.Name) and node.id in assigned_vars:
                    # Check if this is not part of a subscript slice
                    parent_node = getattr(node, 'parent', None)
                    if not (isinstance(parent_node, ast.Subscript) and parent_node.slice == node):
                        other_usage_count += 1
        
        # If most usage is as indices, it's probably intermediate
        # Otherwise, it's likely final usage that should trigger EFP105
        if index_usage_count > 0 and other_usage_count == 0:
            return False  # Primarily used as indices - don't trigger
        
        return True  # Final usage pattern - should trigger

    def _is_indexing_assignment(self, node: ast.Assign, target_var: str) -> bool:
        """Check if assignment is indexing the target variable."""
        if (
            len(node.targets) != 1
            or not isinstance(node.targets[0], (ast.Name, ast.Attribute))
            or not isinstance(node.value, ast.Subscript)
            or not isinstance(node.value.value, ast.Name)
        ):
            return False

        # Check if we're indexing the same variable
        if node.value.value.id != target_var:
            return False
            
        # Ensure we have a constant integer index (no variables)
        if not isinstance(node.value.slice, ast.Constant) or not isinstance(
            node.value.slice.value, int
        ):
            return False
            
        return True
