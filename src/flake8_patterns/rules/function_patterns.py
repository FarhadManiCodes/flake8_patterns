"""Function and API design pattern rules.

Rules for detecting anti-patterns in function definitions, decorators, and APIs.
Based on "Effective Python" (3rd Edition) by Brett Slatkin.
"""

import ast
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flake8_patterns.checker import PatternChecker


class FunctionPatternRules:
    """Rules for function and API design patterns."""

    def check_efp531_return_objects(
        self, node: ast.Return, checker: "PatternChecker"
    ) -> None:
        """Check EFP531: Return Objects vs >3 Tuple Unpacking.

        Detects functions returning more than 3 values as tuple.
        Future implementation for Phase 2.
        """
        # TODO: Implement in Phase 2

    def check_efp537_keyword_only_arguments(
        self, node: ast.FunctionDef, checker: "PatternChecker"
    ) -> None:
        """Check EFP537: Keyword-Only/Positional-Only Arguments.

        Detects functions that could benefit from keyword-only arguments.
        Future implementation for Phase 2.
        """
        # TODO: Implement in Phase 2

    def check_efp538_functools_wraps(
        self, node: ast.FunctionDef, checker: "PatternChecker"
    ) -> None:
        """Check EFP538: functools.wraps for Decorators.

        Detects decorator functions missing functools.wraps.
        Future implementation for Phase 2.
        """
        # TODO: Implement in Phase 2

    def check_efp748_functions_vs_classes(
        self, node: ast.ClassDef, checker: "PatternChecker"
    ) -> None:
        """Check EFP748: Functions vs Classes for Simple Interfaces.

        Detects simple class interfaces that should be functions.
        Future implementation for Phase 2.
        """
        # TODO: Implement in Phase 2

    def check_efp104_helper_functions(
        self, node: ast.Assign, checker: "PatternChecker"
    ) -> None:
        """Check EFP104: Helper Functions over Complex Expressions.

        Detects complex expressions that should be extracted.
        Future implementation for Phase 3.
        """
        # TODO: Implement in Phase 3

    def check_efp108_assignment_expressions(
        self, node: ast.Assign, checker: "PatternChecker"
    ) -> None:
        """Check EFP108: Assignment Expressions for Repetition.

        Detects repeated expressions that could use walrus operator.
        Future implementation for Phase 3.
        """
        # TODO: Implement in Phase 3
