"""Iteration and loop pattern rules.

Rules for detecting anti-patterns in loops, iteration, and generator usage.
Based on "Effective Python" (3rd Edition) by Brett Slatkin.
"""

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flake8_patterns.checker import PatternChecker


class IterationPatternRules:
    """Rules for iteration and loop patterns."""

    def check_efp318_parallel_iteration(
        self, node: ast.For, checker: "PatternChecker"
    ) -> None:
        """Check EFP318: Parallel Iteration with zip().

        Detects patterns like:
        for i in range(len(items)):
            x = items[i]
            y = other[i]

        Suggests: for x, y in zip(items, other)
        """
        # TODO: Implement EFP318 detection
        # Pattern: for i in range(len()) + manual indexing
        # Suggest: for x, y in zip(items, other)

    def check_efp320_loop_variables_after_loop(
        self, node: ast.For, checker: "PatternChecker"
    ) -> None:
        """Check EFP320: Loop Variables After Loop Ends.

        Detects patterns like:
        for item in items:
            if condition: break
        if item.some_property:  # Dangerous!
            ...
        """
        # TODO: Implement EFP320 detection
        # Track loop variable usage in post-loop scope
        # Pattern: for item in items: ...; if item.condition: ...
        # Suggest: Defensive assignment patterns

    def check_efp321_defensive_iteration(
        self, node: ast.FunctionDef, checker: "PatternChecker"
    ) -> None:
        """Check EFP321: Be Defensive when Iterating over Arguments.

        Detects patterns like:
        def func(items):
            total = sum(items)      # First iteration
            for item in items:      # Second iteration - fails if iterator!
                process(item)
        """
        # TODO: Implement EFP321 detection
        # Detect functions that iterate over same parameter multiple times
        # Pattern: Multiple for loops over same argument without iterator check
        # Suggest: Convert to list or check if iterator

    def check_efp317_enumerate_usage(
        self, node: ast.For, checker: "PatternChecker"
    ) -> None:
        """Check EFP317: Comprehensive enumerate suggestions.

        Detects manual counter increment patterns.
        Future implementation for Phase 3.
        """
        # TODO: Implement in Phase 3

    def check_efp645_yield_from(
        self, node: ast.FunctionDef, checker: "PatternChecker"
    ) -> None:
        """Check EFP645: yield from for Generator Composition.

        Detects manual generator composition patterns.
        Future implementation for Phase 3.
        """
        # TODO: Implement in Phase 3
